from sqlalchemy.orm import Session
from app.db.models.menu_item import MenuItem

class MenuItemRepository:

    @staticmethod
    def create(
        db: Session,
        item: MenuItem,
    ) -> MenuItem:
        db.add(item)
        db.commit()
        db.refresh(item)

        return item
    
    @staticmethod
    def get_by_id(
        db: Session,
        item_id: int,
    ) -> MenuItem | None:
        return (
            db.query(MenuItem)
            .filter(MenuItem.id == item_id)
            .first()
        )

    @staticmethod
    def get_by_category(
        db: Session,
        category_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[MenuItem]:
        return (
            db.query(MenuItem)
            .filter(MenuItem.category_id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def save(
        db: Session,
        item: MenuItem,
    ) -> MenuItem:
        db.commit()
        db.refresh(item)

        return item

    @staticmethod
    def delete(
        db: Session,
        item: MenuItem,
    ) -> None:
        db.delete(item)
        db.commit()
