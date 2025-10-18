from database import new_session
from models.club import ClubOrm, ClubMemberOrm
from models.users import UserOrm
from schemas.club import SClubCreate
from sqlalchemy import select, delete, insert, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError




class ClubRepository:
    @classmethod
    async def get_all_clubs(cls, limit: int = 20, offset: int = 0) -> list[ClubOrm]:
        async with new_session() as session:
            try:
                query = select(ClubOrm).order_by(ClubOrm.created_at.desc()).limit(limit).offset(offset)
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении клубов") from e

    @classmethod
    async def get_club_by_id(cls, club_id: int) -> ClubOrm:
        async with new_session() as session:
            try:
                query = select(ClubOrm).where(ClubOrm.id == club_id)
                result = await session.execute(query)
                club = result.scalars().first()
                
                if not club:
                    raise ValueError("Клуб не найден")
                
                return club
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении клуба") from e

    @classmethod
    async def get_club_with_members(cls, club_id: int) -> dict:
        """Получение клуба с информацией об участниках"""
        async with new_session() as session:
            try:
                # Получаем клуб
                club_query = select(ClubOrm).where(ClubOrm.id == club_id)
                club_result = await session.execute(club_query)
                club = club_result.scalars().first()
                
                if not club:
                    raise ValueError("Клуб не найден")

                # Получаем участников клуба
                members_query = (
                    select(UserOrm)
                    .join(ClubMemberOrm, ClubMemberOrm.user_id == UserOrm.id)
                    .where(ClubMemberOrm.club_id == club_id)
                )
                members_result = await session.execute(members_query)
                members = members_result.scalars().all()

                return {
                    "club": club,
                    "members": members
                }
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении клуба с участниками") from e

    @classmethod
    async def create_club(cls, club_data: SClubCreate, user_id: int) -> ClubOrm:
        async with new_session() as session:
            try:
                club = ClubOrm(**club_data.model_dump())
                session.add(club)
                await session.flush()

                # Создатель автоматически становится участником
                club_member = ClubMemberOrm(
                    club_id=club.id,
                    user_id=user_id,
                    role='admin'
                )
                session.add(club_member)

                # Обновляем счетчик участников
                club.members_count = 1

                await session.commit()
                await session.refresh(club)
                return club
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при создании клуба") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при создании клуба") from e

    @classmethod
    async def join_club(cls, club_id: int, user_id: int) -> int:
        async with new_session() as session:
            try:
                # Проверяем, состоит ли уже пользователь в клубе
                member_query = select(ClubMemberOrm).where(
                    ClubMemberOrm.club_id == club_id,
                    ClubMemberOrm.user_id == user_id
                )
                result = await session.execute(member_query)
                existing_member = result.scalars().first()

                if existing_member:
                    raise ValueError("Вы уже состоите в этом клубе")

                # Добавляем пользователя в клуб
                club_member = ClubMemberOrm(
                    club_id=club_id,
                    user_id=user_id
                )
                session.add(club_member)

                # Обновляем счетчик участников
                update_query = update(ClubOrm).where(ClubOrm.id == club_id).values(
                    members_count=ClubOrm.members_count + 1
                )
                await session.execute(update_query)

                await session.commit()

                # Получаем обновленное количество участников
                club_query = select(ClubOrm.members_count).where(ClubOrm.id == club_id)
                result = await session.execute(club_query)
                return result.scalar()
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при вступлении в клуб") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при вступлении в клуб") from e

    @classmethod
    async def leave_club(cls, club_id: int, user_id: int) -> int:
        async with new_session() as session:
            try:
                # Проверяем, состоит ли пользователь в клубе
                member_query = select(ClubMemberOrm).where(
                    ClubMemberOrm.club_id == club_id,
                    ClubMemberOrm.user_id == user_id
                )
                result = await session.execute(member_query)
                existing_member = result.scalars().first()

                if not existing_member:
                    raise ValueError("Вы не состоите в этом клубе")

                # Удаляем пользователя из клуба
                delete_query = delete(ClubMemberOrm).where(
                    ClubMemberOrm.club_id == club_id,
                    ClubMemberOrm.user_id == user_id
                )
                await session.execute(delete_query)

                # Обновляем счетчик участников
                update_query = update(ClubOrm).where(ClubOrm.id == club_id).values(
                    members_count=ClubOrm.members_count - 1
                )
                await session.execute(update_query)

                await session.commit()

                # Получаем обновленное количество участников
                club_query = select(ClubOrm.members_count).where(ClubOrm.id == club_id)
                result = await session.execute(club_query)
                return result.scalar()
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при выходе из клуба") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при выходе из клуба") from e

    @classmethod
    async def get_user_clubs(cls, user_id: int) -> list[ClubOrm]:
        """Получение клубов, в которых состоит пользователь"""
        async with new_session() as session:
            try:
                query = (
                    select(ClubOrm)
                    .join(ClubMemberOrm, ClubMemberOrm.club_id == ClubOrm.id)
                    .where(ClubMemberOrm.user_id == user_id)
                )
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении клубов пользователя") from e

    @classmethod
    async def init_test_clubs(cls):
        """Инициализация тестовых клубов"""
        async with new_session() as session:
            try:
                # Тестовые клубы
                clubs_list = [
                    {
                        "title": "Клуб разработчиков Python",
                        "description": "Сообщество для Python-разработчиков всех уровней. Обсуждаем лучшие практики, делимся опытом и работаем над проектами вместе.",
                        "image_url1": "https://example.com/python_club1.jpg",
                        "image_url2": "https://example.com/python_club2.jpg",
                        "tags": "python, разработка, программирование, django, flask",
                        "target_audience": "Разработчики, Студенты, Начинающие",
                        "members_count": 45
                    },
                    {
                        "title": "Сообщество UI/UX дизайнеров",
                        "description": "Профессиональное сообщество дизайнеров интерфейсов. Проводим воркшопы, обсуждаем тренды и помогаем друг другу расти.",
                        "image_url1": "https://example.com/design_club1.jpg",
                        "image_url2": "https://example.com/design_club2.jpg",
                        "tags": "дизайн, ui/ux, figma, adobe xd, интерфейсы",
                        "target_audience": "Дизайнеры, UX-исследователи, Продукт-менеджеры",
                        "members_count": 32
                    },
                    {
                        "title": "Data Science Hub",
                        "description": "Клуб для специалистов по анализу данных и машинному обучению. Изучаем новые алгоритмы, участвуем в соревнованиях Kaggle.",
                        "image_url1": "https://example.com/ds_club1.jpg",
                        "image_url2": None,
                        "tags": "data science, machine learning, python, аналитика",
                        "target_audience": "Аналитики, Data Scientists, Исследователи",
                        "members_count": 28
                    },
                    {
                        "title": "Клуб мобильной разработки",
                        "description": "Сообщество мобильных разработчиков iOS и Android. Делимся опытом разработки, решаем сложные задачи вместе.",
                        "image_url1": "https://example.com/mobile_club1.jpg",
                        "image_url2": "https://example.com/mobile_club2.jpg",
                        "tags": "ios, android, react native, flutter, мобильная разработка",
                        "target_audience": "Мобильные разработчики, Студенты",
                        "members_count": 37
                    }
                ]

                for club_data in clubs_list:
                    # Проверяем, существует ли уже такой клуб
                    existing_query = select(ClubOrm).where(ClubOrm.title == club_data["title"])
                    result = await session.execute(existing_query)
                    if not result.scalars().first():
                        club = ClubOrm(**club_data)
                        session.add(club)

                await session.commit()
                print("Тестовые клубы успешно созданы")
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError(f"Ошибка при инициализации тестовых клубов: {str(e)}") from e