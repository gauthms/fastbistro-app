from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return OrderService.create_order(
        db,
        order_data,
        current_user,
    )

@router.get(
    "/my-orders",
    response_model=list[OrderResponse],
)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(
        default=0,
        ge=0,
    ),
    offset: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
):
    return OrderService.get_my_orders(
        db,
        current_user,
        skip,
        offset,
    )

@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return OrderService.get_order(
        db,
        order_id,
        current_user,
    )

@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return OrderService.update_status(
        db,
        order_id,
        status_data,
        current_user,
    )


@router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse,
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return OrderService.cancel_order(
        db,
        order_id,
        current_user,
    )
