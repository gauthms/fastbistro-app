from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.schemas import UserCreate, UserResponse

from app.core.permissions import system_admin_required



router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users

@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(system_admin_required),
):
    return {
        "message": "You are a system admin",
        "user_id": current_user.id,
    }


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    hashed_password = hash_password(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=user.role,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



