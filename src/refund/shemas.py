from uuid import UUID

from pydantic import BaseModel, Field

from src.core.db.models.refund import RefundStatusEnum


class RefundBase(BaseModel):
    amount: int
    status: RefundStatusEnum = Field(default=RefundStatusEnum.pending)
    payment_id: str | UUID