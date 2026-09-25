from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.schemas import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate,
)
from app.services.restaurant import RestaurantService


router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)


@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RestaurantService.create_restaurant(
        db,
        restaurant_data,
        current_user,
    )


@router.get(
    "/",
    response_model=list[RestaurantResponse],
)
def get_restaurants(
    db: Session = Depends(get_db),
):
    return RestaurantService.get_restaurants(db)


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    return RestaurantService.get_restaurant(
        db,
        restaurant_id,
    )


@router.put(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RestaurantService.update_restaurant(
        db,
        restaurant_id,
        restaurant_data,
        current_user,
    )


@router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    RestaurantService.delete_restaurant(
        db,
        restaurant_id,
        current_user,
    )
