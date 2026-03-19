from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID

from src.core.db.models.basemodel import Base


class PaymentMethodStatusEnum(str, Enum):
    pending = "PENDING"
    active = "ACTIVE"


class PaymentMethodsORM(Base):
    __tablename__ = "payment_methods"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid4, primary_key=True)

    payment_method_type: Mapped[str] = mapped_column(String(256))
    status: Mapped[PaymentMethodStatusEnum] = mapped_column(default=PaymentMethodStatusEnum.pending)

    bank: Mapped[str] = mapped_column(String(64), nullable=True)
    brand: Mapped[str] = mapped_column(String(64), nullable=True)

    first6: Mapped[str] = mapped_column(String(16), nullable=True)
    last4: Mapped[str] = mapped_column(String(16), nullable=True)

    provider_id: Mapped[str] = mapped_column(String(256))
    user_id: Mapped[str] = mapped_column(String(256))