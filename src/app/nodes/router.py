from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth import User
from app.auth.manager import current_active_user
from app.nodes.dependencies import get_node_service
from app.nodes.schemas import NodeCreate, NodeRead
from app.nodes.service import NodeService

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.get("/available", response_model=list[NodeRead])
async def list_available_nodes(
    service: Annotated[NodeService, Depends(get_node_service)],
    user: Annotated[User, Depends(current_active_user)],
) -> list[NodeRead]:
    nodes = await service.list_available_nodes(user)
    return [NodeRead.model_validate(node) for node in nodes]


@router.post("/create", response_model=NodeRead)
async def create_node(
    data: NodeCreate,
    service: Annotated[NodeService, Depends(get_node_service)],
    user: Annotated[User, Depends(current_active_user)],
) -> NodeRead:
    node = await service.create_node(data, user)
    return NodeRead.model_validate(node)
