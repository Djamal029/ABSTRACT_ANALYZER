# Interface AbstractDAO : persistance des metadonnees d'abstract.
from app.domain.models.abstract import Abstract


class AbstractDAO:
    def __init__(self, db):
        self.db = db

    def create(self, abstract: Abstract):
        pass

    def getById(self, abstractId: str) -> Abstract:
        pass

    def listByEdition(self, editionId: str) -> list[Abstract]:
        pass

    def updateStatus(self, abstractId: str, status: str):
        # Called by AbstractService/DuplicateDetectionService whenever the
        # workflow state changes (SUBMITTED -> FLAGGED_DUPLICATE -> ACCEPTED...).
        pass

    def updateRelevanceScore(self, abstractId: str, relevanceScore: float):
        # Called by RelevanceService right after computing the cosine
        # similarity against the edition's theme vector.
        pass
