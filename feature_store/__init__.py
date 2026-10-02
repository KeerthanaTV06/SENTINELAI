"""Feature store package.

This package will contain utilities to write/read Parquet feature files and
integrate with the feature pipeline.
"""
from __future__ import annotations

__all__ = ["FeatureStore"]


class FeatureStore:
    """Minimal feature store placeholder for Day 1.

    This provides file-based save/load operations for Parquet-backed features.
    """
    def __init__(self, base_path: str = "data/processed") -> None:
        self.base_path = base_path

    def path_for(self, name: str) -> str:
        return f"{self.base_path}/{name}.parquet"

    def save(self, df, name: str) -> None:
        """Save a pandas DataFrame to Parquet.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to persist.
        name : str
            Logical dataset name.
        """
        import pandas as pd
        path = self.path_for(name)
        df.to_parquet(path)

    def load(self, name: str):
        """Load a parquet file as pandas.DataFrame.

        Returns
        -------
        pandas.DataFrame
        """
        import pandas as pd
        path = self.path_for(name)
        return pd.read_parquet(path)
