from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.menu_item import MenuItem
from app.db.models.user import User
from app.repositories.menu_category import MenuCategoryRepository
from app.repositories.menu_item import MenuItemRepository
from app.repositories.restaurant import RestaurantRepository
from app.schemas.schemas import MenuItemCreate, MenuItemUpdate

class MenuItemService:

    @staticmethod
    def create_item(
        db: Session,
        category_id: int,
        item_data: MenuItemCreate,
        current_user: User
    ) -> MenuItem:

        category = MenuCategoryRepository.get_by_id(
            db,
            category_id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        restaurant = RestaurantRepository.get_by_id(
            db,
            category.restaurant_id
        )


        if (
            current_user.role != "SYSTEM_ADMIN"
            and restaurant.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permissions to manage this menu"
            )

        item = MenuItem(
            name=item_data.name,
            description=item_data.description,
            price=item_data.price,
            is_available=item_data.is_available,
            category_id=category_id,
        )

        return MenuItemRepository.create(
            db,
            item,
        )

    @staticmethod
    def get_items(
        db: Session,
        category_id: int,
    ) -> list[MenuItem]:
        
        category = MenuCategoryRepository.get_by_id(
            db,
            category_id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return MenuItemRepository.get_by_category(
            db,
            category_id,
        )


    @staticmethod
    def update_item(
        db: Session,
        category_id: int,
        item_id: int,
        item_data: MenuItemUpdate,
        current_user: User,
    ) -> MenuItem:

        item = MenuItemRepository.get_by_id(
            db,
            item_id,
        )

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found",
            )

        if item.category_id != category_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found in this category",
            )

        category = MenuCategoryRepository.get_by_id(
            db,
            item.category_id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        restaurant = RestaurantRepository.get_by_id(
            db,
            category.restaurant_id,
        )

        if (
            current_user.role != "SYSTEM_ADMIN"
            and restaurant.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to modify this menu item",
            )

        if item_data.name is not None:
            item.name = item_data.name

        if item_data.description is not None:
            item.description = item_data.description

        if item_data.price is not None:
            item.price = item_data.price

        if item_data.is_available is not None:
            item.is_available = item_data.is_available

        return MenuItemRepository.save(
            db,
            item,
        )


    @staticmethod
    def delete_item(
        db: Session,
        category_id: int,
        item_id: int,
        current_user: User,
    ) -> None:

        item = MenuItemRepository.get_by_id(
            db,
            item_id,
        )

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found",
            )


        if item.category_id != category_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found in this category",
            )

        category = MenuCategoryRepository.get_by_id(
            db,
            item.category_id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        restaurant = RestaurantRepository.get_by_id(
            db,
            category.restaurant_id,
        )

        if (
            current_user.role != "SYSTEM_ADMIN"
            and restaurant.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this menu item",
            )

        MenuItemRepository.delete(
            db,
            item,
        )