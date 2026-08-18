# AuditLog entity: immutable trace of any action that changes state (who, what, when).
# Written once, never updated or deleted.
class AuditLog:
    def __init__(self, auditLogId, actorId, action, entityType, entityId, metadata, createdAt):
        self.auditLogId = auditLogId
        self.actorId = actorId  # None => system/job action (e.g. RUN_CLUSTERING), not a human
        self.action = action  # one of Enums.AuditAction
        self.entityType = entityType  # e.g. "Abstract", "Edition", "DuplicateFlag"
        self.entityId = entityId
        self.metadata = metadata  # free-form dict, e.g. {"from": "SUBMITTED", "to": "FLAGGED_DUPLICATE"}
        self.createdAt = createdAt
