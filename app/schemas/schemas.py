from pydantic import BaseModel, ConfigDict


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