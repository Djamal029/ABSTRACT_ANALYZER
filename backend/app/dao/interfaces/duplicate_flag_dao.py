# Interface DuplicateFlagDAO : persistance des doublons potentiels detectes.
from app.domain.models.duplicate_flag import DuplicateFlag


class DuplicateFlagDAO:
    def __init__(self, db):
        self.db = db

    def create(self, duplicateFlag: DuplicateFlag):
        pass

    def getById(self, duplicateFlagId: str) -> DuplicateFlag:
        pass

    def listPendingByEdition(self, editionId: str) -> list[DuplicateFlag]:
        pass

    def updateStatus(self, duplicateFlagId: str, status: str):
        # Called by AbstractService when an organizer confirms/rejects a flag.
        # Raises DuplicateAlreadyReviewed if status is no longer PENDING.
        pass
