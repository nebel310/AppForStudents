from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Model




class ClubOrm(Model):
    __tablename__ = 'clubs'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_url1: Mapped[str] = mapped_column(String(255), nullable=True)
    image_url2: Mapped[str] = mapped_column(String(255), nullable=True)
    tags: Mapped[str] = mapped_column(String(255), nullable=True)
    target_audience: Mapped[str] = mapped_column(String(255), nullable=True)
    members_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ClubMemberOrm(Model):
    __tablename__ = 'club_members'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    club_id: Mapped[int] = mapped_column(ForeignKey('clubs.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    role: Mapped[str] = mapped_column(String(20), default='member')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))