# Implementation AuditLogDAO sur MySQL/Postgres (a coder). Append-only.
# Interface AuditLogDAO : ecriture/lecture de la trace d'audit. Append-only,
# aucune methode update/delete n'existe ici volontairement.

from app.domain.models.audit_log import AuditLog
from backend.app.dao.interfaces.audit_log_dao import AuditLogDAO
from backend.app.dao.relational.sqlalchemy_models import AuditLogModel


class AuditLogDAOImpl(AuditLogDAO):
    def __init__(self, db):
        self.db = db

    # From a SQLAlchemy row, create a domain AuditLog object.
    def _toDomain(self, row: AuditLogModel) -> AuditLog:
        return AuditLog(
            auditLogId=row.auditLogId,
            actorId=row.actorId,
            action=row.action,
            entityType=row.entityType,
            entityId=row.entityId,
            metadata=row.extraData,
            createdAt=row.createdAt
        )

    # Record a new AuditLog entry in the database. This is append-only.
    def record(self, auditLog: AuditLog):
        row = AuditLogModel(
            auditLogId=auditLog.auditLogId,
            actorId=auditLog.actorId,
            action=auditLog.action,
            entityType=auditLog.entityType,
            entityId=auditLog.entityId,
            extraData=auditLog.metadata,
            createdAt=auditLog.createdAt
        )
        self.db.add(row)
        self.db.flush()

    # List all AuditLog entries.
    def list(self) -> list[AuditLog]:
        rows = self.db.query(AuditLogModel).all()
        return [self._toDomain(row) for row in rows]

    # return all AuditLog entries for a given actor.
    def listByActor(self, actorId: str) -> list[AuditLog]:
        rows = self.db.query(AuditLogModel).filter_by(actorId=actorId).all()
        return [self._toDomain(row) for row in rows]

    # return all AuditLog entries for a given action (e.g. "SUBMIT_ABSTRACT", "REVIEW_DUPLICATE_FLAG").
    def listByAction(self, action: str) -> list[AuditLog]:
        rows = self.db.query(AuditLogModel).filter_by(action=action).all()
        return [self._toDomain(row) for row in rows]
