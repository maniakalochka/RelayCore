from typing import Annotated

from fastapi import APIRouter, Depends

from app.nodes.dependencies import get_node_service
from app.nodes.schemas import NodeCreate, NodeRead
from app.nodes.service import NodeService

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.get("/available", response_model=list[NodeRead])
async def list_available_nodes(
    service: Annotated[NodeService, Depends(get_node_service)],
) -> list[NodeRead]:
    nodes = await service.list_available_nodes()
    return [NodeRead.model_validate(node) for node in nodes]


@router.post("/create", response_model=NodeRead)
async def create_node(
    data: NodeCreate,
    service: Annotated[NodeService, Depends(get_node_service)],
) -> NodeRead:
    node = await service.create_node(data)
    return NodeRead.model_validate(node)
