import datetime
import uuid

from app.nodes.healthcheck import NodeHealthCheckResult, NodeHealthCheckService
from app.nodes.models import Node
from app.nodes.repository import NodeRepository


class NodeService:
    def __init__(
        self, repository: NodeRepository, health_check_service: NodeHealthCheckService
    ) -> None:
        self.repository = repository
        self.health_check_service = health_check_service

    async def list_available_nodes(self) -> list[Node]:
        return await self.repository.list_available()

    async def check_node(self, node_id: uuid.UUID) -> NodeHealthCheckResult:
        node = await self.repository.get_by_id(node_id)

        result = await self.health_check_service.check_tcp(node.host, node.port)
        await self.repository.update_health_status(
            node_id=node_id,
            is_active=result.is_active,
            latency_ms=result.latency_ms,
            health_check_error=result.error,
            last_checked_at=datetime.datetime.now(),
        )

        return result
