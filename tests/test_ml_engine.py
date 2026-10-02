from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.pipelines.model_manager import (
    evaluate,
    list_models,
    load_model,
    predict,
    save_model,
    train_model,
)

client = TestClient(app)


def test_train_and_persist_model():
    result = train_model("random_forest", dataset_name="nslkdd", max_rows=500, random_state=7)
    assert result["status"] == "trained"
    assert result["metrics"]["accuracy"] >= 0.0
    assert Path(result["artifact_path"]).exists()
    assert Path(result["metadata_path"]).exists()


def test_load_predict_and_evaluate_model():
    result = train_model("logistic_regression", dataset_name="nslkdd", max_rows=500, random_state=7)
    loaded = load_model(result["model_name"])
    assert loaded["model_name"] == result["model_name"]

    predictions = predict(result["model_name"], dataset_name="nslkdd", max_rows=500)
    assert len(predictions) > 0

    evaluation = evaluate(result["model_name"], dataset_name="nslkdd", max_rows=500)
    assert evaluation["metrics"]["accuracy"] >= 0.0


def test_model_manager_and_api_endpoints():
    saved = save_model(
        model_name="xgboost",
        model=None,
        metrics={"accuracy": 0.5},
        metadata={"dataset": "nslkdd"},
        config={"model": "xgboost"},
    )
    assert saved["model_name"] == "xgboost"

    models = list_models()
    assert isinstance(models, list)

    response = client.post(
        "/api/v1/models/train",
        json={"model_name": "random_forest", "dataset_name": "nslkdd", "max_rows": 300},
    )
    assert response.status_code == 200

    response_models = client.get("/api/v1/models")
    assert response_models.status_code == 200

    predict_response = client.post(
        "/api/v1/models/random_forest/predict",
        json={"dataset_name": "nslkdd", "max_rows": 300},
    )
    assert predict_response.status_code == 200
