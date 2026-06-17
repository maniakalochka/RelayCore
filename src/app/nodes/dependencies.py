from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_async_session
from app.nodes.healthcheck import NodeHealthCheckService
from app.nodes.repository import NodeRepository
from app.nodes.service import NodeService


def get_health_check_service() -> NodeHealthCheckService:
    return NodeHealthCheckService()


def get_node_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    health_check_service: Annotated[NodeHealthCheckService, Depends(get_health_check_service)],
) -> NodeService:
    repository = NodeRepository(session)
    return NodeService(repository, health_check_service)
