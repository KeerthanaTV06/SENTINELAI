from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
DATASETS_DIR = BASE_DIR / "datasets"
RAW_DIR = DATASETS_DIR / "raw"
PROCESSED_DIR = DATASETS_DIR / "processed"
METADATA_DIR = DATASETS_DIR / "metadata"


def ensure_dirs() -> None:
    for path in [RAW_DIR / "nsl_kdd", RAW_DIR / "cicids2017", RAW_DIR / "phishtank", PROCESSED_DIR, METADATA_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def make_nsl_kdd(path: Path) -> pd.DataFrame:
    labels = ["normal", "dos", "probe", "r2l", "u2r"]
    probs = [0.58, 0.25, 0.10, 0.05, 0.02]
    protocols = ["tcp", "udp", "icmp"]
    services = ["http", "ftp", "smtp", "ssh", "dns", "telnet", "pop3", "imap", "ftp_data"]
    flags = ["SF", "S0", "REJ", "RSTO", "RSTR", "SH"]

    rows: List[Dict[str, object]] = []
    for _ in range(10000):
        label = np.random.choice(labels, p=probs)
        if label == "normal":
            duration = max(0, int(np.random.exponential(2.5)))
            src_bytes = max(0, int(np.random.lognormal(mean=6.2, sigma=1.1)))
            dst_bytes = max(0, int(np.random.lognormal(mean=5.8, sigma=1.0)))
            count = max(0, int(np.random.poisson(20)))
            srv_count = max(0, int(np.random.poisson(15)))
            serror_rate = round(float(np.random.beta(1.2, 6.0)), 3)
            srv_serror_rate = round(float(np.random.beta(1.1, 6.0)), 3)
            same_srv_rate = round(float(np.random.beta(5.0, 1.5)), 3)
            logged_in = int(np.random.choice([0, 1], p=[0.2, 0.8]))
            land = 0
            wrong_fragment = 0
            urgent = 0
            hot = max(0, int(np.random.poisson(1)))
            num_failed_logins = 0
            num_compromised = max(0, int(np.random.poisson(0.2)))
            root_shell = 0
            su_attempted = 0
            num_root = max(0, int(np.random.poisson(0.2)))
            num_file_creations = max(0, int(np.random.poisson(0.1)))
            num_shells = 0
            num_access_files = max(0, int(np.random.poisson(0.1)))
            dst_host_count = max(0, int(np.random.poisson(35)))
            dst_host_srv_count = max(0, int(np.random.poisson(25)))
        else:
            duration = max(0, int(np.random.exponential(15)))
            src_bytes = max(0, int(np.random.lognormal(mean=4.5, sigma=1.4)))
            dst_bytes = max(0, int(np.random.lognormal(mean=3.1, sigma=1.8)))
            count = max(0, int(np.random.poisson(120)))
            srv_count = max(0, int(np.random.poisson(110)))
            serror_rate = round(float(np.random.beta(6.0, 1.2)), 3)
            srv_serror_rate = round(float(np.random.beta(6.0, 1.2)), 3)
            same_srv_rate = round(float(np.random.beta(1.2, 5.0)), 3)
            logged_in = int(np.random.choice([0, 1], p=[0.85, 0.15]))
            land = int(np.random.choice([0, 1], p=[0.99, 0.01]))
            wrong_fragment = int(np.random.choice([0, 1], p=[0.97, 0.03]))
            urgent = int(np.random.choice([0, 1], p=[0.97, 0.03]))
            hot = max(0, int(np.random.poisson(5)))
            num_failed_logins = max(0, int(np.random.poisson(0.6)))
            num_compromised = max(0, int(np.random.poisson(2)))
            root_shell = int(np.random.choice([0, 1], p=[0.98, 0.02]))
            su_attempted = int(np.random.choice([0, 1], p=[0.99, 0.01]))
            num_root = max(0, int(np.random.poisson(0.8)))
            num_file_creations = max(0, int(np.random.poisson(0.7)))
            num_shells = int(np.random.choice([0, 1], p=[0.98, 0.02]))
            num_access_files = max(0, int(np.random.poisson(0.5)))
            dst_host_count = max(0, int(np.random.poisson(12)))
            dst_host_srv_count = max(0, int(np.random.poisson(10)))

        rows.append(
            {
                "duration": duration,
                "protocol_type": np.random.choice(protocols),
                "service": np.random.choice(services),
                "flag": np.random.choice(flags),
                "src_bytes": src_bytes,
                "dst_bytes": dst_bytes,
                "land": land,
                "wrong_fragment": wrong_fragment,
                "urgent": urgent,
                "hot": hot,
                "num_failed_logins": num_failed_logins,
                "logged_in": logged_in,
                "num_compromised": num_compromised,
                "root_shell": root_shell,
                "su_attempted": su_attempted,
                "num_root": num_root,
                "num_file_creations": num_file_creations,
                "num_shells": num_shells,
                "num_access_files": num_access_files,
                "count": count,
                "srv_count": srv_count,
                "serror_rate": serror_rate,
                "srv_serror_rate": srv_serror_rate,
                "same_srv_rate": same_srv_rate,
                "dst_host_count": dst_host_count,
                "dst_host_srv_count": dst_host_srv_count,
                "label": label,
            }
        )

    frame = pd.DataFrame(rows)
    frame.to_csv(path, index=False)
    return frame


def make_cicids(path: Path) -> pd.DataFrame:
    labels = ["BENIGN", "DDoS", "DoS", "PortScan", "Bot", "BruteForce", "Infiltration"]
    probs = [0.60, 0.12, 0.10, 0.08, 0.05, 0.03, 0.02]
    rows: List[Dict[str, object]] = []
    for _ in range(10000):
        label = np.random.choice(labels, p=probs)
        if label == "BENIGN":
            flow_duration = max(0, int(np.random.exponential(1200)))
            total_fwd = max(0, int(np.random.poisson(20)))
            total_bwd = max(0, int(np.random.poisson(15)))
            flow_bytes = max(0.0, float(np.random.normal(12000, 4000)))
            flow_packets = max(0.0, float(np.random.normal(100, 20)))
            pkt_len_mean = max(0.0, float(np.random.normal(80, 18)))
            pkt_len_std = max(0.0, float(np.random.exponential(12)))
            fin = int(np.random.choice([0, 1], p=[0.95, 0.05]))
            syn = int(np.random.choice([0, 1], p=[0.95, 0.05]))
            ack = int(np.random.choice([0, 1], p=[0.95, 0.05]))
            avg_pkt_size = max(0.0, float(np.random.normal(70, 15)))
            flow_iat_mean = max(0.0, float(np.random.exponential(500)))
            dest_port = int(np.random.choice([80, 22, 443, 53, 21, 3389, 8080, 3306]))
            protocol = int(np.random.choice([6, 17, 1]))
        else:
            flow_duration = max(0, int(np.random.exponential(6000)))
            total_fwd = max(0, int(np.random.poisson(100)))
            total_bwd = max(0, int(np.random.poisson(90)))
            flow_bytes = max(0.0, float(np.random.normal(50000, 18000)))
            flow_packets = max(0.0, float(np.random.normal(300, 80)))
            pkt_len_mean = max(0.0, float(np.random.normal(120, 30)))
            pkt_len_std = max(0.0, float(np.random.exponential(30)))
            fin = int(np.random.choice([0, 1], p=[0.5, 0.5]))
            syn = int(np.random.choice([0, 1], p=[0.5, 0.5]))
            ack = int(np.random.choice([0, 1], p=[0.5, 0.5]))
            avg_pkt_size = max(0.0, float(np.random.normal(110, 25)))
            flow_iat_mean = max(0.0, float(np.random.exponential(2000)))
            dest_port = int(np.random.choice([80, 22, 443, 53, 21, 3389, 8080, 3306, 25]))
            protocol = int(np.random.choice([6, 17, 1]))

        rows.append(
            {
                "Flow Duration": flow_duration,
                "Total Fwd Packets": total_fwd,
                "Total Backward Packets": total_bwd,
                "Flow Bytes/s": flow_bytes,
                "Flow Packets/s": flow_packets,
                "Packet Length Mean": pkt_len_mean,
                "Packet Length Std": pkt_len_std,
                "FIN Flag Count": fin,
                "SYN Flag Count": syn,
                "ACK Flag Count": ack,
                "Average Packet Size": avg_pkt_size,
                "Flow IAT Mean": flow_iat_mean,
                "Destination Port": dest_port,
                "Protocol": protocol,
                "Label": label,
            }
        )

    frame = pd.DataFrame(rows)
    frame.to_csv(path, index=False)
    return frame


def make_phishing(path: Path) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for _ in range(10000):
        if random.random() < 0.70:
            label = "phishing"
            domain = random.choice(["paypal-secure", "office365-login", "amazon-support", "banking-update", "secure-login"])
            tld = random.choice(["com", "net", "info", "org"])
            path_fragment = random.choice(["/login", "/account", "/verify", "/update", "/reset"])
            url = f"https://{domain}-{random.randint(100, 999)}.{tld}{path_fragment}?id={random.randint(1000, 9999)}"
            has_ip = 0
            has_https = 1
            num_dots = 2
            num_hyphens = random.randint(1, 3)
            num_digits = random.randint(1, 4)
            has_at_symbol = 0
            has_double_slash = 0
            has_login_keyword = 1
            entropy = round(3.2 + random.random() * 1.6, 3)
        else:
            label = "legitimate"
            domain = random.choice(["example", "bankofamerica", "github", "microsoft", "netflix"])
            tld = random.choice(["com", "org", "edu", "net"])
            path_fragment = random.choice(["/docs", "/api/v1", "/about", "/products", "/support"])
            url = f"https://{domain}.{tld}{path_fragment}"
            has_ip = 0
            has_https = 1
            num_dots = 1
            num_hyphens = 0
            num_digits = 0
            has_at_symbol = 0
            has_double_slash = 0
            has_login_keyword = 0
            entropy = round(2.0 + random.random() * 1.2, 3)

        rows.append(
            {
                "url": url,
                "domain_length": len(domain),
                "path_length": len(path_fragment),
                "has_ip": has_ip,
                "has_https": has_https,
                "num_dots": num_dots,
                "num_hyphens": num_hyphens,
                "num_digits": num_digits,
                "has_at_symbol": has_at_symbol,
                "has_double_slash": has_double_slash,
                "has_login_keyword": has_login_keyword,
                "entropy": entropy,
                "label": label,
            }
        )

    frame = pd.DataFrame(rows)
    frame.to_csv(path, index=False)
    return frame


def validate_dataset(frame: pd.DataFrame, expected_columns: List[str], label_column: str) -> Dict[str, object]:
    missing_values = int(frame.isna().sum().sum())
    column_names_ok = list(frame.columns) == expected_columns
    dtypes_ok = all(pd.api.types.is_numeric_dtype(frame[col]) or pd.api.types.is_object_dtype(frame[col]) for col in frame.columns)
    labels = frame[label_column].dropna().astype(str)
    counts = labels.value_counts().to_dict()
    max_share = max(counts.values()) / max(1, sum(counts.values()))
    balanced = max_share < 0.7

    return {
        "missing_values": missing_values,
        "column_names_ok": column_names_ok,
        "dtypes_ok": dtypes_ok,
        "balanced_class_distribution": balanced,
        "label_distribution": counts,
    }


def preprocess_dataset(frame: pd.DataFrame, label_column: str, dataset_name: str) -> Dict[str, object]:
    working = frame.copy()
    working = working.replace({"?": None})
    working = working.fillna(method="ffill").fillna(method="bfill")

    categorical_columns = [col for col in working.columns if working[col].dtype == object and col != label_column]
    numeric_columns = [col for col in working.columns if col != label_column and col not in categorical_columns]

    for col in categorical_columns:
        working[col] = working[col].astype(str)

    encoded = pd.get_dummies(working, columns=categorical_columns, drop_first=True)
    feature_columns = [col for col in encoded.columns if col != label_column]
    X = encoded[feature_columns]
    y = encoded[label_column]

    X = X.astype(float)
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y.astype(str))

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    out_path = PROCESSED_DIR / f"{dataset_name}_processed.csv"
    pd.DataFrame(X_scaled, columns=feature_columns).to_csv(out_path, index=False)

    return {
        "processed_path": str(out_path),
        "feature_columns": feature_columns,
        "label_encoder_classes": label_encoder.classes_.tolist(),
        "train_shape": X_train.shape,
        "test_shape": X_test.shape,
    }


def build_metadata() -> List[Dict[str, object]]:
    nsl_df = pd.read_csv(RAW_DIR / "nsl_kdd" / "train.csv")
    cicids_df = pd.read_csv(RAW_DIR / "cicids2017" / "cicids.csv")
    phish_df = pd.read_csv(RAW_DIR / "phishtank" / "phishing_urls.csv")

    return [
        {
            "name": "nsl_kdd",
            "path": str(RAW_DIR / "nsl_kdd" / "train.csv"),
            "columns": nsl_df.columns.tolist(),
            "label_classes": sorted(nsl_df["label"].astype(str).unique().tolist()),
            "row_count": int(len(nsl_df)),
            "description": "Synthetic NSL-KDD style intrusion detection dataset for multiclass classification.",
        },
        {
            "name": "cicids2017",
            "path": str(RAW_DIR / "cicids2017" / "cicids.csv"),
            "columns": cicids_df.columns.tolist(),
            "label_classes": sorted(cicids_df["Label"].astype(str).unique().tolist()),
            "row_count": int(len(cicids_df)),
            "description": "Synthetic CICIDS2017 style network traffic dataset for attack classification.",
        },
        {
            "name": "phishtank",
            "path": str(RAW_DIR / "phishtank" / "phishing_urls.csv"),
            "columns": phish_df.columns.tolist(),
            "label_classes": sorted(phish_df["label"].astype(str).unique().tolist()),
            "row_count": int(len(phish_df)),
            "description": "Synthetic PhishTank style phishing URL dataset for binary classification.",
        },
    ]


def main() -> None:
    random.seed(42)
    np.random.seed(42)
    ensure_dirs()

    nsl_df = make_nsl_kdd(RAW_DIR / "nsl_kdd" / "train.csv")
    cicids_df = make_cicids(RAW_DIR / "cicids2017" / "cicids.csv")
    phish_df = make_phishing(RAW_DIR / "phishtank" / "phishing_urls.csv")

    report = {
        "datasets": {}
    }

    nsl_validation = validate_dataset(nsl_df, expected_columns=[
        "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent", "hot",
        "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
        "num_shells", "num_access_files", "count", "srv_count", "serror_rate", "srv_serror_rate", "same_srv_rate",
        "dst_host_count", "dst_host_srv_count", "label"
    ], label_column="label")
    cicids_validation = validate_dataset(cicids_df, expected_columns=[
        "Flow Duration", "Total Fwd Packets", "Total Backward Packets", "Flow Bytes/s", "Flow Packets/s",
        "Packet Length Mean", "Packet Length Std", "FIN Flag Count", "SYN Flag Count", "ACK Flag Count",
        "Average Packet Size", "Flow IAT Mean", "Destination Port", "Protocol", "Label"
    ], label_column="Label")
    phish_validation = validate_dataset(phish_df, expected_columns=[
        "url", "domain_length", "path_length", "has_ip", "has_https", "num_dots", "num_hyphens", "num_digits",
        "has_at_symbol", "has_double_slash", "has_login_keyword", "entropy", "label"
    ], label_column="label")

    report["datasets"]["nsl_kdd"] = nsl_validation
    report["datasets"]["cicids2017"] = cicids_validation
    report["datasets"]["phishtank"] = phish_validation

    for name, frame, label_column in [
        ("nsl_kdd", nsl_df, "label"),
        ("cicids2017", cicids_df, "Label"),
        ("phishtank", phish_df, "label"),
    ]:
        preprocess_dataset(frame, label_column, name)

    metadata = build_metadata()
    (METADATA_DIR / "dataset_info.json").write_text(json.dumps({"datasets": metadata}, indent=2), encoding="utf-8")
    (METADATA_DIR / "validation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("✓ Dataset paths")
    print(f"- {RAW_DIR / 'nsl_kdd' / 'train.csv'}")
    print(f"- {RAW_DIR / 'cicids2017' / 'cicids.csv'}")
    print(f"- {RAW_DIR / 'phishtank' / 'phishing_urls.csv'}")
    print("✓ Number of rows")
    print(f"- nsl_kdd: {len(nsl_df)}")
    print(f"- cicids2017: {len(cicids_df)}")
    print(f"- phishtank: {len(phish_df)}")
    print("✓ Label distribution")
    print(f"- nsl_kdd: {nsl_df['label'].value_counts().to_dict()}")
    print(f"- cicids2017: {cicids_df['Label'].value_counts().to_dict()}")
    print(f"- phishtank: {phish_df['label'].value_counts().to_dict()}")
    print("✓ Validation passed")


if __name__ == "__main__":
    main()
