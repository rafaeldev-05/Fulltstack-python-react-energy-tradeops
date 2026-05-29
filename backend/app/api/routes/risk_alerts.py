from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.enums import RiskSeverity
from app.schemas.risk_alert import RiskAlertRead
from app.services.risk_service import RiskService

router = APIRouter(prefix="/risk-alerts", tags=["Risk Alerts"])


@router.get("", response_model=list[RiskAlertRead])
async def list_risk_alerts(
    severity: RiskSeverity | None = None,
    resolved: bool | None = None,
    session: AsyncSession = Depends(get_session),
):
    return await RiskService(session).list(severity, resolved)


@router.patch("/{alert_id}/resolve", response_model=RiskAlertRead)
async def resolve_risk_alert(alert_id: int, session: AsyncSession = Depends(get_session)):
    return await RiskService(session).resolve(alert_id)


@router.post("/run-monitoring-cycle")
async def run_monitoring_cycle(session: AsyncSession = Depends(get_session)):
    return await RiskService(session).run_monitoring_cycle()
