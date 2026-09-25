from sqlalchemy.orm import Session

from app.db.models.restaurant import Restaurant


class RestaurantRepository:

    @staticmethod
    def create(
        db: Session,
        restaurant: Restaurant,
    ) -> Restaurant:
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)

        return restaurant

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[Restaurant]:
        return db.query(Restaurant).all()

    @staticmethod
    def get_by_id(
        db: Session,
        restaurant_id: int,
    ) -> Restaurant | None:
        return (
            db.query(Restaurant)
            .filter(Restaurant.id == restaurant_id)
            .first()
        )

    @staticmethod
    def save(
        db: Session,
        restaurant: Restaurant,
    ) -> Restaurant:
        db.commit()
        db.refresh(restaurant)

        return restaurant

    @staticmethod
    def delete(
        db: Session,
        restaurant: Restaurant,
    ) -> None:
        db.delete(restaurant)
        db.commit()
