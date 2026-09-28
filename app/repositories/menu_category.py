from sqlalchemy.orm import Session

from app.db.models.menu_category import MenuCategory



class MenuCategoryRepository:

    @staticmethod
    def create(
        db: Session,
        category: MenuCategory,
    ) -> MenuCategory:
        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def get_by_restaurant(
        db: Session,
        restaurant_id: int,
    ) -> list[MenuCategory]:
        return (
            db.query(MenuCategory)
            .filter(MenuCategory.restaurant_id == restaurant_id)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: int,
    ) -> MenuCategory | None:
        return (
            db.query(MenuCategory)
            .filter(MenuCategory.id == category_id)
            .first()
        )

    @staticmethod
    def save(
        db: Session,
        category: MenuCategory,
    ) -> MenuCategory:
        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def delete(
        db: Session,
        category: MenuCategory,
    ) -> None:
        db.delete(category)
        db.commit()

