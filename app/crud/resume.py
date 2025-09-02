from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate


async def create_resume(
    db: AsyncSession, user_id: int, data: ResumeCreate
):
    """Создает новое резюме для пользователя."""
    resume = Resume(
        user_id=user_id,
        title=data.title,
        content=data.content,
        improved_history=[],
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    return resume


async def list_resumes(db: AsyncSession, user_id: int):
    """Возвращает все резюме пользователя."""
    result = await db.execute(
        select(Resume)
        .where(Resume.user_id == user_id)
        .order_by(Resume.id.desc())
    )
    return result.scalars().all()


async def get_resume(
    db: AsyncSession, resume_id: int, user_id: int
):
    """Возвращает одно резюме пользователя по ID."""
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id, Resume.user_id == user_id
        )
    )
    return result.scalars().first()


async def update_resume(
    db: AsyncSession, resume: Resume, data: ResumeUpdate
):
    """Обновляет резюме пользователя."""
    if data.title is not None:
        resume.title = data.title
    if data.content is not None:
        resume.content = data.content
    await db.commit()
    await db.refresh(resume)
    return resume


async def delete_resume(db: AsyncSession, resume: Resume):
    """Удаляет резюме пользователя."""
    await db.delete(resume)
    await db.commit()
