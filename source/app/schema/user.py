from fastapi_users.models import BaseUser, BaseUserCreate, BaseUserDB, BaseUserUpdate


class UserBase(BaseUser):
    pass


class UserCreate(BaseUserCreate):
    pass


class UserUpdate(BaseUserUpdate):
    pass


class UserResponse(BaseUserDB):
    pass
