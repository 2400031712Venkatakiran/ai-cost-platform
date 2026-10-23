import logging

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.db.database import get_db
from app.schemas.health import HealthResponse, ReadinessResponse

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Liveness check: confirms the application process is running."""
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
    )


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    responses={503: {"model": ReadinessResponse}},
)
async def readiness_check(
    response: Response,
    session: AsyncSession = Depends(get_db),
) -> ReadinessResponse:
    """Readiness check: confirms the app can actually reach its database."""
    try:
        await session.execute(text("SELECT 1"))
    except Exception:  # noqa: BLE001 - any failure means "not ready"
        logger.exception("Readiness check failed: database unreachable")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ReadinessResponse(status="unavailable", database="down")
    return ReadinessResponse(status="ok", database="up")