from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from datetime import datetime
from typing import List, Optional
from enum import Enum




class UserRole(str, Enum):
    STUDENT = "student"
    RECRUITER = "recruiter"


class SUserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="john_doe", description="Имя пользователя")
    email: EmailStr = Field(..., example="user@example.com", description="Email пользователя")
    password: str = Field(..., min_length=6, example="password123", description="Пароль")
    password_confirm: str = Field(..., min_length=6, example="password123", description="Подтверждение пароля")

    @field_validator('password_confirm')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Пароли не совпадают')
        return v


class SUserLogin(BaseModel):
    email: EmailStr = Field(..., example="user@example.com", description="Email пользователя")
    password: str = Field(..., min_length=6, example="password123", description="Пароль")


class SUser(BaseModel):
    id: int = Field(..., example=1, description="ID пользователя")
    username: str = Field(..., example="john_doe", description="Имя пользователя")
    email: EmailStr = Field(..., example="user@example.com", description="Email пользователя")
    role: UserRole = Field(..., example=UserRole.STUDENT, description="Роль пользователя")
    created_at: datetime = Field(..., example="2024-01-01T00:00:00Z", description="Дата создания")

    model_config = ConfigDict(from_attributes=True)


class SUserProfile(SUser):
    avatar_url: Optional[str] = Field(None, example="https://example.com/avatar.jpg", description="URL аватара")
    rating: float = Field(..., example=4.5, description="Рейтинг пользователя")
    achievements: List[str] = Field(default=[], example=["Победитель хакатона", "Активный участник"], description="Достижения пользователя")
    skills: List[str] = Field(default=[], example=["Python", "JavaScript"], description="Навыки пользователя")
    cases: List[str] = Field(default=[], example=["Кейс 1", "Кейс 2"], description="Кейсы пользователя")
    clubs: List[str] = Field(default=[], example=["Клуб разработчиков", "Клуб дизайнеров"], description="Клубы пользователя")


class SUserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, example="new_username", description="Новое имя пользователя")
    avatar_url: Optional[str] = Field(None, example="https://example.com/new_avatar.jpg", description="Новый URL аватара")


class SUserRoleUpdate(BaseModel):
    role: UserRole = Field(..., example=UserRole.STUDENT, description="Новая роль пользователя")


class SInterest(BaseModel):
    id: int = Field(..., example=1, description="ID интереса")
    name: str = Field(..., example="Программирование", description="Название интереса")

    model_config = ConfigDict(from_attributes=True)


class SSkill(BaseModel):
    id: int = Field(..., example=1, description="ID навыка")
    name: str = Field(..., example="Python", description="Название навыка")

    model_config = ConfigDict(from_attributes=True)


class SUserInterestsUpdate(BaseModel):
    interest_ids: List[int] = Field(..., example=[1, 2, 3], description="Список ID интересов")


class SUserSkillsUpdate(BaseModel):
    skill_ids: List[int] = Field(..., example=[1, 2, 3], description="Список ID навыков")


class SUserWithInterestsSkills(SUser):
    interests: List[SInterest] = Field(default=[], description="Интересы пользователя")
    skills: List[SSkill] = Field(default=[], description="Навыки пользователя")