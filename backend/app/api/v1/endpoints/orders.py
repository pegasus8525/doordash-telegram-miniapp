from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_database
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_processor import OrderProcessor

router = APIRouter()

@router.post("/", response_model=OrderResponse)
async def place_order(
    order_in: OrderCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> Any:
    """
    Place a new DoorDash order.
    """
    try:
        order_processor = OrderProcessor(db)
        result = await order_processor.process_order(order_in)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
