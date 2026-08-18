from app.domain.models.edition import Edition


# Interface EditionDAO : CRUD des editions d'evenement.
class EditionDao:
    def __init__(self):
        pass

    def create(self, edition: Edition):
        pass

    def changeEditionTheme(self, edition: Edition, newTheme: str):
        pass

    def getById(self, editionId: str):
        pass

    def close(self, editionId: str):
        pass
