import logging
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.auth.backends import auth_backend
from app.auth.dependencies import get_user_db
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

log = logging.getLogger(__name__)


class UserManager(BaseUserManager[User, uuid.UUID]):  # type: ignore
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        log.warning("User %r has registered.", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        log.warning("User %r has forgot their password. Reset token: %r", user.id, token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        log.warning("Verification requested for user %r. Verification token: %r", user.id, token)

    def parse_id(
        self,
        value: str,
    ) -> uuid.UUID:
        return uuid.UUID(value)

    async def create(  # type: ignore[override]
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Request | None = None,
    ) -> User:
        return await super().create(user_create, safe=safe, request=request)

    async def update(  # type: ignore[override]
        self,
        user_update: UserUpdate,
        user: User,
        safe: bool = False,
        request: Request | None = None,
    ) -> User:
        return await super().update(user_update, user, safe=safe, request=request)


async def get_user_manager(user_db=Depends(get_user_db)) -> AsyncIterator[UserManager]:  # type: ignore[no-untyped-def]
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](  # type: ignore[type-var]
    get_user_manager, [auth_backend]
)

current_active_user = fastapi_users.current_user(active=True)


@asynccontextmanager
async def user_manager_context(
    user_db: SQLAlchemyUserDatabase[User, uuid.UUID] = Depends(get_user_db),  # type: ignore[type-var]
) -> AsyncIterator[UserManager]:
    yield UserManager(user_db)
