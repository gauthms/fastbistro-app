from sqlalchemy.orm import Session

from app.db.models.order import Order, OrderItem


class OrderRepository:

    @staticmethod
    def create_order(
        db: Session,
        order: Order,
    ) -> Order:
        try:
            db.add(order)
            db.commit()
            db.refresh(order)

            return order

        except:
            db.rollback()
            raise
            

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
        skip: int = 0,
        limit: int = 20,
    ) -> list[Order]:
        return (
            db.query(Order)
            .filter(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_restaurant(
        db: Session,
        restaurant_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Order]:
        return (
            db.query(Order)
            .filter(Order.restaurant_id == restaurant_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def save(
        db: Session,
        order: Order,
    ) -> Order:

        try:
            db.commit()
            db.refresh(order)

            return order
        except Exception:
            db.rollback()
            raise
