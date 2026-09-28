import unittest
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.database import Base
from app.db.models.menu_category import MenuCategory
from app.db.models.menu_item import MenuItem
from app.db.models.restaurant import Restaurant
from app.db.models.user import User
from app.schemas.schemas import MenuItemCreate
from app.services.menu_item import MenuItemService


class MenuItemServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.db: Session = self.SessionLocal()

        self.user = User(
            name="Owner",
            email="owner@example.com",
            password_hash="hashed",
            role="RESTAURANT_ADMIN",
        )
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

        self.restaurant = Restaurant(
            name="Test Restaurant",
            address="123 Main St",
            owner_id=self.user.id,
        )
        self.db.add(self.restaurant)
        self.db.commit()
        self.db.refresh(self.restaurant)

        self.category = MenuCategory(
            name="Lunch",
            restaurant_id=self.restaurant.id,
        )
        self.db.add(self.category)
        self.db.commit()
        self.db.refresh(self.category)

    def tearDown(self):
        self.db.close()

    def test_create_item_persists_orm_model(self):
        item_data = MenuItemCreate(
            name="Burger",
            description="Cheesy and grilled",
            price=Decimal("12.50"),
            is_available=True,
        )

        created = MenuItemService.create_item(
            self.db,
            self.category.id,
            item_data,
            self.user,
        )

        self.assertIsInstance(created, MenuItem)
        self.assertEqual(created.name, "Burger")
        self.assertEqual(created.category_id, self.category.id)
        self.assertEqual(self.db.query(MenuItem).count(), 1)


if __name__ == "__main__":
    unittest.main()
