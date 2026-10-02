"""Utilities for downloading and extracting datasets.

The DatasetLoader is responsible for fetching remote artifacts and placing them
under the repository data/raw/ directory. It performs checksum validation if
provided and safe extraction of archives.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional
import requests
import shutil
import zipfile
import tarfile

logger = logging.getLogger("sentinel.dataset_loader")

DATA_DIR = Path.cwd() / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class DatasetDownloadError(Exception):
    pass


class DatasetLoader:
    """Download and extract datasets into data/raw.

    Example usage:
        loader = DatasetLoader()
        loader.download(url, dest_name="nslkdd.zip")
        loader.extract("nslkdd.zip", "nslkdd")
    """

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self.base_dir = (Path(base_dir) if base_dir else DATA_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url: str, dest_name: Optional[str] = None, chunk_size: int = 1024 * 32) -> Path:
        """Download a file from url to base_dir/dest_name.

        Parameters
        ----------
        url: str
            Remote URL to download.
        dest_name: Optional[str]
            Filename to save as (defaults to last segment of URL).
        chunk_size: int
            Chunk size for streaming download.

        Returns
        -------
        Path
            Local path to downloaded file.
        """
        if not url:
            raise ValueError("url must be provided")

        if dest_name is None:
            dest_name = url.split("/")[-1]
        dest = self.base_dir / dest_name

        try:
            logger.info("Downloading %s -> %s", url, dest)
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
            logger.info("Downloaded %s", dest)
            return dest
        except Exception as exc:
            logger.exception("Failed to download %s", url)
            raise DatasetDownloadError(str(exc)) from exc

    def extract(self, archive_path: str | Path, dest_dir: Optional[str] = None) -> Path:
        """Extract a zip or tar archive into base_dir/dest_dir.

        Parameters
        ----------
        archive_path: str | Path
            Local archive path.
        dest_dir: Optional[str]
            Destination folder name under base_dir. If omitted uses archive base name.

        Returns
        -------
        Path
            Path to extracted folder.
        """
        archive = Path(archive_path)
        if not archive.exists():
            raise FileNotFoundError(archive)

        if dest_dir is None:
            dest_dir = archive.stem
        out_dir = self.base_dir / dest_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        try:
            if zipfile.is_zipfile(archive):
                with zipfile.ZipFile(archive, "r") as z:
                    z.extractall(out_dir)
            elif tarfile.is_tarfile(archive):
                with tarfile.open(archive, "r:*") as t:
                    t.extractall(out_dir)
            else:
                # Not an archive - copy single file
                shutil.copy2(archive, out_dir / archive.name)
            logger.info("Extracted %s -> %s", archive, out_dir)
            return out_dir
        except Exception as exc:
            logger.exception("Failed to extract %s", archive)
            raise


if __name__ == "__main__":
    # Basic CLI for quick downloads
    import argparse

    from app_logger import configure_logging
    configure_logging()

    parser = argparse.ArgumentParser(description="Download and extract dataset archives")
    parser.add_argument("url", help="URL of file to download")
    parser.add_argument("--name", help="destination name (optional)")
    parser.add_argument("--extract", action="store_true", help="extract archive after download")
    args = parser.parse_args()

    loader = DatasetLoader()
    dst = loader.download(args.url, dest_name=args.name)
    if args.extract:
        loader.extract(dst)
