from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.core.security import create_access_token, verify_password
from app.crud.user import get_by_email
from app.db.session import get_session

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/login", summary="Страница входа")
async def login_get(request: Request):
    """Отображает страницу входа"""
    return templates.TemplateResponse(
        "login.html", {"request": request}
    )


@router.post(
    "/login", summary="Авторизация пользователя через форму"
)
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    """Обрабатывает форму входа и создает токен в cookie"""
    user = await get_by_email(db, email)
    if not user or not verify_password(
        password, user.hashed_password
    ):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Неверный email или пароль",
            },
            status_code=401,
        )

    token = create_access_token(subject=str(user.id))
    redirect = RedirectResponse(url="/resumes", status_code=302)
    redirect.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        secure=False,
    )
    return redirect
