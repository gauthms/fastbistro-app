from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.schemas import (
    MenuItemCreate,
    MenuItemResponse,
    MenuItemUpdate
)
from app.services.menu_item import MenuItemService


router = APIRouter(
    prefix="/categories/{category_id}/items",
    tags=["Menu Items"],
)


@router.post(
    "/",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    category_id: int,
    item_data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MenuItemService.create_item(
        db,
        category_id,
        item_data,
        current_user,
    )


@router.get(
    "/",
    response_model=list[MenuItemResponse],
)
def get_items(
    category_id: int,
    db: Session = Depends(get_db),
):
    return MenuItemService.get_items(
        db,
        category_id,
    )


@router.put(
    "/{item_cd}",
    response_model=MenuItemResponse
)
def update_item(
    item_id: int,
    category_id: int,
    item_data: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MenuItemService.update_item(
        db,
        category_id,
        item_id,
        item_data,
        current_user,
    )

@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(
    category_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    MenuItemService.delete_item(
        db,
        category_id,
        item_id,
        current_user,
    )