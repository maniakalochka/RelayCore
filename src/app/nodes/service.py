import datetime
import uuid

from app.auth import User
from app.domain.policies import NodeAccessPolicy
from app.infrastructure.rabbitmq.publisher import NodePublisher
from app.nodes.healthcheck import NodeHealthCheckResult, NodeHealthCheckService
from app.nodes.models import Node, NodeCheck
from app.nodes.repository import NodeRepository
from app.nodes.schemas import NodeCreate


class NodeService:
    def __init__(
        self,
        repository: NodeRepository,
        health_check_service: NodeHealthCheckService,
        publisher: NodePublisher,
    ) -> None:
        self.repository = repository
        self.health_check_service = health_check_service
        self.publisher = publisher

    async def list_available_nodes(self) -> list[NodeCheck]:
        return await self.repository.list_available()

    async def check_node(self, node_id: uuid.UUID) -> NodeHealthCheckResult:
        node = await self.repository.get_by_id(node_id)

        result = await self.health_check_service.check_tcp(node.host, node.port)
        await self.repository.create_health_check(
            node_id=node_id,
            latency_ms=result.latency_ms,
            error=result.error,
            is_active=result.is_active,
            checked_at=datetime.datetime.now(),
        )

        return result

    async def create_node(self, data: NodeCreate) -> Node:
        node = await self.repository.create(data)
        await self.publisher.publish_health_check(node.id)
        return node

    async def get_node_by_id(self, user: User, node_id: uuid.UUID) -> Node:
        node = await self.repository.get_by_id(node_id)

        if not NodeAccessPolicy.can_access_node(user.role, node):
            raise PermissionError("User does not have permission to access this node.")

        return node
