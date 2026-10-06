from sqlalchemy.orm import Session

from app.db.models.restaurant import Restaurant
from app.db.models.user import User
from app.core.exceptions import ForbiddenException, NotFoundException
from app.repositories.restaurant import RestaurantRepository
from app.schemas.schemas import RestaurantCreate, RestaurantUpdate


class RestaurantService:

    @staticmethod
    def create_restaurant(
        db: Session,
        restaurant_data: RestaurantCreate,
        current_user: User,
    ) -> Restaurant:

        if current_user.role not in [
            "SYSTEM_ADMIN",
            "RESTAURANT_ADMIN",
        ]:
            raise ForbiddenException(
                "You do not have permission to create a restaurant"
            )

        restaurant = Restaurant(
            name=restaurant_data.name,
            address=restaurant_data.address,
            owner_id=current_user.id,
        )

        return RestaurantRepository.create(db, restaurant)

    @staticmethod
    def get_restaurants(
        db: Session,
    ) -> list[Restaurant]:
        return RestaurantRepository.get_all(db)

    @staticmethod
    def get_restaurant(
        db: Session,
        restaurant_id: int,
    ) -> Restaurant:

        restaurant = RestaurantRepository.get_by_id(
            db,
            restaurant_id,
        )

        if restaurant is None:
            raise NotFoundException("Restaurant not found")

        return restaurant

    @staticmethod
    def update_restaurant(
        db: Session,
        restaurant_id: int,
        restaurant_data: RestaurantUpdate,
        current_user: User,
    ) -> Restaurant:

        restaurant = RestaurantService.get_restaurant(
            db,
            restaurant_id,
        )

        if (
            current_user.role != "SYSTEM_ADMIN"
            and restaurant.owner_id != current_user.id
        ):
            raise ForbiddenException(
                "You do not have permission to modify this restaurant"
            )

        if restaurant_data.name is not None:
            restaurant.name = restaurant_data.name

        if restaurant_data.address is not None:
            restaurant.address = restaurant_data.address

        return RestaurantRepository.save(db, restaurant)

    @staticmethod
    def delete_restaurant(
        db: Session,
        restaurant_id: int,
        current_user: User,
    ) -> None:

        restaurant = RestaurantService.get_restaurant(
            db,
            restaurant_id,
        )

        if (
            current_user.role != "SYSTEM_ADMIN"
            and restaurant.owner_id != current_user.id
        ):
            raise ForbiddenException(
                "You do not have permission to delete this restaurant"
            )

        RestaurantRepository.delete(db, restaurant)
