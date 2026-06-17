import datetime
import uuid

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.nodes.models import Node


class NodeCheck(Base):
    __tablename__ = "node_checks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    node_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    latency_ms: Mapped[int | None] = mapped_column(nullable=True)
    error: Mapped[str | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    checked_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    node: Mapped["Node"] = relationship(back_populates="checks")

    def __repr__(self) -> str:
        return (
            f"<NodeCheck("
            f"id={self.id}, "
            f"node_id='{self.node_id}', "
            f"latency_ms={self.latency_ms}, "
            f"is active={self.is_active}, "
            f"last checked at={self.checked_at}, "
            f"error='{self.error}')>"
        )
