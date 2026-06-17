import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.nodes.models import NodeCheck


class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)

    checks: Mapped[list["NodeCheck"]] = relationship(
        back_populates="node", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Node(id='{self.id}', "
            f"name='{self.name}', "
            f"host='{self.host}', "
            f"port={self.port}, "
            f"country_code='{self.country_code}')>"
        )
