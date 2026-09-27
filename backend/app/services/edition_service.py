from typing import Protocol

from app.dao.interfaces.edition_dao import EditionDao
from app.domain.enums import Enums
from app.domain.exceptions import EditionNotFound
from app.domain.models.edition import Edition


class AuditLogger(Protocol):
    def record(
        self,
        *,
        action: str,
        entityType: str,
        entityId: str,
        actorId: str | None,
        metadata: dict[str, str],
    ) -> None: ...


class EditionService:
    """Orchestrates edition lifecycle changes and their audit records."""

    def __init__(self, editionDao: EditionDao, auditLogService: AuditLogger):
        self.editionDao = editionDao
        self.auditLogService = auditLogService

    def create(self, edition: Edition, actorId: str | None = None) -> Edition:
        """Create an edition, which opens it in its initial state."""
        if edition.status != Enums.EditionStatus.OPEN:
            raise ValueError("A new edition must have OPEN status.")

        createdEdition = self.editionDao.create(edition)
        self.auditLogService.record(
            action=Enums.AuditAction.OPEN_EDITION,
            entityType="Edition",
            entityId=createdEdition.editionId,
            actorId=actorId,
            metadata={"status": createdEdition.status},
        )
        return createdEdition

    def getById(self, editionId: str) -> Edition:
        edition = self.editionDao.getById(editionId)
        if edition is None:
            raise EditionNotFound(f"Edition with ID {editionId} not found.")
        return edition

    def changeTheme(
        self,
        editionId: str,
        newTheme: str,
        actorId: str | None = None,
    ) -> Edition:
        if not isinstance(newTheme, str) or not newTheme.strip():
            raise ValueError("newTheme must be a non-empty string.")

        edition = self.getById(editionId)
        previousTheme = edition.theme
        updatedTheme = newTheme.strip()
        self.editionDao.changeEditionTheme(edition, updatedTheme)
        edition.theme = updatedTheme
        self.auditLogService.record(
            action=Enums.AuditAction.CHANGE_EDITION_THEME,
            entityType="Edition",
            entityId=edition.editionId,
            actorId=actorId,
            metadata={"from": previousTheme, "to": updatedTheme},
        )
        return edition

    def close(self, editionId: str, actorId: str | None = None) -> Edition:
        edition = self.getById(editionId)
        if edition.status != Enums.EditionStatus.OPEN:
            return edition

        self.editionDao.close(edition.editionId)
        edition.status = Enums.EditionStatus.CLOSED
        self.auditLogService.record(
            action=Enums.AuditAction.CLOSE_EDITION,
            entityType="Edition",
            entityId=edition.editionId,
            actorId=actorId,
            metadata={
                "from": Enums.EditionStatus.OPEN,
                "to": Enums.EditionStatus.CLOSED,
            },
        )
        return edition
