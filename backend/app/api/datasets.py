"""Dataset API endpoints for the SENTINEL-AI pipeline."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.pipelines.dataset_manager import (
    dataset_metadata,
    dataset_statistics,
    list_datasets,
    load_dataset,
    prepare_dataset,
    preview_dataset,
    validate_dataset,
)

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("")
async def get_datasets() -> dict:
    return {"datasets": list_datasets()}


@router.get("/{name}")
async def get_dataset(name: str) -> dict:
    try:
        frame = load_dataset(name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"name": name, "rows": int(len(frame)), "columns": list(frame.columns)}


@router.get("/{name}/stats")
async def get_dataset_stats(name: str) -> dict:
    try:
        return dataset_statistics(name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{name}/preview")
async def get_dataset_preview(name: str, rows: int = 5) -> dict:
    try:
        return {"rows": preview_dataset(name, rows=rows)}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{name}/validate")
async def validate_dataset_route(name: str) -> dict:
    try:
        return validate_dataset(name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{name}/prepare")
async def prepare_dataset_route(name: str) -> dict:
    try:
        prepared_path = prepare_dataset(name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"name": name, "path": str(prepared_path)}


@router.get("/{name}/metadata")
async def get_dataset_metadata(name: str) -> dict:
    try:
        return dataset_metadata(name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
