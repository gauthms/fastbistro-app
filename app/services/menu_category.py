from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.menu_category import MenuCategory
from app.db.models.user import User
from app.repositories.menu_category import MenuCategoryRepository
from app.repositories.restaurant import RestaurantRepository
from app.schemas.schemas import MenuCategoryCreate, MenuCategoryUpdate


class MenuCategoryService:

    @staticmethod
    def create_category(
        db: Session,
        restaurant_id: int,
        category_data: MenuCategoryCreate,
        current_user: User,
    ) -> MenuCategory:

        restaurant = RestaurantRepository.get_by_id(
            db,
            restaurant_id,
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )

        if current_user.role != "SYSTEM_ADMIN" and restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to manage this restaurant",
            )

        category = MenuCategory(
            name=category_data.name,
            restaurant_id=restaurant_id,
        )

        return MenuCategoryRepository.create(db, category)


    @staticmethod
    def get_categories(
        db: Session,
        restaurant_id: int,
    ) -> list[MenuCategory]:

        restaurant = RestaurantRepository.get_by_id(
            db,
            restaurant_id,
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )

        return MenuCategoryRepository.get_by_restaurant(
            db,
            restaurant_id,
        )

    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        category_data: MenuCategoryUpdate,
        current_user: User,
    ) -> MenuCategory:

        category = MenuCategoryRepository.get_by_id(
            db,
            category_id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
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
                detail="You do not have permission to modify this category",
            )

        if category_data.name is not None:
            category.name = category_data.name


        return MenuCategoryRepository.save(
            db,
            category,
        )


    @staticmethod
    def delete_category(
        db: Session,
        category_id: int,
        current_user: User,
    ) -> None:

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
            category.restaurant_id,
        )

        if (
            current_user.role != "SYSTEM_ADMIN"
            and restaurant.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this category",
            )

        MenuCategoryRepository.delete(
            db,
            category,
        )
            