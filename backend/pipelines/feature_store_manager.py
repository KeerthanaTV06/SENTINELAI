"""Feature store manager that uses Parquet files for feature persistence.

This module builds on top of the simple FeatureStore helper in feature_store
package and provides versioned filenames and basic metadata tracking.
"""
from __future__ import annotations

import logging
from pathlib import Path
from datetime import datetime
import pandas as pd

from feature_store import FeatureStore

logger = logging.getLogger("sentinel.feature_store_manager")

FS_BASE = Path.cwd() / "data" / "processed"
FS_BASE.mkdir(parents=True, exist_ok=True)


class FeatureStoreManager:
    def __init__(self, base_path: str = str(FS_BASE)) -> None:
        self.store = FeatureStore(base_path=base_path)

    def save_features(self, df: pd.DataFrame, name: str, version: Optional[str] = None) -> Path:
        """Save features with versioning in the filename and return path."""
        version = version or datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{name}_v{version}"
        path = Path(self.store.path_for(filename))
        df.to_parquet(path)
        logger.info("Saved features to %s", path)
        return path

    def load_latest(self, name: str) -> pd.DataFrame:
        """Load the latest saved feature file for the given name."""
        candidates = sorted(Path(self.store.base_path).glob(f"{name}_v*.parquet"))
        if not candidates:
            raise FileNotFoundError(f"No feature files found for {name}")
        latest = candidates[-1]
        logger.info("Loading latest features from %s", latest)
        return pd.read_parquet(latest)
