import datetime
import uuid

from sqlalchemy import select

from app.db.repository import BaseRepository
from app.nodes.models import Node, NodeCheck


class NodeRepository(BaseRepository):
    async def list_available(self) -> list[NodeCheck]:
        stmt = select(NodeCheck).where(NodeCheck.is_active.is_(True)).order_by(Node.name)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, node_id: uuid.UUID) -> Node:
        stmt = select(Node).where(Node.id == node_id)
        result = await self.session.execute(stmt)
        node = result.scalars().one_or_none()

        if not node:
            raise ValueError(f"Node with id {node_id} not found")

        return node

    async def create_health_check(
        self,
        node_id: uuid.UUID,
        is_active: bool,
        latency_ms: int | None,
        error: str | None,
        checked_at: datetime.datetime,
    ) -> None:
        check = NodeCheck(
            node_id=node_id,
            latency_ms=latency_ms,
            error=error,
            is_active=is_active,
            checked_at=checked_at,
        )

        self.session.add(check)
        await self.session.commit()

    async def create(self, data) -> Node:  # type: ignore[no-untyped-def]
        node = Node(**data.model_dump())
        self.session.add(node)
        await self.session.commit()
        await self.session.refresh(node)
        return node
