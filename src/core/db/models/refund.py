from enum import Enum
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from src.core.db.models.basemodel import Base

if TYPE_CHECKING:
    from src.core.db.models.payment import PaymentsORM


class RefundStatusEnum(str, Enum):
    pending = "PENDING"
    success = "SUCCESS"
    failed = "FAILED"


class RefundORM(Base):
    __tablename__ = "refunds"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), default=uuid4, primary_key=True)

    amount: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[RefundStatusEnum] = mapped_column(default=RefundStatusEnum.pending, nullable=False)
    provider_id: Mapped[str] = mapped_column(String(256), nullable=True)

    payment_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("payments.id", ondelete="CASCADE"),
        nullable=False
    )

    payment_rel: Mapped["PaymentsORM"] = relationship("PaymentsORM", back_populates="refund_rel")
