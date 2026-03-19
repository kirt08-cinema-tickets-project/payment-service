import json

from aioyookassa import YooKassa
from aioyookassa.types.params import CreatePaymentParams, BankCardPaymentMethodData
from aioyookassa.types.payment import Money, Currency, Confirmation
from aioyookassa.types.enum import ConfirmationType

from src.core.db import DataBase
from src.core.db.models.paymentmethod import PaymentMethodStatusEnum
from src.core.config import settings

from src.payment.exceptions import (
    NotPaymentMethodFoundException,
)
from src.payment.schemas import (
    CreatePaymentRequestDTO,
    ProcessPaymentEventRequestDTO,
    PaymentMethodDatabase,
    PaymentMethodBase
)
from src.payment.service import (
    service_create_payment,
    service_update_payment,
    service_find_payment_by_id,
    service_find_payment_method_by_id,
    service_mark_payment_method_success,
    service_mark_payment_method_failed,
    service_create_payment_method,
    service_find_active_payment_method,
    service_find_user_payment_methods,
    service_delete_payment_method,
)


class PaymentHandler:
    def __init__(self, db: DataBase, yookassa_client: YooKassa):
        self._db = db
        self._yookassa_client = yookassa_client

    async def CreatePayment(self, data: CreatePaymentRequestDTO):
        async with self._db.session() as session:
            transaction = await service_create_payment(
                amount = 1000,
                user_id = data.user_id,
                session = session 
            )

            payment_method: PaymentMethodDatabase | None = None

            if data.payment_method_id:
                payment_method = await service_find_payment_method_by_id(id = data.payment_method_id, session = session)

                if not payment_method:
                    raise NotPaymentMethodFoundException

        params = CreatePaymentParams(
            amount = Money(
                value = transaction.amount,
                currency = Currency.RUB
            ),
            description = f"Оплата билетов на сеанс {data.screening_id}",
            confirmation = Confirmation(
                type = ConfirmationType.REDIRECT,
                return_url = f"{settings.host_app.url}/account/tickets"
            ),
            metadata = {
                "payment_id": str(transaction.id),
                "user_id": str(data.user_id),
                "booking_id": "123456"
            }
        )

        if payment_method:
            params.payment_method_id = payment_method.provider_id
        else:
            params.payment_method_data = BankCardPaymentMethodData(type="bank_card")
            params.save_payment_method = data.save_payment_method

        payment = await self._yookassa_client.payments.create_payment(params)
        print(payment)

        async with self._db.session() as session:
            await service_update_payment(
                transaction_id = transaction.id,
                provider_id = payment.id,
                payment_metadata = json.dumps(payment.metadata),
                session = session
            )

        return payment.confirmation.url if payment.confirmation.url else f"{settings.host_app.url}/account/tickets/callback"
    

    async def ProcessPaymentEvent(self, data: ProcessPaymentEventRequestDTO) -> bool:
        async with self._db.session() as session:
            payment = await service_find_payment_by_id(id = data.payment_id, session = session)

        if data.event == "payment.waiting_for_capture":
            try:
                await self._yookassa_client.payments.capture_payment(payment_id = payment.provider_id)
            except Exception as e:
                print(str(e))

        if data.event == "payment.succeeded":
            async with self._db.session() as session:
                await service_mark_payment_method_success(id = payment.id, session = session)

                if data.save_payment_method and data.provider_method_id:
                    existing = await service_find_active_payment_method(
                        user_id = data.user_id,
                        provider_method_id = data.provider_method_id,
                        session = session
                    )

                    if existing:
                        return
                    
                    await service_create_payment_method(
                        payment_method_data= PaymentMethodBase(
                            payment_method_type = "BANK_CARD",
                            bank = data.bank,
                            brand = data.brand,
                            provider_id = data.provider_method_id,
                            user_id = data.user_id,
                            status = PaymentMethodStatusEnum.active,
                            first6 = data.card_first6,
                            last4 = data.card_last4
                        ),
                        session = session
                    )

        
        if data.event == "payment.canceled":
            async with self._db.session() as session:
                await service_mark_payment_method_failed(id = payment.id, session = session)


        return True
    

    async def GetUserPaymentMethods(self, user_id: str) -> list[PaymentMethodDatabase]:
        async with self._db.session() as session:
            data = await service_find_user_payment_methods(
                user_id = user_id,
                session = session
            )
        return data
    

    async def DeleteUserPaymentMethod(self, user_id: str, method_id: str) -> bool:
        async with self._db.session() as session:
            method = await service_find_payment_method_by_id(id = method_id, session = session)

            if not method or method.user_id != user_id:
                raise NotPaymentMethodFoundException()
            
            await service_delete_payment_method(method_id = method_id, session = session)

        return True