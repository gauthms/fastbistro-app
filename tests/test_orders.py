from decimal import Decimal

def test_customer_can_create_order(
    authenticated_client,
    restaurant_admin_client,
):
    # Create restaurant
    restaurant_response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "address": "Test restaurant",
        },
    )
    assert restaurant_response.status_code in [200, 201]
    restaurant = restaurant_response.json()

    # Create category
    category_response = restaurant_admin_client.post(
        f"/restaurants/{restaurant['id']}/categories",
        json={"name": "Main Course"},
    )
    assert category_response.status_code in [200, 201]
    category = category_response.json()

    # Create menu item
    menu_response = restaurant_admin_client.post(
        f"/categories/{category['id']}/items",
        json={
            "name": "Burger",
            "address": "Test burger",
            "price": 250,
            "is_available": True,
        },
    )
    assert menu_response.status_code in [200, 201]
    menu_item = menu_response.json()

    # Create order
    response = authenticated_client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant["id"],
            "items": [
                {
                    "menu_item_id": menu_item["id"],
                    "quantity": 2,
                }
            ],
        },
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["restaurant_id"] == restaurant["id"]
    assert data["status"] == "PENDING"
    assert Decimal(data["total_amount"]) == Decimal("500.00")

def test_create_order_invalid_restaurant(
    authenticated_client,
):
    response = authenticated_client.post(
        "/orders/",
        json={
            "restaurant_id": 99999,
            "items": [
                {
                    "menu_item_id": 1,
                    "quantity": 1,
                }
            ],
        },
    )

    assert response.status_code == 404


def test_menu_item_from_another_restaurant(
    authenticated_client,
    restaurant_admin_client,
    second_restaurant_admin_client,
):
    # Restaurant 1 + menu item
    restaurant_response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Restaurant One",
            "address": "Test restaurant",
        },
    )
    assert restaurant_response.status_code in [200, 201]
    restaurant_1 = restaurant_response.json()

    category_response = restaurant_admin_client.post(
        f"/restaurants/{restaurant_1['id']}/categories",
        json={"name": "Main Course"},
    )
    assert category_response.status_code in [200, 201]
    category = category_response.json()

    menu_response = restaurant_admin_client.post(
        f"/categories/{category['id']}/items",
        json={
            "name": "Burger",
            "address": "Test burger",
            "price": 250,
            "is_available": True,
        },
    )
    assert menu_response.status_code in [200, 201]
    menu_item = menu_response.json()

    # Restaurant 2
    restaurant_response = second_restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Restaurant Two",
            "address": "Test restaurant",
        },
    )
    assert restaurant_response.status_code in [200, 201]
    restaurant_2 = restaurant_response.json()

    # Try using Restaurant 1's menu item for Restaurant 2
    response = authenticated_client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant_2["id"],
            "items": [
                {
                    "menu_item_id": menu_item["id"],
                    "quantity": 1,
                }
            ],
        },
    )

    assert response.status_code == 400


def test_customer_can_view_own_order(
    authenticated_client,
    restaurant_admin_client,
):
    restaurant_response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "address": "Test restaurant",
        },
    )
    restaurant = restaurant_response.json()

    category_response = restaurant_admin_client.post(
        f"/restaurants/{restaurant['id']}/categories",
        json={"name": "Main Course"},
    )
    category = category_response.json()

    menu_response = restaurant_admin_client.post(
        f"/categories/{category['id']}/items",
        json={
            "name": "Burger",
            "address": "Test burger",
            "price": 250,
            "is_available": True,
        },
    )
    menu_item = menu_response.json()

    order_response = authenticated_client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant["id"],
            "items": [
                {
                    "menu_item_id": menu_item["id"],
                    "quantity": 1,
                }
            ],
        },
    )

    order = order_response.json()

    response = authenticated_client.get(
        f"/orders/{order['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == order["id"]


def test_customer_cannot_view_another_customer_order(
    authenticated_client,
    second_customer_client,
    restaurant_admin_client,
):
    restaurant_response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "address": "Test restaurant",
        },
    )
    restaurant = restaurant_response.json()

    category_response = restaurant_admin_client.post(
        f"/restaurants/{restaurant['id']}/categories",
        json={"name": "Main Course"},
    )
    category = category_response.json()

    menu_response = restaurant_admin_client.post(
        f"/categories/{category['id']}/items",
        json={
            "name": "Burger",
            "address": "Test burger",
            "price": 250,
            "is_available": True,
        },
    )
    menu_item = menu_response.json()

    order_response = authenticated_client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant["id"],
            "items": [
                {
                    "menu_item_id": menu_item["id"],
                    "quantity": 1,
                }
            ],
        },
    )

    order = order_response.json()

    response = second_customer_client.get(
        f"/orders/{order['id']}"
    )

    assert response.status_code == 403


def test_restaurant_admin_can_update_order_status(
    authenticated_client,
    restaurant_admin_client,
):
    restaurant_response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "address": "Test restaurant",
        },
    )
    restaurant = restaurant_response.json()

    category_response = restaurant_admin_client.post(
        f"/restaurants/{restaurant['id']}/categories",
        json={"name": "Main Course"},
    )
    category = category_response.json()

    menu_response = restaurant_admin_client.post(
        f"/categories/{category['id']}/items",
        json={
            "name": "Burger",
            "address": "Test burger",
            "price": 250,
            "is_available": True,
        },
    )
    menu_item = menu_response.json()

    order_response = authenticated_client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant["id"],
            "items": [
                {
                    "menu_item_id": menu_item["id"],
                    "quantity": 1,
                }
            ],
        },
    )

    order = order_response.json()

    response = restaurant_admin_client.patch(
        f"/orders/{order['id']}/status",
        json={"status": "CONFIRMED"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CONFIRMED"


def test_invalid_order_status_transition(
    authenticated_client,
    restaurant_admin_client,
):
    restaurant_response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "address": "Test restaurant",
        },
    )
    restaurant = restaurant_response.json()

    category_response = restaurant_admin_client.post(
        f"/restaurants/{restaurant['id']}/categories",
        json={"name": "Main Course"},
    )
    category = category_response.json()

    menu_response = restaurant_admin_client.post(
        f"/categories/{category['id']}/items",
        json={
            "name": "Burger",
            "address": "Test burger",
            "price": 250,
            "is_available": True,
        },
    )
    menu_item = menu_response.json()

def test_customer_can_cancel_own_order(
    authenticated_client,
    restaurant_admin_client,
):
    restaurant_response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "address": "Test restaurant",
        },
    )
    restaurant = restaurant_response.json()

    category_response = restaurant_admin_client.post(
        f"/restaurants/{restaurant['id']}/categories",
        json={"name": "Main Course"},
    )
    category = category_response.json()

    menu_response = restaurant_admin_client.post(
        f"/categories/{category['id']}/items",
        json={
            "name": "Burger",
            "address": "Test burger",
            "price": 250,
            "is_available": True,
        },
    )
    menu_item = menu_response.json()

    order_response = authenticated_client.post(
        "/orders/",
        json={
            "restaurant_id": restaurant["id"],
            "items": [
                {
                    "menu_item_id": menu_item["id"],
                    "quantity": 1,
                }
            ],
        },
    )

    order = order_response.json()

    response = authenticated_client.patch(
        f"/orders/{order['id']}/cancel"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"
