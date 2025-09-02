from fastapi import APIRouter
from starlette.responses import RedirectResponse

from .login_views import router as login_router
from .register_views import router as register_router
from .resume_views import router as resume_router

router = APIRouter(tags=["Фронт"])


@router.get("/", summary="Перенаправляет на страницу входа")
async def root_redirect():
    """Редирект на страницу логина"""
    return RedirectResponse(url="/login")


router.include_router(login_router)
router.include_router(register_router)
router.include_router(resume_router)
