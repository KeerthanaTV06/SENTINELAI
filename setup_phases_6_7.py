import os

base_dir = "c:/Users/monis/OneDrive/Documents/Desktop/New folder/AICS/SENTINELAI"

files_to_create = {
    "backend/response/firewall.py": """import logging\nimport subprocess\n\nclass FirewallManager:\n    def block_ip(self, ip_address):\n        logging.warning(f"[ACTION] Blocking IP: {ip_address}")\n        # subprocess.run(["iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"])\n""",
    "backend/response/alert_router.py": """import logging\nfrom backend.response.firewall import FirewallManager\nfrom backend.response.audit_logger import AuditLogger\n\nclass AlertRouter:\n    def __init__(self):\n        self.firewall = FirewallManager()\n        self.audit = AuditLogger()\n\n    def route_alert(self, alert):\n        severity = alert.get('severity', 'LOW')\n        self.audit.log(alert)\n        if severity == 'CRITICAL':\n            self.firewall.block_ip(alert.get('src_ip'))\n        elif severity == 'HIGH':\n            logging.info("Sent to dashboard approval queue (HITL gate)")\n""",
    "backend/response/audit_logger.py": """import json\nfrom datetime import datetime\nimport os\n\nclass AuditLogger:\n    def __init__(self, log_file="audit.json"):\n        self.log_file = log_file\n\n    def log(self, action):\n        action['timestamp'] = datetime.utcnow().isoformat()\n        with open(self.log_file, "a") as f:\n            f.write(json.dumps(action) + "\\n")\n""",
    "docs/sdg_mapping.md": """# SDG Mapping\n\n- **SDG 3 (Good Health):** Securing healthcare networks from ransomware.\n- **SDG 9 (Industry, Innovation):** Resilient cyber infrastructure.\n- **SDG 11 (Sustainable Cities):** Protecting smart city IoT grids.\n- **SDG 16 (Peace, Justice):** Combating cybercrime.\n- **SDG 17 (Partnerships):** Cross-org federated threat intel sharing.\n""",
    "docs/architecture.md": """# Architecture\n\n```mermaid\ngraph TD;\n    A[Data Source] --> B(Kafka);\n    B --> C{Detectors};\n    C --> D[Elasticsearch];\n    C --> E[Response Engine];\n    D --> F[Dashboard];\n```\n""",
    "demo/run_demo.py": """import time\nimport logging\n\ndef run_demo():\n    logging.info("1. Normal traffic baseline...")\n    time.sleep(1)\n    logging.info("2. Injecting DoS attack wave...")\n    time.sleep(1)\n    logging.info("3. Detecting anomalies...")\n    time.sleep(1)\n    logging.info("4. Triggering SHAP explanations & Auto-blocking IP...")\n    logging.info("Demo complete.")\n\nif __name__ == '__main__':\n    run_demo()\n"""
}

for rel_path, content in files_to_create.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"Created {full_path}")
