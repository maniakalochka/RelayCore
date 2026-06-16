from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_async_session
from app.nodes.repository import NodeRepository
from app.nodes.service import NodeService


def get_node_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> NodeService:
    repository = NodeRepository(session)
    return NodeService(repository)
