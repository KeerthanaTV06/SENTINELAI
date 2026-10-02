# Deployment Guide

This document describes how to run SENTINEL-AI in production using Docker Compose.

Prerequisites
- Docker Engine
- Docker Compose
- 8+ GB RAM recommended

Start production stack
1. Copy .env.example to .env and fill production values.
2. Build and start services:
   docker-compose -f docker-compose.prod.yml up --build -d

Services
- backend: FastAPI app exposed on port 8000
- frontend: Nginx serving built frontend on port 8080
- elasticsearch: port 9200
- kibana: port 5601
- kafka / zookeeper

Logs and volumes
- Logs are written to ./logs
- Models are persisted in ./models

Health checks
- Backend exposes /api/health
- Prometheus metrics at /metrics (if prometheus_client installed)

Security
- Ensure .env secrets are stored securely and not checked into source control.
- Configure allowed CORS origins in config.py or via environment variables.

Monitoring
- Configure Prometheus to scrape backend /metrics if enabled.

Updating
- Pull new code, then run docker-compose -f docker-compose.prod.yml up --build -d
