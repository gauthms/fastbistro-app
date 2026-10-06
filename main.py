from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException

from app.api.routes import auth, users, restaurants, menu_categories, menu_items, orders


app = FastAPI(
    title="FastBistro API",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(menu_categories.router)
app.include_router(menu_categories.category_router)
app.include_router(menu_items.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {"message": "FastBistro API is running"}

@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )
