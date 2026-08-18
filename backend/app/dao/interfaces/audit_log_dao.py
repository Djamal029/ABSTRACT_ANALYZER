# Interface AuditLogDAO : ecriture/lecture de la trace d'audit. Append-only,
# aucune methode update/delete n'existe ici volontairement.
from app.domain.models.audit_log import AuditLog


class AuditLogDAO:
    def __init__(self, db):
        self.db = db

    def record(self, auditLog: AuditLog):
        pass

    def list(self) -> list[AuditLog]:
        pass
