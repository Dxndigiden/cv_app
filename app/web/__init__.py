from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.core.security import (
    create_access_token,
    decode_access_token,
    verify_password,
)
from app.crud.resume import get_resume, list_resumes
from app.crud.user import get_by_email
from app.db.session import get_session

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/login")
async def login_get(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request}
    )


@router.post("/login")
async def login_post(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    user = await get_by_email(db, email)
    if not user or not verify_password(
        password, user.hashed_password
    ):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"},
            status_code=401,
        )
    token = create_access_token(subject=str(user.id))
    # сохраняем токен в cookie (для простоты)
    response = RedirectResponse(url="/resumes", status_code=302)
    response.set_cookie("access_token", token, httponly=True)
    return response


@router.get("/resumes")
async def resumes_page(
    request: Request, db: AsyncSession = Depends(get_session)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/login")
    payload = decode_access_token(token)
    user_id = int(payload.get("sub"))
    resumes = await list_resumes(db, user_id)
    return templates.TemplateResponse(
        "resumes.html", {"request": request, "resumes": resumes}
    )
