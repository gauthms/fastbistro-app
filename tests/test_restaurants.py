def test_get_restaurants(client):
    response = client.get("/restaurants/")

    assert response.status_code == 200
