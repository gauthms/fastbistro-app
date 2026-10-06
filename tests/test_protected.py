def test_authenticated_request(authenticated_client):
    response = authenticated_client.get(
        "/auth/me"
    )

    assert response.status_code == 200
