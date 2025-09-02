from fastapi import APIRouter

from app.api import resumes, users

router = APIRouter()
router.include_router(users.router)
router.include_router(resumes.router)
