def test_login(client):
    # First create a user
    register_response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPassword123",
            "role": "CUSTOMER",
        },
    )

    assert register_response.status_code in [200, 201]

    # Then login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
