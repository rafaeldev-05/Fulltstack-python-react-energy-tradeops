from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.commodity import Commodity
from app.repositories.commodity_repository import CommodityRepository
from app.schemas.commodity import CommodityCreate, CommodityUpdate


class CommodityService:
    def __init__(self, session: AsyncSession):
        self.repository = CommodityRepository(session)

    async def create(self, payload: CommodityCreate) -> Commodity:
        commodity = Commodity(**payload.model_dump())
        try:
            return await self.repository.create(commodity)
        except IntegrityError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Commodity symbol already exists") from exc

    async def list(self, active_only: bool = False) -> list[Commodity]:
        return await self.repository.list(active_only=active_only)

    async def get(self, commodity_id: int) -> Commodity:
        commodity = await self.repository.get(commodity_id)
        if not commodity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commodity not found")
        return commodity

    async def update(self, commodity_id: int, payload: CommodityUpdate) -> Commodity:
        commodity = await self.get(commodity_id)
        values = payload.model_dump(exclude_unset=True)
        try:
            return await self.repository.update(commodity, values)
        except IntegrityError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Commodity symbol already exists") from exc
