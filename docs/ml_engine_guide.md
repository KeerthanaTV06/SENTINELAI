# ML Engine Guide

SENTINEL-AI now includes a lightweight machine-learning engine for cyber threat detection.

## Implemented models
- Random Forest
- XGBoost
- Isolation Forest
- Logistic Regression

## Workflow
1. Load and preprocess a dataset.
2. Split into train/validation/test subsets.
3. Train a selected model.
4. Save the artifact and metrics under models/trained/.
5. Evaluate and persist reports under reports/.
