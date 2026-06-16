from typing import Annotated

from fastapi import APIRouter, Depends

from app.nodes.dependencies import get_node_service
from app.nodes.schemas import NodeRead
from app.nodes.service import NodeService

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.get("", response_model=list[NodeRead])
async def list_all_nodes(
    service: Annotated[NodeService, Depends(get_node_service)],
) -> list[NodeRead]:
    nodes = await service.list_all_nodes()
    return [NodeRead.model_validate(node) for node in nodes]


@router.get("available", response_model=list[NodeRead])
async def list_available_nodes(
    service: Annotated[NodeService, Depends(get_node_service)],
) -> list[NodeRead]:
    nodes = await service.list_available_nodes()
    return [NodeRead.model_validate(node) for node in nodes]
