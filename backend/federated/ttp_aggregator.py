class TTPAggregator:
    def aggregate(self, embeddings):
        return [sum(x)/len(x) for x in zip(*embeddings)]
