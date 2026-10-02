"""Validation helpers for the Sentinel AI data pipeline.

The pipeline uses lightweight pandas-based validation and writes JSON and chart
artifacts for downstream monitoring.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

import pandas as pd

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - optional dependency
    plt = None

logger = logging.getLogger("sentinel.data_validator")

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORTS_ROOT = REPO_ROOT / "reports"
METADATA_ROOT = REPO_ROOT / "datasets" / "metadata"


def _safe_numeric_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]


def _infer_invalid_labels(df: pd.DataFrame, label_column: str | None = None) -> list[dict[str, Any]]:
    if label_column is None:
        for candidate in ["label", "Label", "target"]:
            if candidate in df.columns:
                label_column = candidate
                break
    if label_column is None or label_column not in df.columns:
        return []

    values = df[label_column].astype(str).str.strip()
    issues = []
    empty = values.eq("").sum()
    if empty:
        issues.append({"column": label_column, "issue": "empty_labels", "count": int(empty)})
    return issues


def generate_validation_report(df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
    """Generate a validation report for a DataFrame."""
    frame = df.copy()
    missing_values = {col: int(count) for col, count in frame.isna().sum().items() if int(count) > 0}
    duplicate_rows = int(frame.duplicated().sum())
    invalid_labels = _infer_invalid_labels(frame)

    numeric_columns = _safe_numeric_columns(frame)
    outlier_counts: Dict[str, int] = {}
    feature_ranges: Dict[str, Dict[str, float]] = {}
    for col in numeric_columns:
        series = frame[col].dropna()
        if series.empty:
            continue
        mean = float(series.mean())
        std = float(series.std(ddof=0))
        if std == 0:
            outlier_counts[col] = 0
        else:
            z_scores = (series - mean) / std
            outlier_counts[col] = int(((z_scores.abs() > 3).sum()))
        feature_ranges[col] = {
            "min": float(series.min()),
            "max": float(series.max()),
        }

    issues = []
    if missing_values:
        issues.append("missing_values")
    if duplicate_rows > 0:
        issues.append("duplicate_rows")
    if invalid_labels:
        issues.append("invalid_labels")
    if any(outlier_counts.values()):
        issues.append("outliers")

    status = "ok" if not issues else "warning"
    report = {
        "dataset": dataset_name,
        "status": status,
        "summary": {
            "rows": int(len(frame)),
            "columns": int(len(frame.columns)),
            "missing_values": int(frame.isna().sum().sum()),
            "duplicate_rows": duplicate_rows,
            "invalid_labels": len(invalid_labels),
            "outlier_columns": {k: v for k, v in outlier_counts.items() if v > 0},
        },
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "invalid_labels": invalid_labels,
        "incorrect_dtypes": {},
        "outliers": outlier_counts,
        "feature_ranges": feature_ranges,
        "issues": issues,
    }

    _write_json(METADATA_ROOT / "validation_report.json", report)
    _generate_visualizations(frame, dataset_name)
    return report


def generate_dataset_statistics(df: pd.DataFrame, dataset_name: str = "dataset") -> Dict[str, Any]:
    """Generate dataset summary statistics."""
    frame = df.copy()
    numeric_columns = _safe_numeric_columns(frame)
    stats = {
        "dataset": dataset_name,
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "dtypes": {col: str(dtype) for col, dtype in frame.dtypes.items()},
        "missing_values": {col: int(count) for col, count in frame.isna().sum().items() if int(count) > 0},
        "label_distribution": {},
        "numeric_summary": {},
    }

    label_candidates = [col for col in ["label", "Label", "target"] if col in frame.columns]
    if label_candidates:
        label_col = label_candidates[0]
        stats["label_distribution"] = {
            str(key): int(value) for key, value in frame[label_col].value_counts(dropna=False).items()
        }

    for col in numeric_columns:
        series = frame[col].dropna()
        stats["numeric_summary"][col] = {
            "mean": float(series.mean()) if not series.empty else None,
            "median": float(series.median()) if not series.empty else None,
            "std": float(series.std()) if not series.empty else None,
            "min": float(series.min()) if not series.empty else None,
            "max": float(series.max()) if not series.empty else None,
        }

    _write_json(METADATA_ROOT / "dataset_statistics.json", stats)
    return stats


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _generate_visualizations(df: pd.DataFrame, dataset_name: str) -> None:
    output_dir = REPORTS_ROOT / dataset_name
    output_dir.mkdir(parents=True, exist_ok=True)

    if plt is None:
        logger.warning("matplotlib is not available; skipping chart generation")
        return

    label_candidates = [col for col in ["label", "Label", "target"] if col in df.columns]
    if label_candidates:
        label_col = label_candidates[0]
        counts = df[label_col].value_counts(dropna=False)
        fig, ax = plt.subplots(figsize=(6, 4))
        counts.plot(kind="bar", ax=ax)
        ax.set_title(f"{dataset_name} class distribution")
        ax.set_xlabel(label_col)
        ax.set_ylabel("Count")
        fig.tight_layout()
        fig.savefig(output_dir / "class_distribution.png", dpi=150)
        plt.close(fig)

    numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    if len(numeric_columns) >= 2:
        corr = df[numeric_columns].corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(7, 6))
        im = ax.imshow(corr, cmap="coolwarm")
        ax.set_title(f"{dataset_name} correlation heatmap")
        ax.set_xticks(range(len(numeric_columns)))
        ax.set_xticklabels(numeric_columns, rotation=45, ha="right")
        ax.set_yticks(range(len(numeric_columns)))
        ax.set_yticklabels(numeric_columns)
        fig.colorbar(im, ax=ax, shrink=0.9)
        fig.tight_layout()
        fig.savefig(output_dir / "correlation_heatmap.png", dpi=150)
        plt.close(fig)

    missing = df.isna().sum().sort_values(ascending=False)
    missing_non_zero = missing[missing > 0]
    if not missing_non_zero.empty:
        fig, ax = plt.subplots(figsize=(6, 4))
        missing_non_zero.plot(kind="bar", ax=ax)
        ax.set_title(f"{dataset_name} missing values")
        ax.set_ylabel("Missing count")
        fig.tight_layout()
        fig.savefig(output_dir / "missing_values.png", dpi=150)
        plt.close(fig)


if __name__ == "__main__":
    import pandas as pd

    sample = pd.DataFrame({"a": [1, 2, 3, None], "b": ["x", "x", "y", "y"], "label": ["normal", "normal", "attack", "attack"]})
    print(generate_validation_report(sample, dataset_name="sample"))
    print(generate_dataset_statistics(sample, dataset_name="sample"))
