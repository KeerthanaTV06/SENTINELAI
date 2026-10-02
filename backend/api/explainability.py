"""API endpoints for explainability features."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.explainability.explainer import ExplanationService
from backend.pipelines.dataset_manager import load_dataset

router = APIRouter()
logger = logging.getLogger("sentinel.api.explainability")

service = ExplanationService(models_dir=Path("models") / "trained")


class ExplainRequest(BaseModel):
    features: List[float]
    feature_names: List[str]


def get_feature_names(model_name: str):
    """
    Load feature names from the training dataset instead of expecting
    models/<name>.features.json
    """
    try:
        metadata_path = (
            Path("models")
            / "trained"
            / "metadata"
            / f"{model_name}.json"
        )

        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text())

            dataset_name = metadata.get("dataset_name", "nslkdd")
        else:
            dataset_name = "nslkdd"

        df = load_dataset(dataset_name)

        feature_names = [
            c for c in df.columns
            if c.lower() != "label"
        ]

        return feature_names

    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code=500,
            detail="Unable to load feature names",
        )


@router.get("/api/v1/models/{model}/features")
async def get_features(model: str):
    return {
        "features": get_feature_names(model)
    }


@router.get("/api/v1/models/{model}/importance")
async def get_importance(model: str, top_k: int = 20):

    try:
        feature_names = get_feature_names(model)

        return service.feature_importance(
            model,
            feature_names,
            top_k,
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    except Exception as exc:
        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get("/api/v1/models/{model}/summary")
async def get_summary(model: str):

    try:
        feature_names = get_feature_names(model)

        return service.global_summary(
            model,
            feature_names,
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    except Exception as exc:
        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/api/v1/models/{model}/explain")
async def explain(model: str, body: ExplainRequest):

    try:
        return service.explain_prediction(
            model,
            body.feature_names,
            body.features,
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    except Exception as exc:
        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )