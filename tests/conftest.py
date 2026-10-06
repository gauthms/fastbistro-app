import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.database import Base, get_db

from main import app

from fastapi.testclient import TestClient




test_engine = create_engine(
    settings.test_database_url,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def get_authenticated_client(client, email, password):
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    authenticated_client = TestClient(app)

    authenticated_client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return authenticated_client


@pytest.fixture
def db():
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPassword123",
            "role": "CUSTOMER",
        },
    )

    assert response.status_code in [200, 201]

    return response.json()


@pytest.fixture
def authenticated_client(client, test_user):
    return get_authenticated_client(
        client,
        test_user["email"],
        "TestPassword123",
    )

@pytest.fixture
def restaurant_admin_client(client):
    response = client.post(
        "/users",
        json={
            "name": "Restaurant Admin",
            "email": "admin@example.com",
            "password": "AdminPassword123",
            "role": "RESTAURANT_ADMIN",
        },
    )

    assert response.status_code in [200, 201]

    return get_authenticated_client(
        client,
        "admin@example.com",
        "AdminPassword123",
    )

@pytest.fixture
def second_restaurant_admin_client(client):
    response = client.post(
        "/users",
        json={
            "name": "Restaurant Admin 2",
            "email": "admin2@example.com",
            "password": "AdminPassword456",
            "role": "RESTAURANT_ADMIN",
        },
    )

    assert response.status_code in [200, 201]

    return get_authenticated_client(
        client,
        "admin2@example.com",
        "AdminPassword456",
    )

@pytest.fixture
def second_customer_client(client):
    response = client.post(
        "/users",
        json={
            "name": "Customer Two",
            "email": "customer2@example.com",
            "password": "CustomerPassword456",
            "role": "CUSTOMER",
        },
    )

    assert response.status_code in [200, 201]

    return get_authenticated_client(
        client,
        "customer2@example.com",
        "CustomerPassword456",
    )

