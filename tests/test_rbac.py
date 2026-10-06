def test_customer_cannot_update_restaurant(
    authenticated_client,
    restaurant_admin_client,
):
    # Create restaurant as restaurant admin
    response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Test Restaurant",
            "address": "Test somewhere",
        },
    )

    assert response.status_code in [200, 201]

    restaurant = response.json()
    restaurant_id = restaurant["id"]

    # Customer tries to update it
    response = authenticated_client.put(
        f"/restaurants/{restaurant_id}",
        json={
            "name": "Unauthorized Update",
        },
    )

    assert response.status_code == 403


def test_admin_cannot_update_another_restaurant(
    restaurant_admin_client,
    second_restaurant_admin_client,
):
    # Admin A creates Restaurant A
    response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Restaurant A",
            "address": "Downtown",
        },
    )

    assert response.status_code in [200, 201]

    restaurant_a = response.json()

    # Admin B creates Restaurant B
    response = second_restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Restaurant B",
            "address": "Uptown",
        },
    )

    assert response.status_code in [200, 201]

    restaurant_b = response.json()

    # Admin A tries to update Restaurant B
    response = restaurant_admin_client.put(
        f"/restaurants/{restaurant_b['id']}",
        json={
            "name": "Restaurant A1",
            "address": "somewhere downtown",
        },
    )

    assert response.status_code == 403

def test_admin_can_update_own_restaurant(
    restaurant_admin_client,
):
    response = restaurant_admin_client.post(
        "/restaurants/",
        json={
            "name": "Restaurant A",
            "address": "somewhere"
        },
    )

    assert response.status_code in [200, 201]

    restaurant = response.json()

    response = restaurant_admin_client.put(
        f"/restaurants/{restaurant['id']}",
        json={
            "name": "Restaurant A1",
            "address": "London"
        },
    )

    assert response.status_code == 200
