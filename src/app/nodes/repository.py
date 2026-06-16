from sqlalchemy import select

from app.db.repository import BaseRepository
from app.nodes.models import Node


class NodeRepository(BaseRepository):
    async def list_active(self) -> list[Node]:
        stmt = select(Node).where(Node.is_active.is_(True)).order_by(Node.name)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
