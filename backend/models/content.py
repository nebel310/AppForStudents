from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Model




class NewsOrm(Model):
    __tablename__ = 'news'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    main_text: Mapped[str] = mapped_column(Text, nullable=False)
    image_url1: Mapped[str] = mapped_column(String(255), nullable=True)
    image_url2: Mapped[str] = mapped_column(String(255), nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class NewsLikeOrm(Model):
    __tablename__ = 'news_likes'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    news_id: Mapped[int] = mapped_column(ForeignKey('news.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CaseOrm(Model):
    __tablename__ = 'cases'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    main_text: Mapped[str] = mapped_column(Text, nullable=False)
    image_url1: Mapped[str] = mapped_column(String(255), nullable=True)
    image_url2: Mapped[str] = mapped_column(String(255), nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    tags: Mapped[str] = mapped_column(String(255), nullable=True)
    participants_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CaseParticipantOrm(Model):
    __tablename__ = 'case_participants'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey('cases.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class VacancyOrm(Model):
    __tablename__ = 'vacancies'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    main_text: Mapped[str] = mapped_column(Text, nullable=False)
    image_url1: Mapped[str] = mapped_column(String(255), nullable=True)
    image_url2: Mapped[str] = mapped_column(String(255), nullable=True)
    tags: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class VacancyApplicationOrm(Model):
    __tablename__ = 'vacancy_applications'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))