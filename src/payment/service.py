import uuid

from sqlalchemy import and_, select, update, delete
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.models.payment import PaymentsORM, PaymentStatus
from src.core.db.models.paymentmethod import PaymentMethodsORM, PaymentMethodStatusEnum

from src.shared.schemas import PaymentDataBase

from src.payment.schemas import PaymentMethodDatabase, PaymentMethodBase
from src.payment.exceptions import (
    PaymentNotFoundException,
    MultiplePaymentsFoundException,
)


async def service_create_payment(
        amount: int,
        user_id: str,
        booking_id: str,
        session: AsyncSession
) -> PaymentDataBase:
    new_payment = PaymentsORM(
        amount = amount,
        user_id = user_id,
        booking_id = booking_id
    )
    session.add(new_payment)
    await session.commit()
    await session.refresh(new_payment)
    res_dto = PaymentDataBase.model_validate(new_payment)
    return res_dto


async def service_update_payment(transaction_id: str, provider_id: str, payment_metadata: str, session: AsyncSession) -> None:
    await session.execute(
        update(PaymentsORM)
        .where(PaymentsORM.id == transaction_id)
        .values(
            provider_id = provider_id,
            payment_metadata = payment_metadata
        )
    )
    await session.commit()


async def service_find_payment_by_id(id: uuid.UUID | str, session: AsyncSession) -> PaymentDataBase:
    try:
        data_orm = (await session.execute(
            select(PaymentsORM)
            .filter_by(id = id)
        )).scalars().one()
    except NoResultFound:
        raise PaymentNotFoundException()
    except MultipleResultsFound:
        raise MultiplePaymentsFoundException()
    
    data_dto = PaymentDataBase.model_validate(data_orm)
    return data_dto


async def service_find_payment_by_booking_id(booking_id: str, session: AsyncSession) -> PaymentDataBase | None:
    data_orm = (await session.execute(
        select(PaymentsORM)
        .where(
            and_(
                PaymentsORM.booking_id == booking_id,
                PaymentsORM.status != PaymentStatus.refunded)
            )
        .limit(1)
    )).scalar_one_or_none()

    if not data_orm:
        return None

    data_dto = PaymentDataBase.model_validate(data_orm)
    return data_dto


async def service_mark_payment_refunded(payment_id: str, session: AsyncSession) -> PaymentDataBase:
    data_orm = (await session.execute(
        update(PaymentsORM)
        .where(PaymentsORM.id == payment_id)
        .values(
            status = PaymentStatus.refunded
        )
        .returning(PaymentsORM)
    )).scalar_one()

    await session.commit()
    data_dto = PaymentDataBase.model_validate(data_orm)
    return data_dto


async def service_mark_payment_method_success(id: uuid.UUID | str, session: AsyncSession) -> PaymentDataBase:
    data_orm = (await session.execute(
        update(PaymentsORM)
        .where(PaymentsORM.id == id)
        .values(
            status = PaymentStatus.success
        )
        .returning(PaymentsORM)
    )).scalar_one()
    
    await session.commit()
    return PaymentDataBase.model_validate(data_orm)


async def service_mark_payment_method_failed(id: uuid.UUID | str, session: AsyncSession) -> PaymentDataBase:
    data_orm = (await session.execute(
        update(PaymentsORM)
        .where(PaymentsORM.id == id)
        .values(
            status = PaymentStatus.failed
        )
        .returning(PaymentsORM)
    )).scalar_one()
    
    await session.commit()
    return PaymentDataBase.model_validate(data_orm)


async def service_find_user_payment_methods(user_id: str, session: AsyncSession) -> list[PaymentMethodDatabase] | None:
    data_orm = (await session.execute(
        select(PaymentMethodsORM)
        .where(
            PaymentMethodsORM.user_id == user_id,
            PaymentMethodsORM.status == PaymentMethodStatusEnum.active
        )
        .order_by(
            PaymentMethodsORM.created_at.desc() 
        )
    )).scalars().all()

    if not data_orm:
        return None
    
    data_dto = [PaymentMethodDatabase.model_validate(elem_data_orm) for elem_data_orm in data_orm]
    return data_dto


async def service_find_payment_method_by_id(id: uuid.UUID | str, session: AsyncSession) -> PaymentMethodDatabase | None:
    try:
        data_orm = (await session.execute(
            select(PaymentMethodsORM)
            .filter_by(id = id)
        )).scalars().one_or_none()
    except MultipleResultsFound:
        raise MultiplePaymentsFoundException()
    
    if not data_orm:
        return None
    
    data_dto = PaymentMethodDatabase.model_validate(data_orm)
    return data_dto


async def service_find_active_payment_method(user_id: str, provider_method_id: str, session: AsyncSession) -> PaymentMethodDatabase | None:
    data_orm = (await session.execute(
        select(PaymentMethodsORM)
        .filter_by(
            user_id = user_id,
            provider_id = provider_method_id,
            status = PaymentMethodStatusEnum.active
        )
    )).scalars().first()

    if not data_orm:
        return None
    
    data_dto = PaymentMethodDatabase.model_validate(data_orm)
    return data_dto


async def service_create_payment_method(payment_method_data: PaymentMethodBase, session: AsyncSession) -> None:
    new_payment_method = PaymentMethodsORM(
        payment_method_type = payment_method_data.payment_method_type,
        bank = payment_method_data.bank,
        brand = payment_method_data.brand,
        first6 = payment_method_data.first6,
        last4 = payment_method_data.last4,
        provider_id = payment_method_data.provider_id,
        user_id = payment_method_data.user_id,
        status = payment_method_data.status
    )
    session.add(new_payment_method)
    await session.commit()


async def service_delete_payment_method(method_id: str, session: AsyncSession) -> None:
    await session.execute(
        delete(PaymentMethodsORM)
        .where(PaymentMethodsORM.id == method_id)
    )
    await session.commit()