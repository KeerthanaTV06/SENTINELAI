"""Producer for NSL-KDD dataset rows into Kafka topic.

Reads CSV rows and publishes each row as a JSON message to a configured topic.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional
import csv

from backend.services.kafka_client import KafkaClient

logger = logging.getLogger("sentinel.nslkdd_producer")


class NSLKDDProducer:
    def __init__(self, csv_path: Path, topic: str = "nslkdd", broker: str = "localhost:9092") -> None:
        self.csv_path = csv_path
        self.kafka = KafkaClient(bootstrap_servers=broker)
        self.topic = topic

    def run(self) -> None:
        if not self.csv_path.exists():
            raise FileNotFoundError(self.csv_path)
        logger.info("Streaming NSL-KDD rows from %s to topic %s", self.csv_path, self.topic)
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

    parser = argparse.ArgumentParser(description="Stream NSL-KDD CSV into Kafka topic")
    parser.add_argument("csv", help="Path to NSL-KDD CSV file")
    parser.add_argument("--topic", default="nslkdd")
    parser.add_argument("--broker", default="localhost:9092")
    args = parser.parse_args()

    p = NSLKDDProducer(Path(args.csv), topic=args.topic, broker=args.broker)
    try:
        p.run()
    finally:
        p.close()
