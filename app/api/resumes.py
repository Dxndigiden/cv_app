from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

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
from app.schemas.resume import (
    ResumeCreate,
    ResumeOut,
    ResumeUpdate,
)
from app.utils.ai import improve_text

router = APIRouter(prefix="/api/resumes", tags=["Резюме"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session),
):
    """Получение текущего пользователя по JWT токену."""
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен",
        )

    user = await get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return user


@router.post(
    "", response_model=ResumeOut, summary="Создание нового резюме"
)
async def create_new_resume(
    payload: ResumeCreate,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    """Создает новое резюме для пользователя."""
    return await create_resume(db, user.id, payload)


@router.get(
    "",
    response_model=list[ResumeOut],
    summary="Список всех резюме пользователя",
)
async def get_my_resumes(
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    """Возвращает все резюме пользователя."""
    return await list_resumes(db, user.id)


@router.get(
    "/{resume_id}",
    response_model=ResumeOut,
    summary="Получение одного резюме",
)
async def get_one_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    """Возвращает резюме пользователя по ID."""
    resume = await get_resume(db, resume_id, user.id)
    if not resume:
        raise HTTPException(
            status_code=404, detail="Резюме не найдено"
        )
    return resume


@router.put(
    "/{resume_id}",
    response_model=ResumeOut,
    summary="Редактирование резюме",
)
async def edit_resume(
    resume_id: int,
    payload: ResumeUpdate,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    """Редактирует существующее резюме пользователя."""
    resume = await get_resume(db, resume_id, user.id)
    if not resume:
        raise HTTPException(
            status_code=404, detail="Резюме не найдено"
        )
    return await update_resume(db, resume, payload)


@router.delete(
    "/{resume_id}", status_code=204, summary="Удаление резюме"
)
async def remove_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    """Удаляет резюме пользователя."""
    resume = await get_resume(db, resume_id, user.id)
    if not resume:
        raise HTTPException(
            status_code=404, detail="Резюме не найдено"
        )
    await delete_resume(db, resume)
    return


@router.post(
    "/{resume_id}/improve",
    response_model=ResumeOut,
    summary="Улучшение резюме через AI",
)
async def improve_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    """Улучшает текст резюме с помощью AI(Заглушка)."""
    resume = await get_resume(db, resume_id, user.id)
    if not resume:
        raise HTTPException(
            status_code=404, detail="Резюме не найдено"
        )

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
    return resume
