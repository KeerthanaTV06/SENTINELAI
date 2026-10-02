FROM python:3.11-slim

# Create app user
RUN useradd --create-home sentinel
WORKDIR /home/sentinel/app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . /home/sentinel/app
RUN chown -R sentinel:sentinel /home/sentinel/app
USER sentinel

EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
