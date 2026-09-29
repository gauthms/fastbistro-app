from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.order import Order, OrderItem, OrderStatus
from app.db.models.user import User
from app.repositories.menu_item import MenuItemRepository
from app.repositories.order import OrderRepository
from app.repositories.restaurant import RestaurantRepository
from app.schemas.schemas import OrderCreate, OrderResponse, OrderStatusUpdate



ALLOWED_STATUS_TRANSITIONS = {
    OrderStatus.PENDING: [
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
    ],
    OrderStatus.CONFIRMED: [
        OrderStatus.PREPARING,
        OrderStatus.CANCELLED,
    ],
    OrderStatus.PREPARING: [
        OrderStatus.READY,
    ],
    OrderStatus.READY: [
        OrderStatus.COMPLETED,
    ],
    OrderStatus.COMPLETED: [],
    OrderStatus.CANCELLED: [],
}


class OrderService:

    @staticmethod
    def create_order(
        db: Session,
        order_data: OrderCreate,
        current_user: User
    ) -> Order:

        # Only customers can place orders
        if current_user.role != "CUSTOMER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can place orders",
            )

        # Check that the repository exists
        restaurant = RestaurantRepository.get_by_id(
            db,
            order_data.restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )


        order = Order(
            customer_id=current_user.id,
            restaurant_id=order_data.restaurant_id,
            status="PENDING",
            total_amount=Decimal("0.00"),
        )

        total = Decimal("0.00")

        for item_data in order_data.items:

            menu_item = MenuItemRepository.get_by_id(
                db,
                item_data.menu_item_id,
            )

            if menu_item is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Menu item {item_data.menu_item_id} not found",
                )

            # Make sure the menu item belongs to this restaurant
            if menu_item.category.restaurant_id != restaurant.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Menu item does not belong to this restaurant",
                )

            # Check availability
            if not menu_item.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{menu_item.name} is currently unavailable",
                )

            # Validate quantity
            if item_data.quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Quantity must be greater than zero",
                )

            # Calculate item total
            item_total = (
                menu_item.price * item_data.quantity
            )

            total += item_total

            order_item = OrderItem(
                menu_item_id=menu_item.id,
                quantity=item_data.quantity,
                unit_price=menu_item.price,
            )

            order.items.append(order_item)

        order.total_amount = total

        return OrderRepository.create_order(
            db,
            order,
        )

    @staticmethod
    def get_order(
        db: Session,
        order_id: int,
        current_user: User,
    ) -> Order:

        order = OrderRepository.get_by_id(
            db,
            order_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        # Customer can only view their own orders
        if current_user.role == "CUSTOMER":
            if order.customer_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to view this order",
                )

        # Restaurant admin can only view orders
        # belonging to their restaurant
        elif current_user.role == "RESTAURANT_ADMIN":

            restaurant = RestaurantRepository.get_by_id(
                db,
                order.restaurant_id,
            )

            if (
                restaurant is None
                or restaurant.owner_id != current_user.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to view this order",
                )

        # SYSTEM_ADMIN can view any order

        return order

    @staticmethod
    def get_my_orders(
        db: Session,
        current_user: User,
    ) -> list[Order]:

        if current_user.role != "CUSTOMER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can access this endpoint",
            )

        return OrderRepository.get_by_customer(
            db,
            current_user.id,
        )

    @staticmethod
    def update_status(
        db: Session,
        order_id: int,
        status_data: OrderStatusUpdate,
        current_user: User,
    ) -> Order:

        order = OrderRepository.get_by_id(
            db,
            order_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        # Customers cannot change order status
        if current_user.role == "CUSTOMER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Customers cannot update order status",
            )

        # Restaurant admins can only manage orders
        # belonging to their restaurant
        if current_user.role == "RESTAURANT_ADMIN":

            restaurant = RestaurantRepository.get_by_id(
                db,
                order.restaurant_id,
            )

            if (
                restaurant is None
                or restaurant.owner_id != current_user.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to update this order",
                )

        new_status = status_data.status

        allowed_statuses = ALLOWED_STATUS_TRANSITIONS.get(
            order.status,
            [],
        )
        current_status = order.status

        if new_status not in allowed_statuses.get(
            current_status,
            [],
        ):
            # System admin is allowed to bypass the normal workflow
            if current_user.role != "SYSTEM_ADMIN":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Cannot change order status "
                        f"from {current_status} to {new_status}"
                    ),
                )

        order.status = new_status

        return OrderRepository.save(
            db,
            order,
        )

    @staticmethod
    def cancel_order(
        db: Session,
        order_id: int,
        current_user: User,
    ) -> Order:

        order = OrderRepository.get_by_id(
            db,
            order_id,
        )

        if order is None:
                    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

        # Only the customer who placed the order can cancel it
        if (
            current_user.role != "CUSTOMER"
            or order.customer_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to cancel this order",
            )


        if order.status not in [
            OrderStatus.PENDING,
            OrderStatus.CONFIRMED,
        ]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Order cannot be cancelled when its status "
                    f"is {order.status}"
                )
            )

        order.status = OrderStatus.CANCELLED

        return OrderRepository.save(
            db,
            order,
        )
    