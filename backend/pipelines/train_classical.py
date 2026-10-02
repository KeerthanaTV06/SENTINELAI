"""Train RandomForest and XGBoost classifiers on processed features.

Saves models and logs metrics. Uses scikit-learn and xgboost APIs.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional
import argparse
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

import xgboost as xgb

logger = logging.getLogger("sentinel.train_classical")


def train_random_forest(X_train, y_train, n_estimators=100):
    clf = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1)
    clf.fit(X_train, y_train)
    return clf


def train_xgboost(X_train, y_train, num_round=100):
    dtrain = xgb.DMatrix(X_train, label=y_train)
    params = {"objective": "multi:softprob", "eval_metric": "mlogloss"}
    bst = xgb.train(params, dtrain, num_boost_round=num_round)
    return bst


def evaluate_model(estimator, X_test, y_test):
    if hasattr(estimator, "predict_proba"):
        y_pred = estimator.predict(X_test)
    else:
        # xgboost booster
        dtest = xgb.DMatrix(X_test)
        y_pred_prob = estimator.predict(dtest)
        y_pred = y_pred_prob.argmax(axis=1)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)
    return report, cm


def main(processed: Path, feature_cols: List[str], label_col: str = "label_id", out_dir: Optional[Path] = None):
    df = pd.read_parquet(processed)
    X = df[feature_cols].fillna(0).values
    y = df[label_col].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = train_random_forest(X_train, y_train)
    xg = train_xgboost(X_train, y_train)

    rf_report, rf_cm = evaluate_model(rf, X_test, y_test)
    xg_report, xg_cm = evaluate_model(xg, X_test, y_test)

    out_dir = out_dir or Path("models")
    out_dir.mkdir(parents=True, exist_ok=True)

    rf_path = out_dir / "rf_model.joblib"
    joblib.dump(rf, rf_path)
    xg_path = out_dir / "xg_model.bst"
    xgb.Booster.save_model(xg, str(xg_path)) if hasattr(xg, "save_model") else xg.save_model(str(xg_path))

    logger.info("Saved RandomForest to %s", rf_path)
    logger.info("Saved XGBoost to %s", xg_path)

    # Persist evaluation reports
    (out_dir / "rf_report.json").write_text(str(rf_report))
    (out_dir / "xg_report.json").write_text(str(xg_report))
    (out_dir / "rf_cm.txt").write_text(str(rf_cm.tolist()))
    (out_dir / "xg_cm.txt").write_text(str(xg_cm.tolist()))

    print("RandomForest report:", rf_report)
    print("XGBoost report:", xg_report)


if __name__ == "__main__":
    from app_logger import configure_logging
    configure_logging()

    parser = argparse.ArgumentParser(description="Train RF and XGBoost on processed features")
    parser.add_argument("--processed", required=True)
    parser.add_argument("--features", required=True)
    parser.add_argument("--label", default="label_id")
    args = parser.parse_args()

    features = [s.strip() for s in args.features.split(",")]
    main(Path(args.processed), features, label_col=args.label)
