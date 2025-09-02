from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.crud.user import create_user, get_by_email
from app.db.session import get_session
from app.schemas.user import UserCreate

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/register", summary="Страница регистрации")
async def register_get(request: Request):
    """Показывает страницу регистрации"""
    return templates.TemplateResponse(
        "register.html", {"request": request}
    )


@router.post(
    "/register",
    summary="Регистрация нового пользователя через форму",
)
async def register_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    """Обрабатывает форму регистрации нового пользователя"""
    if password != password2:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Пароли не совпадают"},
            status_code=400,
        )

    existing_user = await get_by_email(db, email)
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Пользователь с таким email уже существует",
            },
            status_code=400,
        )

    user_in = UserCreate(email=email, password=password)
    await create_user(db, user_in)
    return RedirectResponse(url="/login", status_code=302)
