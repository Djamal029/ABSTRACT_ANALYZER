# Implementation DuplicateFlagDAO sur MySQL/Postgres (a coder).
# Interface DuplicateFlagDAO : persistance des doublons potentiels detectes.

from app.domain.models.duplicate_flag import DuplicateFlag
from backend.app.dao.interfaces.duplicate_flag_dao import DuplicateFlagDAO
from backend.app.dao.relational.sqlalchemy_models import DuplicateFlagModel
from backend.app.domain.exceptions import DuplicateAlreadyReviewed, DuplicateFlagNotFound


class DuplicateFlagDAOImpl(DuplicateFlagDAO):
    def __init__(self, db):
        self.db = db

    def create(self, duplicateFlag: DuplicateFlag) -> DuplicateFlag:
        row = DuplicateFlagModel(
            duplicateFlagId=duplicateFlag.duplicateFlagId,
            editionId=duplicateFlag.editionId,
            abstractId1=duplicateFlag.abstractId1,
            abstractId2=duplicateFlag.abstractId2,
            status=duplicateFlag.status,
            createdAt=duplicateFlag.createdAt,
        )
        self.db.add(row)
        self.db.flush()
        return duplicateFlag

    # Function to convert a DuplicateFlagModel to a DuplicateFlag domain object.
    def _toDomain(self, row: DuplicateFlagModel) -> DuplicateFlag:
        return DuplicateFlag(
            row.duplicateFlagId,
            row.editionId,
            row.abstractId1,
            row.abstractId2,
            row.status,
            row.createdAt,
        )

    def getById(self, duplicateFlagId: str) -> DuplicateFlag:
        row = (
            self.db.query(DuplicateFlagModel)
            .filter_by(duplicateFlagId=duplicateFlagId)
            .first()
        )
        if row is None:
            raise DuplicateFlagNotFound(f"DuplicateFlag {duplicateFlagId} not found.")
        return self._toDomain(row)

    def listPendingByEdition(self, editionId: str) -> list[DuplicateFlag]:
        # Returns all pending duplicate flags for a given edition.
        rows = (
                    self.db.query(DuplicateFlagModel)
                    .filter_by(editionId=editionId, status="PENDING")
                    .all()
                )
        return [self._toDomain(row) for row in rows]

    def updateStatus(self, duplicateFlagId: str, status: str):
        # Called by AbstractService when an organizer confirms/rejects a flag.
        # Raises DuplicateAlreadyReviewed if status is no longer PENDING.

        row = (
            self.db.query(DuplicateFlagModel)
            .filter_by(duplicateFlagId=duplicateFlagId)
            .first()
        )

        # If the row is not found, raise an exception (not implemented yet).
        if row is None:
            raise DuplicateFlagNotFound(duplicateFlagId)

        # If the status is no longer PENDING, raise an exception.
        if row.status != "PENDING":
            raise DuplicateAlreadyReviewed(duplicateFlagId, row.status)

        # Update the status and flush the changes to the database.
        row.status = status
        self.db.flush()
