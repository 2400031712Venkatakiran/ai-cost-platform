from fastapi import APIRouter

api_router = APIRouter()

# Feature routers are included here as we build them, for example:
# api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])