from typing import Any

from fastapi_users.authentication import JWTStrategy
from fastapi_users.jwt import generate_jwt

from app.core.config import settings
from app.models.user import User


class CustomJWTStrategy(JWTStrategy):  # type: ignore[type-arg]
    async def write_token(self, user: User) -> str:
        data: dict[str, Any] = {
            "sub": str(user.id),
            "aud": self.token_audience,
        }
        return generate_jwt(
            data,
            settings.JWT_SECRET,
            settings.ACCESS_TOKEN_LIFETIME_S,
            algorithm="HS256",
        )
