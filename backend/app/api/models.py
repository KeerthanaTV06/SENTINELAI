"""Machine-learning model endpoints for SENTINEL-AI."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.pipelines.model_manager import (
    evaluate,
    list_models,
    load_model,
    predict,
    save_model,
    train_model,
)

router = APIRouter(prefix="/models", tags=["models"])


@router.post("/train")
async def train_model_route(payload: dict) -> dict:
    try:
        return train_model(
            model_name=payload.get("model_name", "random_forest"),
            dataset_name=payload.get("dataset_name", "nslkdd"),
            max_rows=int(payload.get("max_rows", 1000)),
            random_state=int(payload.get("random_state", 7)),
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("")
async def list_model_routes() -> dict:
    return {"models": list_models()}


@router.get("/{name}")
async def get_model(name: str) -> dict:
    try:
        return load_model(name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{name}/predict")
async def predict_model(name: str, payload: dict) -> dict:
    try:
        predictions = predict(name, dataset_name=payload.get("dataset_name", "nslkdd"), max_rows=int(payload.get("max_rows", 1000)))
        return {"model_name": name, "predictions": predictions}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{name}/evaluate")
async def evaluate_model(name: str, payload: dict) -> dict:
    try:
        return evaluate(name, dataset_name=payload.get("dataset_name", "nslkdd"), max_rows=int(payload.get("max_rows", 1000)))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/save")
async def save_model_route(payload: dict) -> dict:
    try:
        return save_model(
            model_name=payload.get("model_name", "random_forest"),
            model=payload.get("model"),
            metrics=payload.get("metrics"),
            metadata=payload.get("metadata"),
            config=payload.get("config"),
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
