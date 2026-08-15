# Entite Cluster : axe thematique issu du clustering post-cloture.
class Cluster:
    def __init__(self, clusterId, editionId, clusterName, clusterKeyWords, clusterEmbeddingId, status):
        self.clusterId = clusterId
        self.editionId = editionId
        self.clusterName = clusterName
        self.clusterKeyWords = clusterKeyWords
        self.clusterEmbeddingId = clusterEmbeddingId
        self.status = status
