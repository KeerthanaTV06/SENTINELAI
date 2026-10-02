"""Reusable preprocessing utilities for the SENTINEL-AI pipeline."""
from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Optional

import pandas as pd
from sklearn.utils import resample

logger = logging.getLogger("sentinel.preprocessing")

REPO_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_ROOT = REPO_ROOT / "datasets" / "processed"
CACHE_ROOT = PROCESSED_ROOT / "cache"
PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)
CACHE_ROOT.mkdir(parents=True, exist_ok=True)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to lower snake_case strings."""
    frame = df.copy()
    frame.columns = [str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in frame.columns]
    return frame


def preprocess_dataframe(
    df: pd.DataFrame,
    target_column: Optional[str] = None,
    dataset_name: str = "dataset",
    scaling: str = "standard",
    balance: bool = False,
    use_cache: bool = True,
    cache_dir: Optional[Path] = None,
) -> pd.DataFrame:
    """Clean, encode, scale, balance, and persist a preprocessed dataset."""
    frame = df.copy()
    frame = normalize_column_names(frame)

    if target_column is not None and target_column not in frame.columns:
        for candidate in ["label", "Label", "target"]:
            if candidate in frame.columns:
                target_column = candidate
                break

    for column in frame.columns:
        if column == target_column:
            continue
        if pd.api.types.is_numeric_dtype(frame[column]):
            frame[column] = frame[column].fillna(frame[column].median())
        else:
            mode = frame[column].mode(dropna=True)
            fill_value = mode.iloc[0] if not mode.empty else "missing"
            frame[column] = frame[column].fillna(fill_value)

    categorical_columns = [
        column for column in frame.columns if column != target_column and not pd.api.types.is_numeric_dtype(frame[column])
    ]
    if categorical_columns:
        frame = pd.get_dummies(frame, columns=categorical_columns, drop_first=False)

    if target_column and target_column in frame.columns and pd.api.types.is_numeric_dtype(frame[target_column]):
        target = frame[target_column]
        numeric_columns = [col for col in frame.columns if col != target_column and pd.api.types.is_numeric_dtype(frame[col])]
        for column in numeric_columns:
            if scaling == "standard":
                mean = frame[column].mean()
                std = frame[column].std(ddof=0)
                frame[column] = (frame[column] - mean) / std if std else 0.0
            elif scaling == "minmax":
                min_val = frame[column].min()
                max_val = frame[column].max()
                frame[column] = (frame[column] - min_val) / (max_val - min_val) if max_val != min_val else 0.0
        frame[target_column] = target

    if balance and target_column and target_column in frame.columns and frame[target_column].nunique() > 1:
        frames = []
        for value in frame[target_column].dropna().unique():
            subset = frame[frame[target_column] == value]
            max_count = int(frame[target_column].value_counts().max())
            if len(subset) < max_count:
                subset = resample(subset, replace=True, n_samples=max_count, random_state=42)
            else:
                subset = subset.sample(n=max_count, random_state=42)
            frames.append(subset)
        frame = pd.concat(frames, axis=0).reset_index(drop=True)

    cache_dir = cache_dir or CACHE_ROOT
    cache_dir.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(pd.util.hash_pandas_object(frame, index=True).values.tobytes()).hexdigest()[:12]
    cache_path = cache_dir / f"{dataset_name}_{digest}_preprocessed.csv"
    if use_cache and cache_path.exists():
        logger.info("Loaded cached preprocessed dataset from %s", cache_path)
        return pd.read_csv(cache_path)

    frame.to_csv(cache_path, index=False)
    logger.info("Wrote preprocessed dataset to %s", cache_path)
    return frame


def simple_clean_csv(file_path: Path, out_name: Optional[str] = None) -> Path:
    """Clean a CSV file and write the processed version to datasets/processed."""
    if not file_path.exists():
        raise FileNotFoundError(file_path)

    out_name = out_name or file_path.stem
    out_path = PROCESSED_ROOT / f"{out_name}.csv"
    frame = pd.read_csv(file_path)
    cleaned = preprocess_dataframe(frame, dataset_name=out_name, use_cache=False)
    cleaned.to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    import argparse

    import app_logger

    app_logger.configure_logging()
    parser = argparse.ArgumentParser(description="Simple CSV preprocessing")
    parser.add_argument("csv", help="Path to CSV file")
    parser.add_argument("--out-name", help="Output name under datasets/processed")
    args = parser.parse_args()

    path = simple_clean_csv(Path(args.csv), out_name=args.out_name)
    print(path)
