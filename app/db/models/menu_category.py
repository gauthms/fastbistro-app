from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class MenuCategory(Base):
    __tablename__ = "menu_categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"),
        nullable=False,
    )

    restaurant = relationship("Restaurant")
