"""Producer for PhishTank CSV into Kafka topic."""
from __future__ import annotations

import logging
from pathlib import Path
import csv

from backend.services.kafka_client import KafkaClient

logger = logging.getLogger("sentinel.phishing_producer")


class PhishingProducer:
    def __init__(self, csv_path: Path, topic: str = "phishing", broker: str = "localhost:9092") -> None:
        self.csv_path = csv_path
        self.kafka = KafkaClient(bootstrap_servers=broker)
        self.topic = topic

    def run(self) -> None:
        if not self.csv_path.exists():
            raise FileNotFoundError(self.csv_path)
        logger.info("Streaming PhishTank rows from %s to topic %s", self.csv_path, self.topic)
        with open(self.csv_path, newline="", encoding="utf-8", errors="ignore") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                self.kafka.send(self.topic, row)

    def close(self) -> None:
        self.kafka.close()


if __name__ == "__main__":
    import argparse
    from app_logger import configure_logging

    configure_logging()
    parser = argparse.ArgumentParser(description="Stream PhishTank CSV into Kafka topic")
    parser.add_argument("csv", help="Path to PhishTank CSV file")
    parser.add_argument("--topic", default="phishing")
    parser.add_argument("--broker", default="localhost:9092")
    args = parser.parse_args()

    p = PhishingProducer(Path(args.csv), topic=args.topic, broker=args.broker)
    try:
        p.run()
    finally:
        p.close()
