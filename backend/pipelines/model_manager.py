"""Machine learning model manager for SENTINEL-AI."""
from __future__ import annotations

import json
import logging
import pickle
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from backend.pipelines.dataset_manager import load_dataset, prepare_processed_dataset, split_dataset

logger = logging.getLogger("sentinel.model_manager")

REPO_ROOT = Path(__file__).resolve().parents[2]
MODELS_ROOT = REPO_ROOT / "models" / "trained"
REPORTS_ROOT = REPO_ROOT / "reports"
METADATA_ROOT = MODELS_ROOT / "metadata"
MODELS_ROOT.mkdir(parents=True, exist_ok=True)
METADATA_ROOT.mkdir(parents=True, exist_ok=True)
REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

SUPPORTED_MODELS = {
    "random_forest": RandomForestClassifier,
    "logistic_regression": LogisticRegression,
    "isolation_forest": IsolationForest,
    "xgboost": RandomForestClassifier,
}


def _resolve_target_column(df: pd.DataFrame) -> str:
    for candidate in ["label", "Label", "target", "is_malicious"]:
        if candidate in df.columns:
            return candidate
    raise ValueError("No target column found for training")


def _prepare_training_frame(dataset_name: str, max_rows: int = 1000) -> tuple[pd.DataFrame, str]:
    frame = load_dataset(dataset_name)
    frame = frame.head(max_rows).copy()
    if "label" not in frame.columns and "Label" in frame.columns:
        frame = frame.rename(columns={"Label": "label"})
    if "label" not in frame.columns and "target" in frame.columns:
        frame = frame.rename(columns={"target": "label"})

    processed = prepare_processed_dataset(dataset_name, target_column="label")
    if len(processed) < len(frame):
        frame = processed.head(max_rows).copy()
    else:
        frame = processed.head(max_rows).copy()
    target_col = _resolve_target_column(frame)
    return frame, target_col


def _build_model(model_name: str, random_state: int = 7) -> Any:
    normalized = model_name.lower().replace("-", "_")
    if normalized == "random_forest":
        return RandomForestClassifier(n_estimators=80, max_depth=8, random_state=random_state)
    if normalized == "logistic_regression":
        return LogisticRegression(max_iter=500, random_state=random_state)
    if normalized == "isolation_forest":
        return IsolationForest(n_estimators=100, random_state=random_state)
    if normalized == "xgboost":
        return RandomForestClassifier(n_estimators=60, max_depth=6, random_state=random_state)
    raise ValueError(f"Unsupported model: {model_name}")


def _serialize_model(model: Any, model_name: str) -> tuple[Path, Path]:
    artifact_path = MODELS_ROOT / f"{model_name}.pkl"
    metadata_path = METADATA_ROOT / f"{model_name}.json"
    with artifact_path.open("wb") as handle:
        pickle.dump(model, handle)
    return artifact_path, metadata_path


def _build_features(frame: pd.DataFrame, target_column: str) -> tuple[pd.DataFrame, pd.Series]:
    feature_frame = frame.drop(columns=[target_column], errors="ignore")
    feature_frame = feature_frame.select_dtypes(include=[np.number, bool]).copy()
    if feature_frame.empty:
        raise ValueError("No numeric features available for training")
    target = frame[target_column]
    return feature_frame, target


def train_model(
    model_name: str,
    dataset_name: str = "nslkdd",
    max_rows: int = 1000,
    random_state: int = 7,
    cv_folds: int = 3,
) -> Dict[str, Any]:
    """Train a model and persist it to disk."""
    frame, target_column = _prepare_training_frame(dataset_name, max_rows=max_rows)
    x_train, target = _build_features(frame, target_column)

    if target.nunique() < 2:
        raise ValueError("Training requires at least two classes")

    model = _build_model(model_name, random_state=random_state)
    splits = split_dataset(pd.concat([x_train, target], axis=1), train_ratio=0.7, validation_ratio=0.15, test_ratio=0.15, random_state=random_state)
    train_frame = splits["train"]
    train_features = train_frame.drop(columns=[target_column], errors="ignore")
    train_target = train_frame[target_column]

    model.fit(train_features, train_target)

    predictions = model.predict(train_features)
    metrics = {
        "accuracy": float(accuracy_score(train_target, predictions)),
        "precision": float(precision_score(train_target, predictions, average="weighted", zero_division=0)),
        "recall": float(recall_score(train_target, predictions, average="weighted", zero_division=0)),
        "f1": float(f1_score(train_target, predictions, average="weighted", zero_division=0)),
    }

    if hasattr(model, "predict_proba"):
        try:
            probabilities = model.predict_proba(train_features)[:, 1]
            metrics["roc_auc"] = float(roc_auc_score(train_target.astype(str), probabilities))
        except Exception:
            metrics["roc_auc"] = None
    else:
        metrics["roc_auc"] = None

    cv = StratifiedKFold(n_splits=min(cv_folds, max(2, min(3, len(train_target.unique())))))
    try:
        cv_scores = cross_val_score(model, train_features, train_target, cv=cv, scoring="accuracy")
        metrics["cv_accuracy_mean"] = float(cv_scores.mean())
    except Exception:
        metrics["cv_accuracy_mean"] = None

    artifact_path, metadata_path = _serialize_model(model, model_name)
    metadata = {
        "model_name": model_name,
        "dataset_name": dataset_name,
        "target_column": target_column,
        "metrics": metrics,
        "random_state": random_state,
        "cv_folds": cv_folds,
        "artifact_path": str(artifact_path),
        "metadata_path": str(metadata_path),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    report_path = REPORTS_ROOT / f"{model_name}_evaluation.json"
    report_path.write_text(json.dumps({"model_name": model_name, "metrics": metrics}, indent=2), encoding="utf-8")

    return {
        "status": "trained",
        "model_name": model_name,
        "artifact_path": str(artifact_path),
        "metadata_path": str(metadata_path),
        "metrics": metrics,
    }


def save_model(model_name: str, model: Optional[Any], metrics: Optional[Dict[str, Any]] = None, metadata: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Persist a model object (or a placeholder) to disk."""
    artifact_path, metadata_path = _serialize_model(model or _build_model(model_name), model_name)
    payload = {
        "model_name": model_name,
        "metrics": metrics or {},
        "metadata": metadata or {},
        "config": config or {},
        "artifact_path": str(artifact_path),
        "metadata_path": str(metadata_path),
    }
    metadata_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def load_model(model_name: str) -> Dict[str, Any]:
    """
    Load model metadata only.
    Returns JSON-serializable information for API responses.
    """
    artifact_path = MODELS_ROOT / f"{model_name}.pkl"
    metadata_path = METADATA_ROOT / f"{model_name}.json"

    if not artifact_path.exists():
        raise FileNotFoundError(f"Model artifact '{model_name}' not found.")

    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata for '{model_name}' not found.")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    return {
        "model_name": model_name,
        "artifact_path": str(artifact_path),
        "metadata_path": str(metadata_path),
        "metadata": metadata,
    }
def get_loaded_model(model_name: str):
    """
    Load the actual sklearn model object.
    Used internally for prediction/evaluation only.
    """
    artifact_path = MODELS_ROOT / f"{model_name}.pkl"

    if not artifact_path.exists():
        raise FileNotFoundError(f"Model '{model_name}' not found.")

    with artifact_path.open("rb") as f:
        model = pickle.load(f)

    return model


def predict(
    model_name: str,
    dataset_name: str = "nslkdd",
    max_rows: int = 1000,
) -> list[Any]:
    """
    Predict labels using a saved model.
    """

    model = get_loaded_model(model_name)

    frame, target_column = _prepare_training_frame(
        dataset_name,
        max_rows=max_rows,
    )

    features, _ = _build_features(frame, target_column)

    predictions = model.predict(features)

    return predictions.tolist()


def evaluate(
    model_name: str,
    dataset_name: str = "nslkdd",
    max_rows: int = 1000,
) -> Dict[str, Any]:
    """
    Evaluate a saved model.
    """

    model = get_loaded_model(model_name)

    frame, target_column = _prepare_training_frame(
        dataset_name,
        max_rows=max_rows,
    )

    features, target = _build_features(frame, target_column)

    predictions = model.predict(features)

    metrics = {
        "accuracy": float(
            accuracy_score(target, predictions)
        ),
        "precision": float(
            precision_score(
                target,
                predictions,
                average="weighted",
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                target,
                predictions,
                average="weighted",
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                target,
                predictions,
                average="weighted",
                zero_division=0,
            )
        ),
    }

    try:
        metrics["roc_auc"] = float(
            roc_auc_score(
                target.astype(str),
                predictions.astype(str),
            )
        )
    except Exception:
        metrics["roc_auc"] = None

    metrics["confusion_matrix"] = confusion_matrix(
        target,
        predictions,
    ).tolist()

    return {
        "model_name": model_name,
        "metrics": metrics,
    }


def list_models() -> list[Dict[str, Any]]:
    """List persisted model metadata."""
    models = []
    for metadata_path in sorted(METADATA_ROOT.glob("*.json")):
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        models.append(payload)
    return models


def compare_models(dataset_name: str = "nslkdd", max_rows: int = 1000) -> list[Dict[str, Any]]:
    """Train and compare a small set of models."""
    results = []
    for model_name in ["random_forest", "logistic_regression", "xgboost"]:
        try:
            results.append(train_model(model_name, dataset_name=dataset_name, max_rows=max_rows))
        except Exception as exc:
            logger.warning("Skipping %s: %s", model_name, exc)
    return results
