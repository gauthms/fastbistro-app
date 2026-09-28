from fastapi import FastAPI

from app.api.routes import auth, users, restaurants, menu_categories, menu_items


app = FastAPI(
    title="FastBistro API",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(menu_categories.router)
app.include_router(menu_categories.category_router)
app.include_router(menu_items.router)


@app.get("/")
def root():
    return {"message": "FastBistro API is running"}
