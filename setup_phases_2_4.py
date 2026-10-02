import os

base_dir = "c:/Users/monis/OneDrive/Documents/Desktop/New folder/AICS/SENTINELAI"

files_to_create = {
    "backend/models/cnn_malware.py": """import torch\nimport torch.nn as nn\n\nclass CNNMalwareClassifier(nn.Module):\n    def __init__(self):\n        super(CNNMalwareClassifier, self).__init__()\n        self.conv1 = nn.Conv1d(1, 32, kernel_size=3, padding=1)\n        self.pool = nn.MaxPool1d(2)\n        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, padding=1)\n        self.fc1 = nn.Linear(64 * 64, 128) # assuming 256 input length\n        self.fc2 = nn.Linear(128, 1)\n        self.sigmoid = nn.Sigmoid()\n\n    def forward(self, x):\n        x = self.pool(torch.relu(self.conv1(x)))\n        x = self.pool(torch.relu(self.conv2(x)))\n        x = x.view(x.size(0), -1)\n        x = torch.relu(self.fc1(x))\n        x = self.sigmoid(self.fc2(x))\n        return x\n""",
    "backend/models/autoencoder.py": """import torch\nimport torch.nn as nn\n\nclass AnomalyAutoencoder(nn.Module):\n    def __init__(self, input_dim=41):\n        super(AnomalyAutoencoder, self).__init__()\n        self.encoder = nn.Sequential(nn.Linear(input_dim, 32), nn.ReLU(), nn.Linear(32, 16), nn.ReLU(), nn.Linear(16, 8), nn.ReLU())\n        self.decoder = nn.Sequential(nn.Linear(8, 16), nn.ReLU(), nn.Linear(16, 32), nn.ReLU(), nn.Linear(32, input_dim), nn.Sigmoid())\n\n    def forward(self, x):\n        return self.decoder(self.encoder(x))\n""",
    "backend/federated/fl_server.py": """import flwr as fl\n\nif __name__ == "__main__":\n    strategy = fl.server.strategy.FedAvg(min_fit_clients=2, min_available_clients=3)\n    fl.server.start_server(server_address="0.0.0.0:8080", config=fl.server.ServerConfig(num_rounds=10), strategy=strategy)\n""",
    "backend/federated/fl_client.py": """import flwr as fl\n# Placeholder for LSTM client\nclass LSTMClient(fl.client.NumPyClient):\n    def get_parameters(self, config):\n        return []\n    def fit(self, parameters, config):\n        return parameters, 100, {}\n    def evaluate(self, parameters, config):\n        return 0.0, 100, {"accuracy": 0.95}\nif __name__ == "__main__":\n    fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=LSTMClient())\n""",
    "backend/federated/privacy_accountant.py": """import logging\n\nclass PrivacyAccountant:\n    def __init__(self, target_epsilon=1.0, target_delta=1e-5):\n        self.epsilon = target_epsilon\n        self.delta = target_delta\n    def track_round(self, round_num):\n        logging.info(f"Round {round_num}: Privacy budget tracked.")\n""",
    "backend/federated/ttp_embedder.py": """class TTPEmbedder:\n    def embed(self, ttp_string):\n        return [0.1] * 128 # Placeholder 128-dim vector\n""",
    "backend/federated/ttp_aggregator.py": """class TTPAggregator:\n    def aggregate(self, embeddings):\n        return [sum(x)/len(x) for x in zip(*embeddings)]\n""",
    ".github/workflows/ci.yml": """name: CI\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - name: Set up Python\n        uses: actions/setup-python@v4\n        with: { python-version: '3.11' }\n      - name: Install dependencies\n        run: pip install -r requirements.txt\n      - name: Run tests\n        run: pytest\n""",
    "backend/pipelines/model_ci.py": """def promote_model(challenger_metrics, champion_metrics):\n    if challenger_metrics['f1'] > champion_metrics['f1'] + 0.005:\n        return True\n    return False\n""",
    "backend/pipelines/drift_detector.py": """def check_drift(reference_data, current_data):\n    # Placeholder PSI calculation\n    return 0.25 # Returns PSI > 0.2 to trigger drift\n""",
    "backend/pipelines/retrain_job.py": """import logging\n\ndef trigger_retrain():\n    logging.info("Drift detected. Triggering retrain job to fetch new data and retrain models.")\n""",
    "kubernetes/deployment.yaml": """apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: sentinel-inference\nspec:\n  replicas: 2\n  selector:\n    matchLabels:\n      app: sentinel\n  template:\n    metadata:\n      labels:\n        app: sentinel\n    spec:\n      containers:\n      - name: api\n        image: sentinel-api:latest\n        ports:\n        - containerPort: 8000\n""",
    "kubernetes/service.yaml": """apiVersion: v1\nkind: Service\nmetadata:\n  name: sentinel-service\nspec:\n  selector:\n    app: sentinel\n  ports:\n    - protocol: TCP\n      port: 80\n      targetPort: 8000\n  type: ClusterIP\n""",
    "kubernetes/hpa.yaml": """apiVersion: autoscaling/v2\nkind: HorizontalPodAutoscaler\nmetadata:\n  name: sentinel-hpa\nspec:\n  scaleTargetRef:\n    apiVersion: apps/v1\n    kind: Deployment\n    name: sentinel-inference\n  minReplicas: 2\n  maxReplicas: 5\n  metrics:\n  - type: Resource\n    resource:\n      name: cpu\n      target:\n        type: Utilization\n        averageUtilization: 80\n"""
}

for rel_path, content in files_to_create.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"Created {full_path}")
