from typing import Protocol
from uuid import uuid4
from datetime import datetime, timezone

from app.core.security import create_access_token, hash_password, verify_password
from app.dao.interfaces.user_dao import UserDao
from app.domain.enums import Enums
from app.domain.exceptions import (
    InvalidCredentials,
    UnauthorizedAction,
    UserAlreadyExists,
    UserNotFound,
)
from app.domain.models.user import User


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


class UserService:
    """Coordinates user registration, authentication, and deactivation."""

    def __init__(self, userDao: UserDao, auditLogService: AuditLogger):
        self.userDao = userDao
        self.auditLogService = auditLogService

    def register(
        self,
        email: str,
        fullName: str,
        password: str,
    ) -> User:
        normalizedEmail = self._normalizeEmail(email)
        normalizedName = self._validateFullName(fullName)
        self._validatePassword(password)

        try:
            self.userDao.getByEmail(normalizedEmail)
        except UserNotFound:
            pass
        else:
            raise UserAlreadyExists(
                f"An account with email {normalizedEmail} already exists."
            )

        user = User(
            userId=str(uuid4()),
            userEmail=normalizedEmail,
            userFullName=normalizedName,
            userRole=Enums.UserRole.RESEARCHER,
            passwordHash=hash_password(password),
            isActive=True,
            createdAt=datetime.now(timezone.utc),
        )
        createdUser = self.userDao.create(user)
        self.auditLogService.record(
            action=Enums.AuditAction.CREATE_USER,
            entityType="User",
            entityId=createdUser.userId,
            actorId=createdUser.userId,
            metadata={"role": createdUser.userRole},
        )
        return createdUser

    def login(self, email: str, password: str) -> dict[str, object]:
        normalizedEmail = self._normalizeEmail(email)
        if not isinstance(password, str) or not password:
            raise InvalidCredentials("Invalid email or password.")

        try:
            user = self.userDao.getByEmail(normalizedEmail)
        except UserNotFound as exc:
            raise InvalidCredentials("Invalid email or password.") from exc

        if not user.isActive or not verify_password(password, user.passwordHash):
            raise InvalidCredentials("Invalid email or password.")

        token = create_access_token(user.userId, user.userRole)
        self.auditLogService.record(
            action=Enums.AuditAction.LOGIN,
            entityType="User",
            entityId=user.userId,
            actorId=user.userId,
            metadata={},
        )
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "userId": user.userId,
                "email": user.userEmail,
                "fullName": user.userFullName,
                "role": user.userRole,
            },
        }

    def deactivate(
        self,
        userId: str,
        actorId: str,
    ) -> None:
        actor = self.userDao.getById(actorId)
        if (
            not actor.isActive
            or actor.userRole
            not in (Enums.UserRole.ORGANIZER, Enums.UserRole.SUPERUSER)
        ):
            raise UnauthorizedAction(
                "Only an active organizer or superuser can deactivate users."
            )

        user = self.userDao.getById(userId)
        if not user.isActive:
            return

        self.userDao.deactivate(userId)
        self.auditLogService.record(
            action=Enums.AuditAction.DEACTIVATE_USER,
            entityType="User",
            entityId=user.userId,
            actorId=actorId,
            metadata={"isActive": "false"},
        )

    @staticmethod
    def _normalizeEmail(email: str) -> str:
        if not isinstance(email, str):
            raise ValueError("email must be a valid email address.")
        normalizedEmail = email.strip().casefold()
        if (
            not normalizedEmail
            or "@" not in normalizedEmail
            or any(character.isspace() for character in normalizedEmail)
        ):
            raise ValueError("email must be a valid email address.")
        return normalizedEmail

    @staticmethod
    def _validateFullName(fullName: str) -> str:
        if not isinstance(fullName, str) or not fullName.strip():
            raise ValueError("fullName must be a non-empty string.")
        return fullName.strip()

    @staticmethod
    def _validatePassword(password: str) -> None:
        if not isinstance(password, str) or len(password) < 8:
            raise ValueError("password must contain at least 8 characters.")
        if len(password.encode("utf-8")) > 72:
            raise ValueError("password must not exceed 72 UTF-8 bytes.")
