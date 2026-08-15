# Interface AbstractDAO : persistance des metadonnees d'abstract (CRUD, recherche par edition).
from backend.app.domain.models.abstract import Abstract


class AbstractDAO:
    def __init__(self, db):
        self.db = db

    def create(self, abstract: Abstract):
        pass

    def getById(self, abstractId: str) -> Abstract:
        pass

    def listEditionByID(self, editionID: str) -> list[Abstract]:
        pass