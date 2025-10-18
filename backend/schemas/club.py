from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional




class SClubBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="Клуб разработчиков Python", description="Название клуба")
    description: Optional[str] = Field(None, example="Сообщество для Python-разработчиков", description="Описание клуба")
    image_url1: Optional[str] = Field(None, example="https://example.com/club1.jpg", description="URL первого изображения")
    image_url2: Optional[str] = Field(None, example="https://example.com/club2.jpg", description="URL второго изображения")
    tags: Optional[str] = Field(None, example="python, разработка, программирование", description="Теги клуба")
    target_audience: Optional[str] = Field(None, example="Разработчики, Студенты", description="Целевая аудитория")


class SClubCreate(SClubBase):
    pass


class SClub(SClubBase):
    id: int = Field(..., example=1, description="ID клуба")
    members_count: int = Field(..., example=15, description="Количество участников")
    created_at: datetime = Field(..., example="2024-01-01T00:00:00Z", description="Дата создания")

    model_config = ConfigDict(from_attributes=True)


class SClubDetail(SClub):
    members: List[dict] = Field(..., example=[{"id": 1, "username": "user1", "avatar_url": "https://example.com/avatar.jpg", "rating": 4.5}], description="Участники клуба")


class SClubMember(BaseModel):
    id: int = Field(..., example=1, description="ID пользователя")
    username: str = Field(..., example="john_doe", description="Имя пользователя")
    avatar_url: Optional[str] = Field(None, example="https://example.com/avatar.jpg", description="URL аватара")
    rating: float = Field(..., example=4.5, description="Рейтинг пользователя")


class SClubJoinResponse(BaseModel):
    success: bool = Field(..., example=True, description="Успех операции")
    members_count: int = Field(..., example=16, description="Новое количество участников")


class SClubLeaveResponse(BaseModel):
    success: bool = Field(..., example=True, description="Успех операции")
    members_count: int = Field(..., example=15, description="Новое количество участников")