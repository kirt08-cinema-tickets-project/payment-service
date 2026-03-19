import uuid
from enum import Enum

from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from src.core.db.models.basemodel import Base

class PaymentStatus(str, Enum):
    pending = "PENDING"
    success = "SUCCESS"
    failed = "FAILED"
    refunded = "REFUNDED"


class PaymentsORM(Base):
    __tablename__ = "payments"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(default=PaymentStatus.failed)
    provider_id: Mapped[str | None] = mapped_column(String(512), nullable=True)
    payment_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    user_id: Mapped[str] = mapped_column(String(256), nullable=False)
    
