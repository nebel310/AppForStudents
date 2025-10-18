from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional




class SNewsBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="Новая конференция по AI", description="Заголовок новости")
    author: str = Field(..., min_length=1, max_length=100, example="Компания Яндекс", description="Автор новости")
    main_text: str = Field(..., example="Текст новости...", description="Основной текст новости")
    image_url1: Optional[str] = Field(None, example="http://example.com/image1.jpg", description="URL первого изображения")
    image_url2: Optional[str] = Field(None, example="http://example.com/image2.jpg", description="URL второго изображения")
    start_date: datetime = Field(..., example="2024-01-01T10:00:00Z", description="Дата и время начала")
    end_date: datetime = Field(..., example="2024-01-01T18:00:00Z", description="Дата и время окончания")
    address: str = Field(..., example="Москва, ул. Примерная, 1", description="Адрес проведения")


class SNewsCreate(SNewsBase):
    pass


class SNews(SNewsBase):
    id: int = Field(..., example=1, description="ID новости")
    likes_count: int = Field(..., example=5, description="Количество лайков")
    created_at: datetime = Field(..., example="2024-01-01T00:00:00Z", description="Дата создания")

    model_config = ConfigDict(from_attributes=True)


class SCaseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="Кейс по разработке мобильного приложения", description="Название кейса")
    author: str = Field(..., min_length=1, max_length=100, example="Компания VK", description="Автор кейса")
    main_text: str = Field(..., example="Описание кейса...", description="Основной текст кейса")
    image_url1: Optional[str] = Field(None, example="http://example.com/image1.jpg", description="URL первого изображения")
    image_url2: Optional[str] = Field(None, example="http://example.com/image2.jpg", description="URL второго изображения")
    start_date: datetime = Field(..., example="2024-01-01T10:00:00Z", description="Дата и время начала")
    end_date: datetime = Field(..., example="2024-01-01T18:00:00Z", description="Дата и время окончания")
    address: str = Field(..., example="Москва, ул. Примерная, 1", description="Адрес проведения")
    tags: Optional[str] = Field(None, example="программирование, дизайн", description="Теги кейса")


class SCaseCreate(SCaseBase):
    pass


class SCase(SCaseBase):
    id: int = Field(..., example=1, description="ID кейса")
    participants_count: int = Field(..., example=15, description="Количество участников")
    created_at: datetime = Field(..., example="2024-01-01T00:00:00Z", description="Дата создания")

    model_config = ConfigDict(from_attributes=True)


class SVacancyBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="Стажер-разработчик Python", description="Название вакансии")
    author: str = Field(..., min_length=1, max_length=100, example="Компания Тинькофф", description="Автор вакансии")
    main_text: str = Field(..., example="Описание вакансии...", description="Основной текст вакансии")
    image_url1: Optional[str] = Field(None, example="http://example.com/image1.jpg", description="URL первого изображения")
    image_url2: Optional[str] = Field(None, example="http://example.com/image2.jpg", description="URL второго изображения")
    tags: Optional[str] = Field(None, example="python, django, postgresql", description="Теги вакансии")


class SVacancyCreate(SVacancyBase):
    pass


class SVacancy(SVacancyBase):
    id: int = Field(..., example=1, description="ID вакансии")
    created_at: datetime = Field(..., example="2024-01-01T00:00:00Z", description="Дата создания")

    model_config = ConfigDict(from_attributes=True)


class SParticipationResponse(BaseModel):
    success: bool = Field(..., example=True, description="Успех операции")
    participants_count: int = Field(..., example=16, description="Новое количество участников")


class SApplicationResponse(BaseModel):
    success: bool = Field(..., example=True, description="Успех операции")
    application_id: int = Field(..., example=1, description="ID заявки")


class SLikeResponse(BaseModel):
    success: bool = Field(..., example=True, description="Успех операции")
    likes_count: int = Field(..., example=6, description="Новое количество лайков")