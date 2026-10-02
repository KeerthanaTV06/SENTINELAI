# Architecture

```mermaid
graph TD;
    A[Data Source] --> B(Kafka);
    B --> C{Detectors};
    C --> D[Elasticsearch];
    C --> E[Response Engine];
    D --> F[Dashboard];
```
