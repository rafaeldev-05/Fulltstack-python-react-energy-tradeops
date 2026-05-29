from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.enums import RiskSeverity
from app.models.risk_alert import RiskAlert


class RiskAlertRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, alert: RiskAlert) -> RiskAlert:
        self.session.add(alert)
        await self.session.commit()
        await self.session.refresh(alert)
        return alert

    async def list(self, severity: RiskSeverity | None = None, resolved: bool | None = None) -> list[RiskAlert]:
        statement = select(RiskAlert).order_by(RiskAlert.created_at.desc())
        if severity:
            statement = statement.where(RiskAlert.severity == severity)
        if resolved is not None:
            statement = statement.where(RiskAlert.resolved == resolved)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get(self, alert_id: int) -> RiskAlert | None:
        return await self.session.get(RiskAlert, alert_id)

    async def resolve(self, alert: RiskAlert) -> RiskAlert:
        alert.resolved = True
        self.session.add(alert)
        await self.session.commit()
        await self.session.refresh(alert)
        return alert
