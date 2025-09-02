from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.core.security import decode_access_token
from app.crud.resume import (
    create_resume,
    delete_resume,
    get_resume,
    list_resumes,
    update_resume,
)
from app.crud.user import get_by_id
from app.db.session import get_session
from app.schemas.resume import ResumeCreate

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


async def get_current_user(request: Request, db: AsyncSession):
    """Получает текущего пользователя по токену из cookie"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        return None
    return await get_by_id(db, user_id)


@router.get("/resumes", summary="Страница со списком резюме")
async def resumes_page(
    request: Request, db: AsyncSession = Depends(get_session)
):
    """Отображает страницу со списком всех резюме пользователя"""
    user = await get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    resumes = await list_resumes(db, user.id)
    return templates.TemplateResponse(
        "resumes.html",
        {"request": request, "resumes": resumes, "user": user},
    )


@router.post("/resumes", summary="Создание нового резюме")
async def create_resume_web(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    """Создаёт новое резюме для текущего пользователя"""
    user = await get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    resume_data = ResumeCreate(title=title, content=content)
    await create_resume(db, user.id, resume_data)
    return RedirectResponse("/resumes", status_code=302)


@router.post(
    "/resumes/{resume_id}/edit", summary="Редактирование резюме"
)
async def edit_resume_web(
    request: Request,
    resume_id: int,
    title: str = Form(...),
    content: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    """Редактирует выбранное резюме пользователя"""
    user = await get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    resume = await get_resume(db, resume_id, user.id)
    if not resume:
        return RedirectResponse("/resumes")
    await update_resume(
        db, resume, ResumeCreate(title=title, content=content)
    )
    return RedirectResponse("/resumes", status_code=302)


@router.post(
    "/resumes/{resume_id}/delete", summary="Удаление резюме"
)
async def delete_resume_web(
    resume_id: int,
    request: Request,
    db: AsyncSession = Depends(get_session),
):
    """Удаляет выбранное резюме пользователя"""
    user = await get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    resume = await get_resume(db, resume_id, user.id)
    if resume:
        await delete_resume(db, resume)
    return RedirectResponse("/resumes", status_code=302)


@router.post(
    "/resumes/{resume_id}/improve",
    summary="Улучшение резюме через AI",
)
async def improve_resume_web(
    resume_id: int,
    request: Request,
    db: AsyncSession = Depends(get_session),
):
    """Улучшает текст резюме с помощью AI и сохраняет историю изменений"""
    from app.utils.ai import improve_text

    user = await get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    resume = await get_resume(db, resume_id, user.id)
    if not resume:
        return RedirectResponse("/resumes")

    improved = await improve_text(resume.content)
    history = resume.improved_history or []
    history.append(
        {
            "ts": datetime.utcnow().isoformat() + "Z",
            "text": improved,
        }
    )
    resume.content = improved
    resume.improved_history = history
    await db.commit()
    await db.refresh(resume)
    return RedirectResponse("/resumes", status_code=302)
