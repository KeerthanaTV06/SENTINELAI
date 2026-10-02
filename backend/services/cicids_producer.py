"""Producer for CICIDS2017 CSV files into Kafka topic.

Handles directory of CSVs and streams them row-by-row.
"""
from __future__ import annotations

import logging
from pathlib import Path
import csv

from backend.services.kafka_client import KafkaClient

logger = logging.getLogger("sentinel.cicids_producer")


class CICIDSProducer:
    def __init__(self, dir_path: Path, topic: str = "cicids", broker: str = "localhost:9092") -> None:
        self.dir_path = dir_path
        self.kafka = KafkaClient(bootstrap_servers=broker)
        self.topic = topic

    def run(self) -> None:
        if not self.dir_path.exists() or not self.dir_path.is_dir():
            raise FileNotFoundError(self.dir_path)
        logger.info("Streaming CICIDS CSVs from %s to topic %s", self.dir_path, self.topic)
        for csv_file in sorted(self.dir_path.glob("*.csv")):
            logger.info("Streaming file %s", csv_file)
            with open(csv_file, newline="", encoding="utf-8", errors="ignore") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    self.kafka.send(self.topic, row)

    def close(self) -> None:
        self.kafka.close()


if __name__ == "__main__":
    import argparse
    from app_logger import configure_logging

    configure_logging()
    parser = argparse.ArgumentParser(description="Stream CICIDS2017 CSV directory into Kafka topic")
    parser.add_argument("dir", help="Directory containing CICIDS CSV files")
    parser.add_argument("--topic", default="cicids")
    parser.add_argument("--broker", default="localhost:9092")
    args = parser.parse_args()

    p = CICIDSProducer(Path(args.dir), topic=args.topic, broker=args.broker)
    try:
        p.run()
    finally:
        p.close()
