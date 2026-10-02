"""Schema validation utilities that use Pydantic models to validate rows.

The validator reads CSV files chunk-wise and yields bad rows or raises on fatal errors.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, Tuple, List
import pandas as pd

from backend.schemas.schema import NetworkEvent, PhishingEvent, MalwareEvent

logger = logging.getLogger("sentinel.validation")


def validate_csv_with_model(csv_path: Path, model, chunk_size: int = 10000) -> Tuple[int, List[dict]]:
    """Validate CSV rows against a pydantic model.

    Returns number of validated rows and list of example invalid rows (up to 10).
    """
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    total = 0
    invalid_examples = []

    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        for _, row in chunk.iterrows():
            total += 1
            data = row.to_dict()
            try:
                model(**data)
            except Exception as exc:
                if len(invalid_examples) < 10:
                    invalid_examples.append({"row": data, "error": str(exc)})
                logger.debug("Row failed validation: %s", exc)

    return total, invalid_examples


def validate_dataset_folder(folder: Path) -> dict:
    """Scan a dataset folder and attempt validation where possible.

    Looks for common CSV filenames and applies heuristics to choose a model.
    """
    results = {}
    for file in folder.glob("**/*.csv"):
        name = file.name.lower()
        if "phish" in name or "phishtank" in name:
            model = PhishingEvent
        elif "nsl" in name or "kdd" in name or "connection" in name:
            model = NetworkEvent
        else:
            model = NetworkEvent

        total, invalid = validate_csv_with_model(file, model)
        results[str(file)] = {"total": total, "invalid_examples": invalid}

    return results
