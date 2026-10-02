"""Explainability service using SHAP with fallbacks.

Supports RandomForest, XGBoost (Booster or sklearn wrapper), and LogisticRegression.
Generates global and local explanations, saves plots and JSON under reports/shap/<model>.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json
import csv

import numpy as np

try:
    import shap
except Exception:  # shap may be optional in some environments
    shap = None  # type: ignore

import joblib

logger = logging.getLogger("sentinel.explainability")

REPORTS_DIR = Path.cwd() / "reports" / "shap"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


class ExplanationService:
    """Service that produces explanations for trained models.

    Models are expected to be saved in the repository `models/` directory with
    conventional names like `rf_model.joblib`, `xg_model.bst` or similar. This
    service loads models via joblib.load when possible.
    """

    def __init__(self, models_dir: Optional[Path] = None):
        self.models_dir = Path(models_dir) if models_dir else Path.cwd() / "models"
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def _model_path(self, name: str) -> Path:
        # Allow multiple extensions
        candidates = list(self.models_dir.glob(f"{name}*"))
        if not candidates:
            raise FileNotFoundError(f"Model {name} not found in {self.models_dir}")
        return candidates[0]

    def load_model(self, name: str) -> Any:
        path = self._model_path(name)
        logger.info("Loading model %s", path)
        try:
            if path.suffix in {".joblib", ".pkl"}:
                return joblib.load(path)
            elif path.suffix in {".bst", ".model"}:
                # xgboost native booster
                try:
                    import xgboost as xgb
                    booster = xgb.Booster()
                    booster.load_model(str(path))
                    return booster
                except Exception:
                    raise
            else:
                return joblib.load(path)
        except Exception as exc:
            logger.exception("Failed loading model %s: %s", name, exc)
            raise

    def feature_importance(self, name: str, feature_names: List[str], top_k: int = 20) -> Dict[str, Any]:
        """Compute and store feature importance for a model.

        If SHAP is available uses TreeExplainer or KernelExplainer; otherwise
        falls back to model.feature_importances_ or coefficients.
        """
        model = self.load_model(name)
        out_dir = REPORTS_DIR / name
        out_dir.mkdir(parents=True, exist_ok=True)

        importance: Dict[str, float] = {}

        # Try SHAP global importance if available and model supported
        try:
            if shap is not None:
                logger.info("Computing SHAP global importance for %s", name)
                # For tree models use TreeExplainer; for linear use LinearExplainer
                if hasattr(model, "feature_importances_") or model.__class__.__name__.lower().startswith("xgboost"):
                    expl = shap.TreeExplainer(model)  # type: ignore
                else:
                    expl = shap.Explainer(model)

                # Need to load training data or rely on model to accept an array
                # For global importance compute mean(|shap_values|) over a background
                # Here we attempt to use a small background sampled from model if available
                # Fallback: use zero background and rely on TreeExplainer
                try:
                    # If model has a training_data_ attribute, use it
                    background = getattr(model, "training_data_", None)
                    if background is None:
                        # otherwise try to use a default small background of zeros
                        background = np.zeros((1, len(feature_names)))
                    shap_values = expl.shap_values(background)
                    # shap_values may be list (multi-class) or array
                    if isinstance(shap_values, list):
                        arr = np.abs(np.vstack([np.mean(np.abs(sv), axis=0) for sv in shap_values]))
                        mean_vals = np.mean(arr, axis=0)
                    else:
                        mean_vals = np.mean(np.abs(shap_values), axis=0)
                    importance = {fn: float(v) for fn, v in zip(feature_names, mean_vals)}
                except Exception:
                    logger.exception("SHAP global computation failed, falling back")
                    importance = {}
        except Exception:
            logger.exception("SHAP not available or failed; using fallback importance")
            importance = {}

        # Fallbacks
        if not importance:
            # sklearn feature_importances_
            if hasattr(model, "feature_importances_"):
                vals = getattr(model, "feature_importances_")
                importance = {fn: float(v) for fn, v in zip(feature_names, vals)}
            elif hasattr(model, "coef_"):
                coef = getattr(model, "coef_")
                if coef.ndim == 1:
                    vals = np.abs(coef)
                else:
                    vals = np.mean(np.abs(coef), axis=0)
                importance = {fn: float(v) for fn, v in zip(feature_names, vals)}
            else:
                # As ultimate fallback set uniform importance
                importance = {fn: 0.0 for fn in feature_names}

        # Generate sorted ranking
        ranking = sorted(importance.items(), key=lambda kv: kv[1], reverse=True)

        # Save JSON and CSV
        fi_json = out_dir / "feature_importance.json"
        fi_csv = out_dir / "feature_importance.csv"
        with fi_json.open("w", encoding="utf-8") as f:
            json.dump({"ranking": ranking}, f, indent=2)
        with fi_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["feature", "importance"])
            for feat, val in ranking:
                writer.writerow([feat, val])

        # Also attempt to produce SHAP bar plot and summary if shap is available
        try:
            if shap is not None:
                logger.info("Generating SHAP plots for %s", name)
                # create dummy background
                expl = shap.Explainer(model)  # type: ignore
                background = np.zeros((1, len(feature_names)))
                shap_values = expl.shap_values(background)
                # summary plot
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                plt.figure()
                try:
                    shap.summary_plot(shap_values, features=background, feature_names=feature_names, show=False)
                    plt.tight_layout()
                    plt.savefig(out_dir / "shap_summary.png")
                    plt.close()
                except Exception:
                    logger.exception("Failed to create SHAP summary plot")
                # bar plot
                try:
                    plt.figure()
                    shap.plots.bar(shap_values, feature_names=feature_names, show=False)  # type: ignore
                    plt.tight_layout()
                    plt.savefig(out_dir / "shap_bar.png")
                    plt.close()
                except Exception:
                    logger.exception("Failed to create SHAP bar plot")
        except Exception:
            logger.exception("SHAP plotting failed or shap not installed")

        return {"ranking": ranking}

    def explain_prediction(self, name: str, feature_names: List[str], X: List[float]) -> Dict[str, Any]:
        """Explain a single prediction and return local feature contributions.

        Returns a dict containing prediction, probabilities (if available), and
        a list of (feature, contribution) sorted by absolute contribution.
        """
        model = self.load_model(name)
        arr = np.asarray(X).reshape(1, -1)

        # Get prediction and probabilities
        pred = None
        probs = None
        try:
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(arr).tolist()
                pred = int(np.argmax(probs[0]))
            else:
                pred = int(model.predict(arr)[0])
        except Exception:
            logger.exception("Model prediction failed")
            pred = None

        contributions: List[Tuple[str, float]] = []
        try:
            if shap is not None:
                logger.info("Computing SHAP local explanation for %s", name)
                # pick appropriate explainer
                if hasattr(model, "feature_importances_") or model.__class__.__name__.lower().startswith("xgboost"):
                    expl = shap.TreeExplainer(model)  # type: ignore
                else:
                    expl = shap.Explainer(model)
                shap_vals = expl.shap_values(arr)
                # shap_vals could be list for multiclass
                if isinstance(shap_vals, list):
                    sv = shap_vals[0][0]  # choose first class explanation
                else:
                    sv = shap_vals[0]
                contributions = [(fn, float(val)) for fn, val in zip(feature_names, sv.tolist())]
        except Exception:
            logger.exception("SHAP local explanation failed; falling back to simple attribution")
            # Fallback: use model.coef_ or feature_importances_
            if hasattr(model, "coef_"):
                coef = getattr(model, "coef_")
                if coef.ndim == 1:
                    vals = coef
                else:
                    vals = coef[0]
                contributions = [(fn, float(v * x)) for fn, v, x in zip(feature_names, vals, X)]
            elif hasattr(model, "feature_importances_"):
                vals = getattr(model, "feature_importances_")
                contributions = [(fn, float(v * x)) for fn, v, x in zip(feature_names, vals, X)]

        # Sort by absolute contribution
        contributions_sorted = sorted(contributions, key=lambda kv: abs(kv[1]), reverse=True)

        # Save explanation JSON
        out_dir = REPORTS_DIR / name
        out_dir.mkdir(parents=True, exist_ok=True)
        expl_json = out_dir / "explanation.json"
        with expl_json.open("w", encoding="utf-8") as f:
            json.dump({"prediction": pred, "probabilities": probs, "contributions": contributions_sorted}, f, indent=2)

        # Generate human-friendly reason summary
        reasons = [f"{feat} -> {val:.4f}" for feat, val in contributions_sorted[:5]]
        human = {"prediction": pred, "reasons": reasons}
        (out_dir / "explanation_human.txt").write_text("\n".join([str(h) for h in reasons]))

        return {"prediction": pred, "probabilities": probs, "contributions": contributions_sorted}

    def global_summary(self, name: str, feature_names: List[str]) -> Dict[str, Any]:
        """Wrapper to compute global summary (alias for feature_importance).
        Keeps API semantic clarity.
        """
        return self.feature_importance(name, feature_names)