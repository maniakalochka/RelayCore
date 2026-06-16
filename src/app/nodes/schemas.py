import uuid

from pydantic import BaseModel, ConfigDict


class NodeRead(BaseModel):
    id: uuid.UUID
    name: str
    host: str
    country_code: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
