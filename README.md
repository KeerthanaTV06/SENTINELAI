# SENTINEL-AI

SENTINEL-AI – Autonomous AI-Powered Cyber Threat Intelligence Platform

This repository contains the Day 1 scaffold for SENTINEL-AI. The goal for Day 1 is to create a production-ready project skeleton, configuration, Docker Compose stack for Kafka, Zookeeper, Elasticsearch and Kibana, and a minimal FastAPI service.

Directory layout and Day 1 deliverables are provided below. Subsequent days will add datasets, streaming producers/consumers, feature engineering, validation, model training, and experiment tracking.

Requirements
- Python 3.11
- Docker and Docker Compose

Quickstart (Day 1)
1. Copy `.env.example` to `.env` and adjust values as needed.
2. Start services:
   docker-compose up -d --build
3. Wait for Elasticsearch and Kafka to start, then run the FastAPI app (container will run it automatically):
   - App is available at http://localhost:8000
   - Kibana is available at http://localhost:5601
   - Elasticsearch at http://localhost:9200
   - Kafka broker: localhost:9092

Testing
- Run unit tests:
  python -m pytest -q

See docs/ for more details.
dir -Recurse *logging*