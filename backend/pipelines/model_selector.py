"""Model selector chooses the best model based on evaluation metrics.

A simple implementation that reads saved reports and selects the model with
highest average F1-score across classes.
"""
from __future__ import annotations

import logging
from pathlib import Path
import json

logger = logging.getLogger("sentinel.model_selector")


def load_report(path: Path) -> dict:
    txt = path.read_text()
    try:
        return json.loads(txt)
    except Exception:
        # Fallback for stringified dicts
        return eval(txt)


def choose_best_model(models_dir: Path) -> Path:
    """Return path to best model artifact by average macro F1-score."""
    rf_report = models_dir / "rf_report.json"
    xg_report = models_dir / "xg_report.json"

    scores = {}
    if rf_report.exists():
        r = load_report(rf_report)
        # classification_report dict may contain 'macro avg' or be nested
        try:
            f1 = r.get("macro avg", {}).get("f1-score") or r.get("macro avg", {}).get("f1_score")
        except Exception:
            f1 = None
        scores["rf"] = float(f1) if f1 is not None else 0.0

    if xg_report.exists():
        r = load_report(xg_report)
        try:
            f1 = r.get("macro avg", {}).get("f1-score") or r.get("macro avg", {}).get("f1_score")
        except Exception:
            f1 = None
        scores["xg"] = float(f1) if f1 is not None else 0.0

    logger.info("Model scores: %s", scores)
    best = max(scores.items(), key=lambda kv: kv[1])[0] if scores else None
    if not best:
        raise FileNotFoundError("No model reports found in %s" % models_dir)

    if best == "rf":
        return models_dir / "rf_model.joblib"
    else:
        return models_dir / "xg_model.bst"


if __name__ == "__main__":
    from app_logger import configure_logging
    configure_logging()
    import argparse

    parser = argparse.ArgumentParser(description="Choose best model from models directory")
    parser.add_argument("models_dir", help="Directory containing model artifacts and reports")
    args = parser.parse_args()

    best = choose_best_model(Path(args.models_dir))
    print(best)
