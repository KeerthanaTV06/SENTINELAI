import json
from datetime import datetime
import os

class AuditLogger:
    def __init__(self, log_file="audit.json"):
        self.log_file = log_file

    def log(self, action):
        action['timestamp'] = datetime.utcnow().isoformat()
        with open(self.log_file, "a") as f:
            f.write(json.dumps(action) + "\n")
