from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Схема для регистрации нового пользователя."""

    email: EmailStr = Field(..., title="Email пользователя")
    password: str = Field(..., title="Пароль")


class UserOut(BaseModel):
    """Схема для вывода информации о пользователе через API."""

    id: int
    email: EmailStr
    is_active: bool = True

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Схема для JWT-токена пользователя."""

    access_token: str
    token_type: str = "bearer"
