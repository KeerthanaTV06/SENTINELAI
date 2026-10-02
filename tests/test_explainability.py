"""Tests for explainability features.

Tests are designed to run without SHAP installed by mocking where appropriate.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

# helpers to create fake model artifacts
class FakeModel:
    def __init__(self, feature_importances=None, coef=None):
        self.feature_importances_ = feature_importances
        self.coef_ = coef
    def predict(self, X):
        return [0 for _ in range(len(X))]
    def predict_proba(self, X):
        return [[0.7, 0.3] for _ in range(len(X))]


@pytest.fixture()
def create_fake_model(tmp_path, monkeypatch):
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    # create a fake model file
    model_file = models_dir / "rf_model.joblib"
    # monkeypatch joblib.load to return FakeModel
    import joblib
    monkeypatch.setattr(joblib, "load", lambda p: FakeModel(feature_importances=[0.6, 0.4]))
    # create features JSON
    features_json = models_dir / "rf_model.features.json"
    features_json.write_text(json.dumps(["f1", "f2"]))
    yield
    # cleanup
    try:
        for f in models_dir.glob("*"):
            f.unlink()
        models_dir.rmdir()
    except Exception:
        pass


def test_feature_importance_api(create_fake_model):
    client = TestClient(app)
    resp = client.get("/api/v1/models/rf_model/importance")
    assert resp.status_code == 200
    j = resp.json()
    assert "ranking" in j
    assert isinstance(j["ranking"], list)
    assert j["ranking"][0][0] in ("f1", "f2")


def test_explain_api(create_fake_model):
    client = TestClient(app)
    body = {"features": [1.0, 2.0], "feature_names": ["f1", "f2"]}
    resp = client.post("/api/v1/models/rf_model/explain", json=body)
    assert resp.status_code == 200
    j = resp.json()
    assert "prediction" in j
    assert "contributions" in j


def test_summary_api(create_fake_model):
    client = TestClient(app)
    resp = client.get("/api/v1/models/rf_model/summary")
    assert resp.status_code == 200
    j = resp.json()
    assert "ranking" in j


def test_features_api(create_fake_model):
    client = TestClient(app)
    resp = client.get("/api/v1/models/rf_model/features")
    assert resp.status_code == 200
    j = resp.json()
    assert j["features"] == ["f1", "f2"]
