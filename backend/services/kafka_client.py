"""Kafka producer/consumer utilities using kafka-python.

Provides a simple wrapper around KafkaProducer and KafkaConsumer for use in
producers and consumers implemented in services/.
"""
from __future__ import annotations

import logging
from typing import Optional, Iterable, Any
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json

logger = logging.getLogger("sentinel.kafka")


class KafkaClient:
    """Lightweight Kafka client wrapper.

    This class intentionally keeps a minimal surface API that exposes send
    and consume generator methods.
    """

    def __init__(self, bootstrap_servers: str = "localhost:9092") -> None:
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def send(self, topic: str, value: dict, key: Optional[bytes] = None) -> None:
        """Send a JSON-serializable dict to topic.

        Exceptions are logged and re-raised as KafkaError.
        """
        try:
            fut = self.producer.send(topic, value=value, key=key)
            fut.get(timeout=10)
            logger.debug("Sent message to %s: %s", topic, value)
        except KafkaError:
            logger.exception("Failed to send message to %s", topic)
            raise

    def close(self) -> None:
        try:
            self.producer.flush()
            self.producer.close()
        except Exception:
            logger.exception("Error closing Kafka producer")


def create_consumer(topic: str, bootstrap_servers: str = "localhost:9092", group_id: Optional[str] = None) -> KafkaConsumer:
    """Create a KafkaConsumer subscribed to a single topic."""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=group_id,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    return consumer
