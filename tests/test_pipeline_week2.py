from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.pipelines.dataset_manager import (
    dataset_metadata,
    dataset_statistics,
    list_datasets,
    load_dataset,
    prepare_dataset,
    preview_dataset,
    split_dataset,
    validate_dataset,
)
from backend.pipelines.preprocessing import preprocess_dataframe

client = TestClient(app)


def test_dataset_manager_discovers_supported_datasets():
    datasets = list_datasets()
    for name in ["nslkdd", "cicids2017", "phishtank", "unsw_nb15", "malware", "iot"]:
        assert name in datasets


def test_load_and_prepare_dataset_work_locally():
    dataset_path = prepare_dataset("nslkdd")
    assert dataset_path.exists()

    df = load_dataset("nslkdd")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_validation_report_and_statistics_are_generated():
    report = validate_dataset("nslkdd")
    assert report["status"] in {"ok", "warning"}
    stats_path = Path("datasets/metadata/dataset_statistics.json")
    report_path = Path("datasets/metadata/validation_report.json")
    assert stats_path.exists()
    assert report_path.exists()


def test_preprocessing_and_splitting_work():
    df = load_dataset("nslkdd")
    processed = preprocess_dataframe(df, target_column="label")
    assert isinstance(processed, pd.DataFrame)
    assert not processed.empty

    splits = split_dataset(df, train_ratio=0.7, validation_ratio=0.15, test_ratio=0.15, random_state=7)
    assert set(splits.keys()) == {"train", "validation", "test"}
    assert all(len(v) > 0 for v in splits.values())


def test_dataset_summary_and_api_endpoints():
    stats = dataset_statistics("nslkdd")
    assert stats["rows"] > 0

    preview = preview_dataset("nslkdd", rows=5)
    assert len(preview) <= 5

    meta = dataset_metadata("nslkdd")
    assert meta["name"] == "nslkdd"

    response = client.get("/api/v1/datasets")
    assert response.status_code == 200

    validate_response = client.post("/api/v1/datasets/nslkdd/validate")
    assert validate_response.status_code == 200
