from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str
    role: str


class UserResponse(UserBase):
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)


class RestaurantBase(BaseModel):
    name: str
    address: str


class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(RestaurantBase):
    name: str | None = None
    address: str | None = None

class RestaurantResponse(RestaurantBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class MenuCategoryCreate(BaseModel):
    name: str

class MenuCategoryUpdate(BaseModel):
    name: str | None = None


class MenuCategoryResponse(BaseModel):
    id: int
    name: str
    restaurant_id: int

    model_config = ConfigDict(from_attributes=True)

class MenuItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    is_available: bool = True


class MenuItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    is_available: bool | None = None


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    is_available: bool
    category_id: int

    model_config = ConfigDict(from_attributes=True)
