# FastBistro API

A RESTful backend API for a restaurant ordering platform, built with **Python, FastAPI, PostgreSQL, and SQLAlchemy**.

The project implements authentication, role-based access control, restaurant and menu management, order processing, status workflows, database migrations, automated testing, and Docker-based deployment.

## 🚀 Live Demo

- **Live API Documentation (Swagger UI):** [Explore FastBistro API](https://fastbistro-app.onrender.com/docs)
- **Deployment Platform:** Render

## Features

- JWT-based authentication
- Password hashing with Argon2
- Role-based access control (RBAC)
- Restaurant management
- Menu category management
- Menu item management
- Restaurant-specific menu validation
- Order creation and retrieval
- Order status workflow
- Order cancellation
- Pagination for list endpoints
- Service/repository architecture
- Custom application exceptions
- PostgreSQL database
- Alembic database migrations
- Automated API tests with pytest
- Dockerized FastAPI and PostgreSQL services

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| Pydantic | Request/response validation |
| JWT | Authentication |
| Argon2 | Password hashing |
| pytest | Automated testing |
| Docker | Containerization |
| Docker Compose | Local service orchestration |

## Architecture

The application follows a layered architecture:

```text
Client
  │
  ▼
FastAPI Routes
  │
  ├── Authentication / Permissions
  │
  ▼
Services
  │
  ▼
Repositories
  │
  ▼
SQLAlchemy
  │
  ▼
PostgreSQL
```

### Responsibilities

**Routes**

Handle HTTP requests, authentication dependencies, request validation, and responses.

**Services**

Contain business logic and application rules.

**Repositories**

Handle database persistence and queries.

**Models**

Represent database entities using SQLAlchemy.

**Schemas**

Define and validate API request and response data using Pydantic.

## Project Structure

```text
fastbistro/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── menu_categories.py
│   │       ├── menu_items.py
│   │       ├── orders.py
│   │       ├── restaurants.py
│   │       └── users.py
│   │
│   ├── core/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── permissions.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models/
│   │
│   ├── repositories/
│   ├── schemas/
│   └── services/
│
├── alembic/
│   └── versions/
│
├── tests/
│
├── main.py
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

## Authentication & Authorization

The API uses JWT-based authentication.

Passwords are securely hashed using Argon2 before being stored.

The application supports three roles:

- `CUSTOMER`
- `RESTAURANT_ADMIN`
- `SYSTEM_ADMIN`

Access to protected operations is controlled through role-based permissions and resource ownership.

For example:

- Customers can create and manage their own orders.
- Restaurant administrators can manage their restaurants and associated orders.
- System administrators have broader administrative access.

## Order Workflow

Orders follow a controlled status workflow:

```text
PENDING
   │
   ▼
CONFIRMED
   │
   ▼
PREPARING
   │
   ▼
READY
   │
   ▼
COMPLETED
```

Orders can also be cancelled when permitted by the business rules.

The service layer validates status transitions before updating an order.

When an order is created:

- The restaurant must exist.
- Menu items must exist.
- Menu items must belong to the selected restaurant.
- Menu items must be available.
- Quantity must be valid.
- Prices are taken from the current menu item data.
- The order total is calculated server-side.

## Database Migrations

Alembic is used to manage database schema changes.

Run migrations with:

```bash
alembic upgrade head
```

When running the application through Docker:

```bash
docker compose exec api alembic upgrade head
```

## Running with Docker

### Prerequisites

- Docker
- Docker Compose

### Start the application

```bash
docker compose up -d --build
```

Run the database migrations:

```bash
docker compose exec api alembic upgrade head
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

To stop the application:

```bash
docker compose down
```

## Running Tests

The project includes automated tests covering authentication, authorization, restaurants, and order workflows.

Run the complete test suite with:

```bash
pytest -v
```

The test suite uses a separate PostgreSQL test database to avoid affecting development data.

## API Documentation

FastAPI automatically generates interactive OpenAPI documentation.

Once the application is running, visit:

```text
http://localhost:8000/docs
```

The Swagger UI can be used to explore and test the available endpoints.

## Testing Coverage

The order test suite covers core scenarios including:

- Successful order creation
- Invalid restaurant validation
- Cross-restaurant menu item validation
- Order retrieval
- Customer ownership authorization
- Restaurant administrator status updates
- Invalid status transitions
- Order cancellation

## Future Improvements

Potential future improvements include:

- Automated Docker image publishing
- Refresh tokens
- Rate limiting
- Structured logging
- More comprehensive integration testing
- Payment integration
- Order notifications

## License

This project is intended as a personal portfolio and learning project.
