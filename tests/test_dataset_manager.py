"""Unit tests for dataset manager (Day 2).

These tests are lightweight and do not download large datasets. They ensure the
API surface of dataset_manager functions as expected.
"""
from backend.pipelines.dataset_manager import list_datasets, prepare_dataset
from pathlib import Path
import pytest


def test_list_datasets_contains_known_keys():
    names = list_datasets()
    assert "nslkdd" in names
    assert "cicids2017" in names
    assert "phishtank" in names


def test_prepare_dataset_uses_local_data_when_available():
    prepared_path = prepare_dataset("nslkdd")
    assert prepared_path.exists()


def test_prepare_dataset_unknown_raises():
    with pytest.raises(ValueError):
        prepare_dataset("nonexistent_dataset_key")
