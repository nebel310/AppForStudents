import os
from dotenv import load_dotenv
from database import new_session
from models.users import UserOrm, RefreshTokenOrm, BlacklistedTokenOrm, InterestOrm, SkillOrm, UserInterestOrm, UserSkillOrm
from schemas.users import SUserRegister, SUserRoleUpdate, SUserInterestsUpdate, SUserSkillsUpdate
from sqlalchemy import select, delete, insert
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta




load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    @classmethod
    async def register_user(cls, user_data: SUserRegister) -> int:
        async with new_session() as session:
            try:
                query = select(UserOrm).where(UserOrm.email == user_data.email)
                result = await session.execute(query)
                if result.scalars().first():
                    raise ValueError("Пользователь с таким email уже существует")
                  
                hashed_password = pwd_context.hash(user_data.password)
                
                user = UserOrm(
                    username=user_data.username,
                    email=user_data.email,
                    hashed_password=hashed_password,
                    role='student'
                )
                session.add(user)
                await session.flush()
                await session.commit()
                return user.id
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при регистрации") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при регистрации") from e
    
    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> UserOrm | None:
        async with new_session() as session:
            try:
                query = select(UserOrm).where(UserOrm.email == email)
                result = await session.execute(query)
                user = result.scalars().first()
                
                if not user or not pwd_context.verify(password, user.hashed_password):
                    return None
                
                return user
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при аутентификации") from e
    
    @classmethod
    async def get_user_by_email(cls, email: str) -> UserOrm | None:
        async with new_session() as session:
            try:
                query = select(UserOrm).where(UserOrm.email == email)
                result = await session.execute(query)
                return result.scalars().first()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при поиске пользователя") from e
    
    @classmethod
    async def get_user_by_id(cls, user_id: int) -> UserOrm | None:
        async with new_session() as session:
            try:
                query = select(UserOrm).where(UserOrm.id == user_id)
                result = await session.execute(query)
                return result.scalars().first()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при поиске пользователя") from e
    
    @classmethod
    async def get_user_by_refresh_token(cls, refresh_token: str) -> UserOrm | None:
        async with new_session() as session:
            try:
                query = select(RefreshTokenOrm).where(RefreshTokenOrm.token == refresh_token)
                result = await session.execute(query)
                refresh_token_orm = result.scalars().first()
                
                if not refresh_token_orm or refresh_token_orm.expires_at < datetime.now(timezone.utc):
                    return None
                
                return await cls.get_user_by_id(refresh_token_orm.user_id)
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при проверке refresh токена") from e
    
    @classmethod
    async def create_refresh_token(cls, user_id: int) -> str:
        async with new_session() as session:
            try:
                delete_query = delete(RefreshTokenOrm).where(RefreshTokenOrm.user_id == user_id)
                await session.execute(delete_query)
                
                refresh_token = jwt.encode({"sub": str(user_id)}, SECRET_KEY, algorithm=ALGORITHM)
                expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
                
                refresh_token_orm = RefreshTokenOrm(
                    user_id=user_id,
                    token=refresh_token,
                    expires_at=expires_at
                )
                session.add(refresh_token_orm)
                await session.commit()
                return refresh_token
            except (SQLAlchemyError, JWTError) as e:
                await session.rollback()
                raise ValueError("Ошибка при создании refresh токена") from e

    @classmethod
    async def revoke_refresh_token(cls, user_id: int):
        async with new_session() as session:
            try:
                query = delete(RefreshTokenOrm).where(RefreshTokenOrm.user_id == user_id)
                await session.execute(query)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка при отзыве refresh токена") from e

    @classmethod
    async def add_to_blacklist(cls, token: str):
        async with new_session() as session:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            except JWTError:
                return

            try:
                blacklisted_token = BlacklistedTokenOrm(
                    token=token,
                    expires_at=expires_at,
                    created_at=datetime.now(timezone.utc)
                )
                session.add(blacklisted_token)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка при добавлении токена в черный список") from e

    @classmethod
    async def update_user_role(cls, user_id: int, role_data: SUserRoleUpdate) -> UserOrm:
        async with new_session() as session:
            try:
                query = select(UserOrm).where(UserOrm.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                
                if not user:
                    raise ValueError("Пользователь не найден")
                
                user.role = role_data.role
                await session.commit()
                return user
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при обновлении роли") from e

    @classmethod
    async def get_all_interests(cls) -> list[InterestOrm]:
        async with new_session() as session:
            try:
                query = select(InterestOrm)
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении интересов") from e

    @classmethod
    async def get_all_skills(cls) -> list[SkillOrm]:
        async with new_session() as session:
            try:
                query = select(SkillOrm)
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении навыков") from e

    @classmethod
    async def update_user_interests(cls, user_id: int, interests_data: SUserInterestsUpdate) -> list[InterestOrm]:
        async with new_session() as session:
            try:
                # Проверяем существование интересов
                if interests_data.interest_ids:
                    interests_query = select(InterestOrm).where(InterestOrm.id.in_(interests_data.interest_ids))
                    result = await session.execute(interests_query)
                    existing_interests = result.scalars().all()
                    
                    if len(existing_interests) != len(interests_data.interest_ids):
                        raise ValueError("Некоторые интересы не найдены в базе данных")
                
                # Удаляем старые интересы
                delete_query = delete(UserInterestOrm).where(UserInterestOrm.user_id == user_id)
                await session.execute(delete_query)
                
                # Добавляем новые интересы
                if interests_data.interest_ids:
                    insert_query = insert(UserInterestOrm).values(
                        [{"user_id": user_id, "interest_id": interest_id} for interest_id in interests_data.interest_ids]
                    )
                    await session.execute(insert_query)
                
                await session.commit()
                
                # Возвращаем обновленные интересы
                if interests_data.interest_ids:
                    interests_query = select(InterestOrm).where(InterestOrm.id.in_(interests_data.interest_ids))
                    result = await session.execute(interests_query)
                    return result.scalars().all()
                return []
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при обновлении интересов") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при обновлении интересов") from e

    @classmethod
    async def update_user_skills(cls, user_id: int, skills_data: SUserSkillsUpdate) -> list[SkillOrm]:
        async with new_session() as session:
            try:
                # Проверяем существование навыков
                if skills_data.skill_ids:
                    skills_query = select(SkillOrm).where(SkillOrm.id.in_(skills_data.skill_ids))
                    result = await session.execute(skills_query)
                    existing_skills = result.scalars().all()
                    
                    if len(existing_skills) != len(skills_data.skill_ids):
                        raise ValueError("Некоторые навыки не найдены в базе данных")
                
                # Удаляем старые навыки
                delete_query = delete(UserSkillOrm).where(UserSkillOrm.user_id == user_id)
                await session.execute(delete_query)
                
                # Добавляем новые навыки
                if skills_data.skill_ids:
                    insert_query = insert(UserSkillOrm).values(
                        [{"user_id": user_id, "skill_id": skill_id} for skill_id in skills_data.skill_ids]
                    )
                    await session.execute(insert_query)
                
                await session.commit()
                
                # Возвращаем обновленные навыки
                if skills_data.skill_ids:
                    skills_query = select(SkillOrm).where(SkillOrm.id.in_(skills_data.skill_ids))
                    result = await session.execute(skills_query)
                    return result.scalars().all()
                return []
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при обновлении навыков") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при обновлении навыков") from e

    @classmethod
    async def get_user_with_interests_skills(cls, user_id: int) -> UserOrm:
        async with new_session() as session:
            try:
                query = select(UserOrm).where(UserOrm.id == user_id)
                result = await session.execute(query)
                return result.scalars().first()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении пользователя") from e

    @classmethod
    async def init_interests_and_skills(cls):
        """Инициализация базовых интересов и навыков"""
        async with new_session() as session:
            try:
                # Базовые интересы
                interests = [
                    "Программирование", "Дизайн", "Маркетинг", "Аналитика", 
                    "Управление", "Искусственный интеллект", "Data Science",
                    "Веб-разработка", "Мобильная разработка", "Кибербезопасность",
                    "DevOps", "UI/UX дизайн", "Продукт-менеджмент", "Бизнес-анализ",
                    "Машинное обучение", "Блокчейн", "Cloud computing"
                ]
                
                for interest_name in interests:
                    # Проверяем, существует ли уже такой интерес
                    existing_query = select(InterestOrm).where(InterestOrm.name == interest_name)
                    result = await session.execute(existing_query)
                    if not result.scalars().first():
                        interest = InterestOrm(name=interest_name)
                        session.add(interest)
                
                # Базовые навыки
                skills = [
                    "Python", "JavaScript", "Java", "C++", "SQL", "HTML/CSS",
                    "React", "Vue.js", "Django", "FastAPI", "Docker", "Git",
                    "Photoshop", "Figma", "Excel", "PowerPoint", "Английский язык",
                    "TypeScript", "Node.js", "PostgreSQL", "MongoDB", "Redis",
                    "Kubernetes", "AWS", "Azure", "Google Cloud", "TensorFlow",
                    "PyTorch", "Pandas", "NumPy", "Scikit-learn"
                ]
                
                for skill_name in skills:
                    existing_query = select(SkillOrm).where(SkillOrm.name == skill_name)
                    result = await session.execute(existing_query)
                    if not result.scalars().first():
                        skill = SkillOrm(name=skill_name)
                        session.add(skill)
                
                await session.commit()
                print("Базовые интересы и навыки успешно созданы")
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError(f"Ошибка при инициализации интересов и навыков: {str(e)}") from e