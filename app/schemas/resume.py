from typing import Any, List, Optional

from pydantic import BaseModel, Field


class ResumeCreate(BaseModel):
    """Схема для создания нового резюме."""

    title: str = Field(
        ...,
        title="Название резюме",
        description="Краткое название вашего резюме",
    )
    content: str = Field(
        ...,
        title="Описание",
        description="Подробное описание резюме",
    )


class ResumeUpdate(BaseModel):
    """Схема для обновления существующего резюме."""

    title: Optional[str] = None
    content: Optional[str] = None


class ResumeOut(BaseModel):
    """Схема для вывода резюме через API."""

    id: int
    title: str
    content: str
    improved_history: List[Any] = Field(default_factory=list)

    class Config:
        from_attributes = True
