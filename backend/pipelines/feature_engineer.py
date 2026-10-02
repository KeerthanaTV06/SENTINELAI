"""Feature engineering utilities for network traffic and threat events."""
from __future__ import annotations

import logging
import re
from typing import Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger("sentinel.feature_engineer")


def encode_protocol(df: pd.DataFrame, col: str = "protocol_type") -> pd.DataFrame:
    """One-hot encode a protocol column into numeric features."""
    frame = df.copy()
    if col not in frame.columns:
        return frame
    dummies = pd.get_dummies(frame[col].astype(str), prefix="proto")
    return pd.concat([frame, dummies], axis=1)


def compute_flow_duration(df: pd.DataFrame, start_col: str = "start_time", end_col: str = "end_time", out_col: str = "flow_duration") -> pd.DataFrame:
    """Compute flow duration if start and end timestamps are available."""
    frame = df.copy()
    if start_col in frame.columns and end_col in frame.columns:
        try:
            frame[out_col] = (pd.to_datetime(frame[end_col]) - pd.to_datetime(frame[start_col])).dt.total_seconds().astype(float)
        except Exception:
            logger.debug("Failed to compute flow duration, leaving NaN")
            frame[out_col] = np.nan
    else:
        frame[out_col] = np.nan
    return frame


def compute_entropy(series: pd.Series) -> float:
    """Compute Shannon entropy for a sequence of bytes or categorical values."""
    counts = series.value_counts(normalize=True)
    probs = counts.values
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs)) if len(probs) > 0 else 0.0


def add_entropy_feature(df: pd.DataFrame, cols: Tuple[str, ...], out_col: str = "entropy") -> pd.DataFrame:
    """Compute entropy across specified columns for each row and add as out_col."""
    frame = df.copy()
    if not all(col in frame.columns for col in cols):
        frame[out_col] = 0.0
        return frame

    def row_entropy(row: pd.Series) -> float:
        values = [str(row[col]) for col in cols if pd.notnull(row[col])]
        if not values:
            return 0.0
        return compute_entropy(pd.Series(values))

    frame[out_col] = frame.apply(row_entropy, axis=1)
    return frame


def binary_label(df: pd.DataFrame, label_col: str = "label", positive_values: Tuple[str, ...] = ("normal",)) -> pd.DataFrame:
    """Create a binary label column where normal -> 0 else 1."""
    frame = df.copy()
    if label_col not in frame.columns:
        frame["is_malicious"] = 1
        return frame
    frame["is_malicious"] = (~frame[label_col].astype(str).str.lower().isin([value.lower() for value in positive_values])).astype(int)
    return frame


def multi_class_label(df: pd.DataFrame, label_col: str = "label") -> pd.DataFrame:
    """Map string labels to integer classes."""
    frame = df.copy()
    if label_col not in frame.columns:
        frame["label_id"] = -1
        return frame
    frame["label_id"], _ = pd.factorize(frame[label_col].astype(str))
    return frame


def engineer_features(df: pd.DataFrame, dataset_name: str | None = None) -> pd.DataFrame:
    """Add dataset-specific derived features for intrusion and phishing datasets."""
    frame = df.copy()
    normalized_name = (dataset_name or "").lower().replace("-", "_")

    if normalized_name in {"nslkdd", "cicids2017", "nsl_kdd"}:
        if "src_bytes" in frame.columns and "dst_bytes" in frame.columns:
            frame["traffic_ratio"] = frame["src_bytes"] / (frame["dst_bytes"] + 1)
        if "count" in frame.columns and "srv_count" in frame.columns:
            frame["connection_rate"] = frame["count"] / (frame["srv_count"] + 1)
        if "count" in frame.columns and "duration" in frame.columns:
            frame["packet_rate"] = frame["count"] / (frame["duration"] + 1)
        if "src_bytes" in frame.columns and "count" in frame.columns:
            frame["average_packet_size"] = frame["src_bytes"] / (frame["count"] + 1)
        if "wrong_fragment" in frame.columns and "count" in frame.columns:
            frame["error_ratio"] = frame["wrong_fragment"] / (frame["count"] + 1)
        if "duration" in frame.columns and "count" in frame.columns:
            frame["session_duration"] = frame["duration"]
        frame = add_entropy_feature(frame, tuple([col for col in ["protocol_type", "service", "flag"] if col in frame.columns]), out_col="flow_entropy")
        frame["risk_score"] = frame["traffic_ratio"].fillna(0.0) + frame["connection_rate"].fillna(0.0) + frame["packet_rate"].fillna(0.0)

    if normalized_name == "phishtank" or "url" in frame.columns:
        if "url" in frame.columns:
            frame["url_length"] = frame["url"].astype(str).str.len()
            frame["url_entropy"] = frame["url"].astype(str).apply(lambda value: compute_entropy(pd.Series(list(value))))
            suspicious_keywords = ["login", "secure", "verify", "account", "update", "bank", "paypal"]
            frame["suspicious_keyword_score"] = frame["url"].astype(str).str.lower().apply(
                lambda value: sum(1 for keyword in suspicious_keywords if keyword in value)
            )
            frame["character_distribution"] = frame["url"].astype(str).apply(lambda value: len(set(value)) / max(len(value), 1))
            frame["subdomain_depth"] = frame["url"].astype(str).apply(lambda value: value.count(".") - 1)
            frame["digit_ratio"] = frame["url"].astype(str).apply(lambda value: sum(1 for char in value if char.isdigit()) / max(len(value), 1))
            frame["special_char_ratio"] = frame["url"].astype(str).apply(lambda value: sum(1 for char in value if not char.isalnum()) / max(len(value), 1))

    return frame
