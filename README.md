# SENTINEL-AI 🛡️

[![CI Status](https://img.shields.io/badge/CI-passing-success)](#)
[![Python Version](https://img.shields.io/badge/python-3.11-blue)](#)
[![License](https://img.shields.io/badge/license-MIT-green)](#)
[![MLflow](https://img.shields.io/badge/MLflow-v2.0-blue)](#)

**SENTINEL-AI** is a production-grade, end-to-end Artificial Intelligence system designed for modern Cyber Security. Built over a 30-day solo development sprint, it integrates multiple Deep Learning models, Privacy-Preserving Federated Learning, Explainable AI (XAI), and Autonomous Response mechanisms into a single, cohesive platform.

This project directly supports the **UN's Sustainable Development Goals (SDGs)**, specifically SDG 3 (Healthcare Security), SDG 9 (Resilient Infrastructure), SDG 11 (Smart City IoT Protection), SDG 16 (Combating Cybercrime), and SDG 17 (Cross-Organization Partnerships via Federated Threat Sharing).

---

## 🏗️ System Architecture

SENTINEL-AI utilizes a microservices architecture that handles high-throughput data ingestion, real-time ML inference, and automated threat mitigation.

```mermaid
graph TD;
    A[Data Ingestion (Kafka Producers)] --> B(Kafka Brokers);
    B --> C{Core ML Detectors};
    C --> D[Elasticsearch / Kibana];
    C --> E[Autonomous Response Engine];
    D --> F[React Dashboard (XAI)];
    G[Federated Learning Engine] -.-> C;
    H[MLOps CI/CD Pipeline] -.-> C;
```

### Core Components
1. **Data Pipeline**: Real-time event streaming designed around Apache Kafka and Elasticsearch.
2. **Inference Backend**: A high-performance FastAPI server wrapping the machine learning models.
3. **Frontend Dashboard**: A sleek, modern React/Vite web application providing:
   - **Live Threat Monitoring**: SHAP-based model explainability dashboards (LSTM, CNN, XGBoost).
   - **Inference Board**: Live testing environment for manual predictions against deployed models.
   - **Datasets Board**: Centralized view of training/testing datasets with size and status monitoring.
   - **Connection Board**: Real-time infrastructure monitoring showing uptime, latency, and system activity logs.
4. **Response Engine**: An automated script wrapping OS-level firewall commands (e.g., `iptables`) to instantly drop malicious connections with a Human-in-the-Loop (HITL) approval gate for high-severity alerts.

---
## 🧠 Machine Learning Models & Datasets

SENTINEL-AI utilizes an ensemble of state-of-the-art models targeting specific threat vectors:

### 1. Network Intrusion Detection (LSTM)
*   **Architecture**: 2-layer Long Short-Term Memory (LSTM) network in PyTorch.
*   **Dataset**: NSL-KDD (sequence data using 10-timestep sliding windows).
*   **Purpose**: Detects multi-stage network attacks (DoS, Probe, U2R, R2L) by analyzing temporal patterns in network flows.

### 2. Malware Classification (1D-CNN)
*   **Architecture**: 1D Convolutional Neural Network (PyTorch).
*   **Dataset**: EMBER dataset (Portable Executable headers and section entropy).
*   **Purpose**: Extracts spatial features from raw PE files to definitively classify binaries as benign or malicious.

### 3. Phishing URL Detection (Random Forest + XGBoost)
*   **Architecture**: Ensemble trees (scikit-learn / xgboost).
*   **Dataset**: PhishTank URLs (enriched with VirusTotal API).
*   **Purpose**: Analyzes 30+ lexical features (entropy, subdomains, HTTPS usage) to detect zero-day phishing links.

### 4. Zero-Day Anomaly Detection (Autoencoder)
*   **Architecture**: Unsupervised PyTorch Autoencoder.
*   **Dataset**: CICIDS2017 (Normal traffic baseline).
*   **Purpose**: Flags novel, never-before-seen zero-day attacks by calculating reconstruction errors on live network streams.

---

## 🌐 Federated Learning Engine (Cross-Org Intel Sharing)

To comply with data privacy regulations (GDPR/HIPAA), SENTINEL-AI implements **Federated Learning** using the `Flower (flwr)` framework.
*   **Decentralized Training**: Models train locally on individual organization servers. Only aggregated weight updates are sent to the central server via the `FedAvg` algorithm.
*   **Differential Privacy**: Integrated with Facebook's `Opacus` library, Gaussian noise is injected into gradients to guarantee individual data points cannot be reconstructed (Epsilon-Delta DP).
*   **TTP Sharing**: Detected attacks are mapped to MITRE ATT&CK embeddings and shared anonymously across the network to provide global herd immunity against zero-day threats.

---

## ⚙️ MLOps & CI/CD Pipeline

The project implements full-scale MLOps to ensure the models remain accurate over time:
*   **Experiment Tracking**: All models are logged, versioned, and stored in the **MLflow Model Registry**.
*   **Automated Model Promotion**: Challenger models are evaluated against Champion models. If the Challenger's F1 score is `> 0.005` higher, it is automatically promoted to Production.
*   **Drift Detection**: Integrated with **Evidently AI** to calculate the Population Stability Index (PSI). If distribution drift is detected in live traffic, an automated Kafka signal triggers a retraining job.
*   **CI/CD**: GitHub Actions workflows run `pytest` and linting, while local deployments use Kubernetes (`minikube`) with HPA auto-scaling.

---

## 🚀 Quickstart

To spin up the standalone infrastructure (FastAPI Backend, React Dashboard, Elasticsearch) locally:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
*(Note: The first build pulls heavy ML libraries and takes ~10 minutes. Subsequent boots are nearly instant).*

### 🔗 Localhost Access Links
- **Web UI (React Dashboard):** [http://localhost:8080](http://localhost:8080)
- **FastAPI Backend (Swagger API Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Kibana (Data Exploration):** [http://localhost:5601](http://localhost:5601)

### 🎥 Running the Live Demo
To trigger the automated attack simulation and test the Autonomous Response Engine:
```bash
python demo/run_demo.py
```