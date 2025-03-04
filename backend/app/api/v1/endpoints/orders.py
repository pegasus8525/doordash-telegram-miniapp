from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app.api import deps
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_processor import OrderProcessor

router = APIRouter()

@router.post("/", response_model=OrderResponse)
def place_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: OrderCreate,
) -> Any:
    """
    Place a new DoorDash order.
    """
    try:
        order_processor = OrderProcessor(db)
        result = order_processor.process_order(order_in)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )