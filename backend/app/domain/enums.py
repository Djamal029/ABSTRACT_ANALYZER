# Enums metier (statut abstract, role utilisateur, statut d'edition...).
class Enums:
    class AbstractStatus:
        DRAFT = "DRAFT"
        SUBMITTED = "SUBMITTED"
        FLAGGED_DUPLICATE = "FLAGGED_DUPLICATE"
        ACCEPTED = "ACCEPTED"
        REJECTED = "REJECTED"
        WITHDRAWN = "WITHDRAWN"

    class UserRole:
        RESEARCHER = "RESEARCHER"
        ORGANIZER = "ORGANIZER"
        SUPERUSER = "SUPERUSER"

    class EditionStatus:
        OPEN = "OPEN"
        CLOSED = "CLOSED"
        CLUSTERED = "CLUSTERED"

    class AuditAction:
        SUBMIT_ABSTRACT = "SUBMIT_ABSTRACT"
        UPDATE_ABSTRACT_STATUS = "UPDATE_ABSTRACT_STATUS"
        REVIEW_DUPLICATE = "REVIEW_DUPLICATE"
        OPEN_EDITION = "OPEN_EDITION"
        CLOSE_EDITION = "CLOSE_EDITION"
        RUN_CLUSTERING = "RUN_CLUSTERING"
        LOGIN = "LOGIN"
        CREATE_USER = "CREATE_USER"
