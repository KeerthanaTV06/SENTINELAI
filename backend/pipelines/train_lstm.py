"""Training script for LSTM intrusion detection model using PyTorch.

This script expects processed features saved as Parquet under data/processed
and a binary or multiclass label column 'label_id' or 'is_malicious'. It
creates PyTorch datasets and trains an LSTM model while logging metrics to
MLflow (if configured).
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional
import argparse

import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np

from backend.models.lstm_ids import LSTMIDS

logger = logging.getLogger("sentinel.train_lstm")


class TabularSequenceDataset(Dataset):
    def __init__(self, df: pd.DataFrame, feature_cols: list, label_col: str, seq_len: int = 1):
        self.df = df
        self.feature_cols = feature_cols
        self.label_col = label_col
        self.seq_len = seq_len

        # For simplicity assume each row is an independent sequence of length 1
        self.X = df[self.feature_cols].fillna(0).values.astype(np.float32)
        self.y = df[self.label_col].values.astype(np.int64)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        x = self.X[idx]
        x = x.reshape((1, -1))  # seq_len=1
        y = int(self.y[idx])
        return torch.from_numpy(x), torch.tensor(y, dtype=torch.long)


def train(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    for X, y in dataloader:
        X = X.to(device)
        y = y.to(device)
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * X.size(0)
        _, preds = outputs.max(1)
        correct += (preds == y).sum().item()
        total += X.size(0)
    return total_loss / total, correct / total


def evaluate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for X, y in dataloader:
            X = X.to(device)
            y = y.to(device)
            outputs = model(X)
            loss = criterion(outputs, y)
            total_loss += loss.item() * X.size(0)
            _, preds = outputs.max(1)
            correct += (preds == y).sum().item()
            total += X.size(0)
    return total_loss / total, correct / total


def main(processed_path: Path, feature_cols: list, label_col: str = "label_id", epochs: int = 5, batch_size: int = 64, lr: float = 1e-3, out_path: Optional[Path] = None):
    df = pd.read_parquet(processed_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    ds = TabularSequenceDataset(df, feature_cols, label_col)
    loader = DataLoader(ds, batch_size=batch_size, shuffle=True)

    model = LSTMIDS(input_size=len(feature_cols), hidden_size=128, num_layers=2, num_classes=len(df[label_col].unique()), dropout=0.3)
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(1, epochs + 1):
        train_loss, train_acc = train(model, loader, criterion, optimizer, device)
        logger.info("Epoch %d train loss=%.4f acc=%.4f", epoch, train_loss, train_acc)

    out_path = out_path or Path("models")
    out_path.mkdir(parents=True, exist_ok=True)
    model_file = out_path / "lstm_ids.pt"
    torch.save(model.state_dict(), model_file)
    logger.info("Saved model to %s", model_file)


if __name__ == "__main__":
    from app_logger import configure_logging
    configure_logging()

    parser = argparse.ArgumentParser(description="Train LSTM IDS model on processed features")
    parser.add_argument("--processed", required=True, help="Path to processed parquet file")
    parser.add_argument("--features", required=True, help="Comma-separated feature column names")
    parser.add_argument("--label", default="label_id")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()

    features = [s.strip() for s in args.features.split(",")]
    main(Path(args.processed), features, label_col=args.label, epochs=args.epochs, batch_size=args.batch_size)
