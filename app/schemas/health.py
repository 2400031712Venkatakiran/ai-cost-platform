from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str


class ReadinessResponse(BaseModel):
    status: str
    database: str