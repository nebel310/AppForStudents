from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, String, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Model




class UserOrm(Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default='student')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class RefreshTokenOrm(Model):
    __tablename__ = 'refresh_tokens'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class BlacklistedTokenOrm(Model):
    __tablename__ = 'blacklisted_tokens'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class InterestOrm(Model):
    __tablename__ = 'interests'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class SkillOrm(Model):
    __tablename__ = 'skills'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class UserInterestOrm(Model):
    __tablename__ = 'user_interests'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    interest_id: Mapped[int] = mapped_column(ForeignKey('interests.id'))


class UserSkillOrm(Model):
    __tablename__ = 'user_skills'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'))