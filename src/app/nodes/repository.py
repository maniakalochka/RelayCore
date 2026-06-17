import datetime
import uuid

from sqlalchemy import select

from app.db.repository import BaseRepository
from app.nodes.models import Node


class NodeRepository(BaseRepository):
    async def list_available(self) -> list[Node]:
        stmt = select(Node).where(Node.is_active.is_(True)).order_by(Node.name)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, node_id: uuid.UUID) -> Node:
        stmt = select(Node).where(Node.id == node_id)
        result = await self.session.execute(stmt)
        node = result.scalars().one_or_none()

        if not node:
            raise ValueError(f"Node with id {node_id} not found")

        return node

    async def update_health_status(
        self,
        node_id: uuid.UUID,
        is_active: bool,
        latency_ms: int | None,
        health_check_error: str | None,
        last_checked_at: datetime.datetime | None,
    ) -> None:
        stmt = select(Node).where(Node.id == node_id)
        result = await self.session.execute(stmt)
        node = result.scalars().first()
        if node:
            node.is_active = is_active
            node.latency_ms = latency_ms
            node.health_check_error = health_check_error
            node.last_checked_at = last_checked_at
            await self.session.commit()
