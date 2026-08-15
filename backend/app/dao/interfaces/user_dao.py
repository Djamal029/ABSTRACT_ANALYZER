from backend.app.domain.models.user import User
# Interface UserDAO : CRUD utilisateurs, authentification.
class UserDao:
    def __init__(self):
        pass

    def create(self, user: User):
        pass

    def getByEmail(self, email: str):
        pass

    def updatePassword(self, userId: str, newPasswordHash: str):
            pass

    def updateProfile(self, userId: str, fullName: str):
        pass

    def deactivate(self, userId: str):
        # Soft delete: sets isActive = False. No hard delete, since
        # User is referenced by Abstract.authorId and AuditLog.actorId.
        pass