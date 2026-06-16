from app.nodes.models import Node
from app.nodes.repository import NodeRepository


class NodeService:
    def __init__(self, repository: NodeRepository) -> None:
        self.repository = repository

    async def list_available_nodes(self) -> list[Node]:
        return await self.repository.list_active()

    async def list_all_nodes(self) -> list[Node]:
        return await self.repository.list_all_nodes()
