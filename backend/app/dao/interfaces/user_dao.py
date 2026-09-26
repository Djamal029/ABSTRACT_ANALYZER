from app.domain.models.user import User


# Interface UserDAO : CRUD utilisateurs, authentification.
class UserDao:
    def __init__(self):
        pass

    def create(self, user: User) -> User:
        pass

    def getByEmail(self, email: str) -> User:
        pass

    def getById(self, userId: str) -> User:
        pass

    def updatePassword(self, userId: str, newPasswordHash: str) -> None:
        pass

    def updateProfile(self, userId: str, fullName: str) -> None:
        pass

    def deactivate(self, userId: str) -> None:
        # Soft delete: sets isActive = False. No hard delete, since
        # User is referenced by Abstract.authorId and AuditLog.actorId.
        pass
