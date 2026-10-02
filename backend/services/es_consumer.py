"""Kafka consumer that writes messages to Elasticsearch.

This consumer subscribes to a topic and indexes incoming JSON messages into
Elasticsearch using the document API. It uses simple heuristics to choose the
index name based on topic.
"""
from __future__ import annotations

import logging
from typing import Optional
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch, helpers
import json

logger = logging.getLogger("sentinel.es_consumer")


class ESConsumer:
    def __init__(self, bootstrap_servers: str = "localhost:9092", es_hosts: Optional[list] = None, topic: str = "nslkdd", group_id: Optional[str] = None) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer: KafkaConsumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        es_hosts = es_hosts or [{"host": "localhost", "port": 9200}]
        self.es = Elasticsearch(hosts=es_hosts)

    def index_name_for_topic(self) -> str:
        return f"sentinel-{self.topic.lower()}"

    def run(self) -> None:
        index_name = self.index_name_for_topic()
        # ensure index exists
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, ignore=400)
        logger.info("Consuming from topic %s and indexing to %s", self.topic, index_name)
        for msg in self.consumer:
            try:
                doc = msg.value
                # Add optional metadata
                doc.setdefault("_topic", self.topic)
                doc.setdefault("_offset", msg.offset)
                # Prepare bulk action
                action = {"_index": index_name, "_source": doc}
                helpers.bulk(self.es, [action])
                logger.debug("Indexed doc offset=%s to index=%s", msg.offset, index_name)
            except Exception:
                logger.exception("Failed indexing message offset=%s", getattr(msg, "offset", None))

    def close(self) -> None:
        try:
            self.consumer.close()
        except Exception:
            logger.exception("Error closing Kafka consumer")


if __name__ == "__main__":
    import argparse
    from app_logger import configure_logging

    configure_logging()
    parser = argparse.ArgumentParser(description="Consume Kafka topic and index to Elasticsearch")
    parser.add_argument("topic", help="Kafka topic")
    parser.add_argument("--broker", default="localhost:9092")
    parser.add_argument("--es-host", default="http://localhost:9200")
    args = parser.parse_args()

    # Elastic hosts parsing
    es_host = args.es_host
    if es_host.startswith("http"):
        # allow simple http://host:port
        import urllib.parse as up
        p = up.urlparse(es_host)
        host = p.hostname or "localhost"
        port = int(p.port or 9200)
        hosts = [{"host": host, "port": port}]
    else:
        hosts = [{"host": "localhost", "port": 9200}]

    c = ESConsumer(bootstrap_servers=args.broker, es_hosts=hosts, topic=args.topic)
    try:
        c.run()
    finally:
        c.close()
