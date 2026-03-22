from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from src.core.db.models.payment import PaymentStatus
from src.core.db.models.refund import RefundStatusEnum


class PaymentDataBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID | str
    amount: int
    status: PaymentStatus
    provider_id: str | None = None
    payment_metadata: str | None = None
    user_id: str
    booking_id: str
   

class PaymentDataBaseWithRel(PaymentDataBase):
    refund_rel: list["RefundDataBase"] | None = None

    
class RefundDataBase(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )

    id: UUID | str
    amount: int
    status: RefundStatusEnum = Field(default=RefundStatusEnum.pending)
    payment_id: UUID | str
    provider_id: UUID | str
    

class RefundDataBaseWithRel(RefundDataBase):
    payment_rel: PaymentDataBase | None = None

# GRPC
class CreateReservationResponse(BaseModel):
    order_id: str
    tickets_id: list[str]
    amount: int