from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.models.refund import RefundORM, RefundStatusEnum

from src.shared.schemas import RefundDataBase, RefundDataBaseWithRel

from src.refund.shemas import RefundBase


async def service_find_refund_by_provider_id(provider_id: str, session: AsyncSession) -> RefundDataBaseWithRel | None:
    data_orm = (await session.execute(
        select(RefundORM)
        .where(RefundORM.provider_id == provider_id)
        .options(
            selectinload(RefundORM.payment_rel)
        )
        .limit(1)
    )).scalar_one_or_none()

    if not data_orm:
        return None
    
    data_dto = RefundDataBaseWithRel.model_validate(data_orm)
    return data_dto


async def service_create_refund(data: RefundBase, session: AsyncSession) -> RefundDataBase:
    new_refund = RefundORM(
        amount = data.amount,
        status = data.status,
        payment_id = data.payment_id
    )
    session.add(new_refund)
    await session.commit()
    await session.refresh(new_refund)
    return new_refund


async def service_update_refund(refund_id: str, provider_id: str, session: AsyncSession) -> RefundDataBase | None:
    data_orm = (await session.execute(
        update(RefundORM)
        .where(RefundORM.id == refund_id)
        .values(
            provider_id = provider_id
        )
        .returning(RefundORM)
    )).scalar_one_or_none()

    if not data_orm:
        return None

    await session.commit()
    data_dto = RefundDataBase.model_validate(data_orm)
    return data_dto


async def service_mark_refund_success(id: str, session: AsyncSession) -> RefundDataBase:
    data_orm = (await session.execute(
        update(RefundORM)
        .where(RefundORM.id == id)
        .values(
            status = RefundStatusEnum.success
        )
        .returning(RefundORM)
    )).scalar_one()

    await session.commit()
    data_dto = RefundDataBase.model_validate(data_orm)
    return data_dto


async def service_mark_refund_failed(id: str, session: AsyncSession) -> RefundDataBase:
    data_orm = (await session.execute(
        update(RefundORM)
        .where(RefundORM.id == id)
        .values(
            status = RefundStatusEnum.failed
        )
        .returning(RefundORM)
    )).scalar_one()

    await session.commit()
    data_dto = RefundDataBase.model_validate(data_orm)
    return data_dto

