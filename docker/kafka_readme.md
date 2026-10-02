Kafka and Zookeeper are provided through Bitnami images in docker-compose.yml. Important notes:

- Zookeeper runs on port 2181
- Kafka broker is exposed on 9092
- For external clients use the broker address configured in KAFKA_CFG_ADVERTISED_LISTENERS

If using local tooling to produce/consume messages, ensure the broker address in your client matches the docker host address (e.g., localhost:9092) and that listeners/advertised listeners are configured appropriately.
