from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.schemas import (
    MenuCategoryCreate,
    MenuCategoryResponse,
)
from app.services.menu_category import MenuCategoryService


router = APIRouter(
    prefix="/restaurants/{restaurant_id}/categories",
    tags=["Menu Categories"],
)

category_router = APIRouter(
    prefix="/categories",
    tags=["Menu Categories"],
)

@router.get(
    "/",
    response_model=list[MenuCategoryResponse],
)
def get_categories(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    return MenuCategoryService.get_categories(
        db,
        restaurant_id,
    )


@router.post(
    "/",
    response_model=MenuCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    restaurant_id: int,
    category_data: MenuCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MenuCategoryService.create_category(
        db,
        restaurant_id,
        category_data,
        current_user,
    )

@router.put(
    "/{category_id}",
    response_model=MenuCategoryResponse,
)
def update_category(
    category_id: int,
    category_data: MenuCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MenuCategoryService.update_category(
        db,
        category_id,
        category_data,
        current_user,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    MenuCategoryService.delete_category(
        db,
        category_id,
        current_user,
    )
    