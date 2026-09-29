from sqlalchemy.orm import Session

from app.db.models.order import Order, OrderItem


class OrderRepository:

    @staticmethod
    def create_order(
        db: Session,
        order: Order,
    ) -> Order:
        db.add(order)
        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def get_by_id(
        db: Session,
        order_id: int,
    ) -> Order | None:
        return (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    @staticmethod
    def get_by_customer(
        db: Session,
        customer_id: int,
    ) -> list[Order]:
        return (
            db.query(Order)
            .filter(Order.customer_id == customer_id)
            .all()
        )

    @staticmethod
    def get_by_restaurant(
        db: Session,
        restaurant_id: int,
    ) -> list[Order]:
        return (
            db.query(Order)
            .filter(Order.restaurant_id == restaurant_id)
            .all()
        )

    @staticmethod
    def save(
        db: Session,
        order: Order,
    ) -> Order:
        db.commit()
        db.refresh(order)

        return order