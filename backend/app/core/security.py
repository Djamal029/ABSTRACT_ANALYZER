# Authentication helpers shared by the user service and API dependencies.
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.domain.exceptions import InvalidCredentials

_passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string.")
    if len(password.encode("utf-8")) > 72:
        raise ValueError("password must not exceed 72 UTF-8 bytes.")
    return _passwordContext.hash(password)


def verify_password(password: str, passwordHash: str) -> bool:
    if not isinstance(password, str) or not isinstance(passwordHash, str):
        return False
    return _passwordContext.verify(password, passwordHash)


def create_access_token(
    subject: str,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:
    secretKey = settings.jwtSecretKey
    if not secretKey or len(secretKey.encode("utf-8")) < 32:
        raise RuntimeError("JWT_SECRET_KEY must be configured to issue tokens.")

    lifetime = expires_delta or timedelta(
        minutes=settings.accessTokenExpireMinutes
    )
    if lifetime.total_seconds() <= 0:
        raise ValueError("Access token lifetime must be positive.")
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "role": role,
        "iat": now,
        "exp": now + lifetime,
    }
    return jwt.encode(payload, secretKey, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    secretKey = settings.jwtSecretKey
    if not secretKey or len(secretKey.encode("utf-8")) < 32:
        raise RuntimeError("JWT_SECRET_KEY must be configured to verify tokens.")
    try:
        payload = jwt.decode(token, secretKey, algorithms=["HS256"])
    except JWTError as exc:
        raise InvalidCredentials("Invalid or expired access token.") from exc
    if not isinstance(payload.get("sub"), str):
        raise InvalidCredentials("Access token is missing its subject.")
    return payload
