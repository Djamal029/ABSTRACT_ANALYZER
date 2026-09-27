# Implementation UserDAO (SQLAlchemy, compatible MySQL/Postgres).
from app.dao.interfaces.user_dao import UserDao
from app.dao.relational.sqlalchemy_models import UserModel
from app.domain.exceptions import UserNotFound
from app.domain.models.user import User


class UserDaoImpl(UserDao):
    def __init__(self, db):
        self.db = db

    def create(self, user: User) -> User:
        row = UserModel(
            userId=user.userId,
            userEmail=user.userEmail,
            userFullName=user.userFullName,
            userRole=user.userRole,
            passwordHash=user.passwordHash,
            isActive="1" if user.isActive else "0",
            createdAt=user.createdAt,
        )
        self.db.add(row)
        self.db.flush()
        return user

    def getByEmail(self, email: str) -> User:
        row = self.db.query(UserModel).filter_by(userEmail=email).first()
        if row is None:
            raise UserNotFound(f"User with email {email} not found.")
        return self._toDomain(row)

    def getById(self, userId: str) -> User:
        row = self.db.query(UserModel).filter_by(userId=userId).first()
        if row is None:
            raise UserNotFound(f"User with ID {userId} not found.")
        return self._toDomain(row)

    def updatePassword(self, userId: str, newPasswordHash: str):
        row = self.db.query(UserModel).filter_by(userId=userId).first()
        if row is None:
            raise UserNotFound(f"User with ID {userId} not found.")
        row.passwordHash = newPasswordHash
        self.db.flush()

    def updateProfile(self, userId: str, fullName: str):
        row = self.db.query(UserModel).filter_by(userId=userId).first()
        if row is None:
            raise UserNotFound(f"User with ID {userId} not found.")
        row.userFullName = fullName
        self.db.flush()

    def deactivate(self, userId: str):
        row = self.db.query(UserModel).filter_by(userId=userId).first()
        if row is None:
            raise UserNotFound(f"User with ID {userId} not found.")
        row.isActive = "0"
        self.db.flush()

    def _toDomain(self, row: UserModel) -> User:
        return User(
            userId=row.userId,
            userEmail=row.userEmail,
            userFullName=row.userFullName,
            userRole=row.userRole,
            passwordHash=row.passwordHash,
            isActive=row.isActive == "1",
            createdAt=row.createdAt,
        )