# Interface ClusterDAO : persistance des resultats de clustering par edition.
from backend.app.domain.models.cluster import Cluster


class ClusterDAO:
    def __init__(self, db):
        self.db = db

    def saveClusters(self, editionId: str, clusters: list[Cluster]):
        # Persists all clusters produced by a single clustering run as one
        # atomic operation (replaces any previous run's clusters for this edition).
        pass

    def deleteByEdition(self, editionId: str):
        # Removes all clusters for an edition. Called before saveClusters()
        # when a clustering run is re-triggered, so listByEdition() never
        # mixes clusters from two different runs.
        pass

    def listByEdition(self, editionId: str) -> list[Cluster]:
        pass