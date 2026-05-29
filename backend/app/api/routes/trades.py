from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.enums import OperationType, TradeStatus
from app.schemas.trade_operation import TradeOperationCreate, TradeOperationDetail, TradeOperationRead, TradeOperationUpdate
from app.services.trade_service import TradeService

router = APIRouter(prefix="/trades", tags=["Trade Operations"])


@router.post("", response_model=TradeOperationRead, status_code=201)
async def create_trade(payload: TradeOperationCreate, session: AsyncSession = Depends(get_session)):
    return await TradeService(session).create(payload)


@router.get("", response_model=list[TradeOperationDetail])
async def list_trades(
    commodity_id: int | None = None,
    region: str | None = None,
    status: TradeStatus | None = None,
    operation_type: OperationType | None = None,
    session: AsyncSession = Depends(get_session),
):
    return await TradeService(session).list(commodity_id, region, status, operation_type)


@router.get("/{trade_id}", response_model=TradeOperationDetail)
async def get_trade(trade_id: int, session: AsyncSession = Depends(get_session)):
    return await TradeService(session).get_detail(trade_id)


@router.patch("/{trade_id}", response_model=TradeOperationRead)
async def update_trade(trade_id: int, payload: TradeOperationUpdate, session: AsyncSession = Depends(get_session)):
    return await TradeService(session).update(trade_id, payload)


@router.patch("/{trade_id}/confirm", response_model=TradeOperationRead)
async def confirm_trade(trade_id: int, session: AsyncSession = Depends(get_session)):
    return await TradeService(session).confirm(trade_id)


@router.patch("/{trade_id}/settle", response_model=TradeOperationRead)
async def settle_trade(trade_id: int, session: AsyncSession = Depends(get_session)):
    return await TradeService(session).settle(trade_id)


@router.patch("/{trade_id}/cancel", response_model=TradeOperationRead)
async def cancel_trade(trade_id: int, session: AsyncSession = Depends(get_session)):
    return await TradeService(session).cancel(trade_id)
