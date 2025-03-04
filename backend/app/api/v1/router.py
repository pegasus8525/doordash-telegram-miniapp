from fastapi import APIRouter
from app.api.v1.endpoints import orders, chains

api_router = APIRouter()

api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(chains.router, prefix="/chains", tags=["chains"])