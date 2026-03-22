from aioyookassa import YooKassa
from aioyookassa.types import CreateRefundParams, Currency, Money

from src.core.db import DataBase

from src.core.clients.booking import BookingClient

from src.payment.exceptions import (
    PaymentNotFoundException,
)
from src.payment.service import (
    service_find_payment_by_booking_id,
    service_mark_payment_refunded,
)

from src.refund.exceptions import(
    RefundNotFoundException,
)
from src.refund.shemas import RefundBase
from src.refund.service import (
    service_create_refund,
    service_update_refund,
    service_find_refund_by_provider_id,
    service_mark_refund_success,
)


class RefundHandler:
    def __init__(self, db: DataBase, yookassa_client: YooKassa, booking_client: BookingClient):
        self._db = db
        self._yookassa_client = yookassa_client
        self._booking_client = booking_client


    async def CreateRefundRequest(self, booking_id: str, user_id: str):
        async with self._db.session() as session:
            payment = await service_find_payment_by_booking_id(
                booking_id = booking_id,
                session = session
            )
        
            if not payment or payment.user_id != user_id:
                raise PaymentNotFoundException()

            refund = await service_create_refund(
                data = RefundBase(
                    amount = payment.amount,
                    payment_id = payment.id
                ),
                session = session
            )

        yk = await self._yookassa_client.refunds.create_refund(
            params = CreateRefundParams(
                payment_id = payment.provider_id,
                amount = Money(value=payment.amount, currency=Currency.RUB)
            )
        )

        async with self._db.session() as session:
            await service_update_refund(
                refund_id = refund.id,
                provider_id = yk.id,
                session = session
            )

        return True

        
    async def ProcessRefundEvent(
            self,
            event: str,
            provider_refund_id: str,
            status: str
    ):
        async with self._db.session() as session:
            refund = await service_find_refund_by_provider_id(
                provider_id = provider_refund_id,
                session = session
            )

        if not refund:
            raise RefundNotFoundException

        if event == "refund.succeeded":
            try:
                async with self._db.session() as session:
                    await service_mark_refund_success(id = refund.id, session = session)
                    await service_mark_payment_refunded(payment_id = refund.payment_id, session = session)

                    await self._booking_client.CancelBooking(
                        booking_id = refund.payment_rel.booking_id,
                        user_id = refund.payment_rel.user_id
                    )

                    return True
            except Exception as e:
                print(str(e))
             
        return False