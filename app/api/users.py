from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.crud.user import create_user, get_by_email
from app.db.session import get_session
from app.schemas.user import Token, UserCreate, UserOut

router = APIRouter(prefix="/api/users", tags=["Пользователи"])


@router.post(
    "/register",
    response_model=UserOut,
    summary="Регистрация нового пользователя",
)
async def register(
    user_in: UserCreate, db: AsyncSession = Depends(get_session)
):
    """Регистрация пользователя с email и паролем. Проверяет уникальность email."""
    existing_user = await get_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован",
        )
    user = await create_user(db, user_in)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Авторизация и получение JWT",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    """Авторизация пользователя и выдача JWT для последующих запросов."""
    user = await get_by_email(db, form_data.username)
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
