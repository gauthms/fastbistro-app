from fastapi import FastAPI

from app.api.routes import auth, users, restaurants


app = FastAPI(
    title="FastBistro API",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)


@app.get("/")
def root():
    return {"message": "FastBistro API is running"}
