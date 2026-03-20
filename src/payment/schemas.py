import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from src.core.db.models.payment import PaymentStatus
from src.core.db.models.paymentmethod import PaymentMethodStatusEnum

from src.shared.schemas import RefundDataBase


class SeatType(BaseModel):
    seat_id: str
    price: int


class CreatePaymentRequestDTO(BaseModel):
    user_id: str
    screening_id: str = Field(...)
    seats: list[SeatType]
    payment_method_id: str | None = Field(default=None)
    save_payment_method: bool


class ProcessPaymentEventRequestDTO(BaseModel):
    event: str
    payment_id: str
    booking_id: str
    user_id: str
    save_payment_method: bool = False
    provider_method_id: Optional[str] = None
    card_first6: Optional[str] = Field(None, min_length=6, max_length=6)
    card_last4: Optional[str] = Field(None, min_length=4, max_length=4)
    bank: str | None = None
    brand: str | None = None


class PaymentMethodBase(BaseModel):
    payment_method_type: str
    bank: str | None = None
    brand: str | None = None
    first6: str | None = None
    last4: str | None = None
    provider_id: str
    user_id: str
    status: PaymentMethodStatusEnum


class PaymentMethodDatabase(PaymentMethodBase):
    model_config = ConfigDict(
        from_attributes = True
    )

    id: uuid.UUID | str
    

class PaymentMethodItem(BaseModel):
    id: str
    bank: str
    brand: str
    first6: str
    last4: str
