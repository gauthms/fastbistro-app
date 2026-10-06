from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.models.user import User
from app.core.auth import get_current_user
from app.core.exceptions import ForbiddenException, NotFoundException
from app.db.database import get_db
from app.db.models.restaurant import Restaurant


def require_role(required_role: str):
    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        if current_user.role != required_role:
            raise ForbiddenException(
                "You do not have permission to perform this action"
            )

        return current_user


    return role_checker

def require_restaurant_access(
    restaurant_id: int,
    db: Session,
    current_user: User,
) -> Restaurant:
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )

    if restaurant is None:
        raise NotFoundException("Restaurant not found")

    if current_user.role == "SYSTEM_ADMIN":
        return restaurant

    if (
        current_user.role == "RESTAURANT_ADMIN"
        and restaurant.owner_id == current_user.id
    ):
        return restaurant

    raise ForbiddenException(
        "You do not have permission to access this restaurant"
    )


system_admin_required = require_role("SYSTEM_ADMIN")
restaurant_admin_required = require_role("RESTAURANT_ADMIN")
customer_required = require_role("CUSTOMER")
