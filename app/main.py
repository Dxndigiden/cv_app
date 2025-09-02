from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import router as api_router
from app.web.web_router import router as web_router

app = FastAPI(
    title="Приложение для работы с резюме",
    description="API для работы с резюме",
    version="1.0.0",
    docs_url="/docs",
)

app.include_router(api_router)
app.include_router(web_router)

app.mount(
    "/static", StaticFiles(directory="app/static"), name="static"
)
