"""Dataset manager orchestrates dataset preparation for SENTINEL-AI.

This module exposes a stable interface for discovering, validating, preparing,
preprocessing, and previewing the synthetic cybersecurity datasets used by the
Week 2 pipeline.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from backend.pipelines.data_validator import (
    generate_dataset_statistics,
    generate_validation_report,
)
from backend.pipelines.dataset_loader import DatasetDownloadError, DatasetLoader
from backend.pipelines.feature_engineer import engineer_features
from backend.pipelines.preprocessing import preprocess_dataframe

logger = logging.getLogger("sentinel.dataset_manager")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATASETS_ROOT = REPO_ROOT / "datasets"
RAW_ROOT = DATASETS_ROOT / "raw"
PROCESSED_ROOT = DATASETS_ROOT / "processed"
METADATA_ROOT = DATASETS_ROOT / "metadata"
METADATA_PATH = METADATA_ROOT / "dataset_info.json"
VALIDATION_REPORT_PATH = METADATA_ROOT / "validation_report.json"
STATISTICS_PATH = METADATA_ROOT / "dataset_statistics.json"

DATASET_REGISTRY: Dict[str, Dict[str, Optional[str]]] = {
    "nslkdd": {
        "display_name": "NSL-KDD",
        "url": None,
        "notes": "Synthetic NSL-KDD style dataset available under datasets/raw/nsl_kdd",
    },
    "cicids2017": {
        "display_name": "CICIDS2017",
        "url": None,
        "notes": "Synthetic CICIDS2017 style dataset available under datasets/raw/cicids2017",
    },
    "phishtank": {
        "display_name": "PhishTank",
        "url": None,
        "notes": "Synthetic PhishTank style dataset available under datasets/raw/phishtank",
    },
    "unsw_nb15": {
        "display_name": "UNSW-NB15",
        "url": None,
        "notes": "Prepared for future local ingestion and pipeline compatibility",
    },
    "malware": {
        "display_name": "Malware",
        "url": None,
        "notes": "Prepared for future local ingestion and pipeline compatibility",
    },
    "iot": {
        "display_name": "IoT",
        "url": None,
        "notes": "Prepared for future local ingestion and pipeline compatibility",
    },
}


def _normalize_name(name: str) -> str:
    value = (name or "").strip().lower().replace(" ", "_").replace("-", "_")
    aliases = {
        "nsl_kdd": "nslkdd",
        "nslkdd": "nslkdd",
        "cicids2017": "cicids2017",
        "cicids": "cicids2017",
        "phishtank": "phishtank",
        "phishing": "phishtank",
        "unsw_nb15": "unsw_nb15",
        "unsw_nb15_dataset": "unsw_nb15",
        "malware": "malware",
        "iot": "iot",
    }
    return aliases.get(value, value)


def _discover_local_datasets() -> Dict[str, Dict[str, Optional[str]]]:
    """Merge registry entries with metadata discovered under datasets/metadata."""
    registry = {k: v.copy() for k, v in DATASET_REGISTRY.items()}
    if not METADATA_PATH.exists():
        return registry

    try:
        payload = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        logger.warning("Unable to read dataset metadata from %s", METADATA_PATH)
        return registry

    for item in payload.get("datasets", []):
        name = item.get("name")
        if not name:
            continue
        key = _normalize_name(name)
        registry[key] = {
            "display_name": item.get("name", key),
            "url": None,
            "notes": item.get("description", "Local synthetic dataset"),
        }

    return registry


DATASET_REGISTRY = _discover_local_datasets()


def _candidate_paths(name: str) -> list[Path]:
    canonical = _normalize_name(name)
    candidates: list[Path] = []
    if canonical == "nslkdd":
        candidates.extend(
            [
                RAW_ROOT / "nsl_kdd" / "train.csv",
                RAW_ROOT / "nslkdd" / "train.csv",
            ]
        )
    elif canonical == "cicids2017":
        candidates.append(RAW_ROOT / "cicids2017" / "cicids.csv")
    elif canonical == "phishtank":
        candidates.append(RAW_ROOT / "phishtank" / "phishing_urls.csv")
    else:
        candidates.extend(
            [
                RAW_ROOT / canonical / f"{canonical}.csv",
                RAW_ROOT / canonical / "data.csv",
                RAW_ROOT / canonical / "dataset.csv",
            ]
        )

    candidates.extend(
        [
            PROCESSED_ROOT / f"{canonical}.csv",
            PROCESSED_ROOT / f"{canonical}.parquet",
            REPO_ROOT / "data" / "raw" / f"{canonical}.csv",
        ]
    )
    return [path for path in candidates if path.exists()]


def load_dataset(name: str, use_processed: bool = False) -> pd.DataFrame:
    """Load a dataset from the local filesystem into a pandas DataFrame."""
    canonical = _normalize_name(name)
    candidate_paths = _candidate_paths(canonical) if not use_processed else [
        PROCESSED_ROOT / f"{canonical}.csv",
        PROCESSED_ROOT / f"{canonical}.parquet",
    ]
    if not candidate_paths:
        raise FileNotFoundError(f"Dataset {canonical} is not available locally")

    path = candidate_paths[0]
    logger.info("Loading dataset %s from %s", canonical, path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def validate_dataset(name: str, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Validate a dataset and persist JSON reports to datasets/metadata."""
    frame = df if df is not None else load_dataset(name)
    report = generate_validation_report(frame, dataset_name=_normalize_name(name))
    report_path = VALIDATION_REPORT_PATH
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    dataset_statistics(name=name, df=frame)
    return report


def prepare_dataset(name: str, url: Optional[str] = None, base_dir: Optional[Path] = None) -> Path:
    """Prepare a dataset from the registry, local path, or URL when provided."""
    canonical = _normalize_name(name)
    if canonical not in DATASET_REGISTRY:
        raise ValueError(f"Unknown dataset: {canonical}")

    info = DATASET_REGISTRY[canonical]
    download_url = url or info.get("url")

    loader = DatasetLoader(base_dir=base_dir or RAW_ROOT)
    if download_url:
        try:
            archive = loader.download(download_url, dest_name=f"{canonical}.csv")
            out = loader.extract(archive, dest_dir=canonical)
            logger.info("Prepared dataset %s at %s", canonical, out)
            return out
        except DatasetDownloadError as exc:
            logger.exception("Failed to download dataset %s", canonical)
            raise FileNotFoundError(str(exc)) from exc

    raw_paths = _candidate_paths(canonical)
    if raw_paths:
        existing = raw_paths[0]
        logger.info("Dataset %s already present at %s", canonical, existing)
        return existing.parent

    fallback = RAW_ROOT / canonical
    fallback.mkdir(parents=True, exist_ok=True)
    logger.info("Created placeholder dataset directory for %s at %s", canonical, fallback)
    return fallback


def list_datasets() -> Dict[str, Dict[str, Optional[str]]]:
    """Return a shallow copy of the dataset registry."""
    return {k: v.copy() for k, v in DATASET_REGISTRY.items()}


def dataset_statistics(name: str, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Compute and persist dataset statistics in JSON."""
    frame = df if df is not None else load_dataset(name)
    stats = generate_dataset_statistics(frame, dataset_name=_normalize_name(name))
    STATISTICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATISTICS_PATH.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return stats


def preview_dataset(name: str, rows: int = 5) -> list[Dict[str, Any]]:
    """Return a lightweight preview of the dataset as a list of records."""
    frame = load_dataset(name)
    preview = frame.head(rows).copy()
    return preview.to_dict(orient="records")


def dataset_metadata(name: str) -> Dict[str, Any]:
    """Return dataset metadata for the given name."""
    canonical = _normalize_name(name)
    info = DATASET_REGISTRY.get(canonical, {})
    frame = load_dataset(canonical)
    return {
        "name": canonical,
        "display_name": info.get("display_name", canonical),
        "notes": info.get("notes", "Local dataset"),
        "path": str(_candidate_paths(canonical)[0] if _candidate_paths(canonical) else None),
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "dtypes": {col: str(dtype) for col, dtype in frame.dtypes.items()},
    }


def split_dataset(
    df: pd.DataFrame,
    train_ratio: float = 0.7,
    validation_ratio: float = 0.15,
    test_ratio: float = 0.15,
    random_state: int = 42,
) -> Dict[str, pd.DataFrame]:
    """Split a DataFrame into train/validation/test subsets."""
    if not 0.0 < train_ratio < 1.0:
        raise ValueError("train_ratio must be between 0 and 1")
    if not 0.0 < validation_ratio < 1.0 or not 0.0 < test_ratio < 1.0:
        raise ValueError("validation_ratio and test_ratio must be between 0 and 1")
    total = train_ratio + validation_ratio + test_ratio
    if not abs(total - 1.0) < 1e-9:
        raise ValueError("Split ratios must sum to 1.0")

    shuffled = df.sample(frac=1, random_state=random_state).reset_index(drop=True)
    train_end = int(len(shuffled) * train_ratio)
    validation_end = train_end + int(len(shuffled) * validation_ratio)
    return {
        "train": shuffled.iloc[:train_end].copy(),
        "validation": shuffled.iloc[train_end:validation_end].copy(),
        "test": shuffled.iloc[validation_end:].copy(),
    }


def prepare_processed_dataset(name: str, target_column: Optional[str] = None) -> pd.DataFrame:
    """Load, engineer, and preprocess a dataset into a training-ready frame."""
    frame = load_dataset(name)
    engineered = engineer_features(frame, dataset_name=_normalize_name(name))
    return preprocess_dataframe(engineered, target_column=target_column, dataset_name=_normalize_name(name))


if __name__ == "__main__":
    import argparse

    import app_logger

    app_logger.configure_logging()
    parser = argparse.ArgumentParser(description="Prepare datasets for SENTINEL-AI")
    parser.add_argument("name", help="Dataset key to prepare (e.g., phishtank)")
    parser.add_argument("--url", help="Optional URL override for download")
    args = parser.parse_args()

    path = prepare_dataset(args.name, url=args.url)
    print(f"Prepared dataset at: {path}")
