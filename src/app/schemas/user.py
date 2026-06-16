import uuid

from fastapi_users import schemas as fu_schemas
from pydantic import ConfigDict

from app.schemas.utils import to_camel


class UserRead(fu_schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class UserCreate(fu_schemas.BaseUserCreate):
    first_name: str
    last_name: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class UserUpdate(fu_schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    is_active: bool

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
