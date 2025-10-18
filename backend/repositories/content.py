from datetime import datetime, timezone
from database import new_session
from models.content import NewsOrm, NewsLikeOrm, CaseOrm, CaseParticipantOrm, VacancyOrm, VacancyApplicationOrm
from schemas.content import SNewsCreate, SCaseCreate, SVacancyCreate
from sqlalchemy import select, delete, insert, update, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError




class ContentRepository:
    # News methods
    @classmethod
    async def get_all_news(cls, limit: int = 20, offset: int = 0) -> list[NewsOrm]:
        async with new_session() as session:
            try:
                query = select(NewsOrm).order_by(NewsOrm.created_at.desc()).limit(limit).offset(offset)
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении новостей") from e

    @classmethod
    async def create_news(cls, news_data: SNewsCreate) -> NewsOrm:
        async with new_session() as session:
            try:
                news = NewsOrm(**news_data.model_dump())
                session.add(news)
                await session.commit()
                await session.refresh(news)
                return news
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при создании новости") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при создании новости") from e

    @classmethod
    async def like_news(cls, news_id: int, user_id: int) -> int:
        async with new_session() as session:
            try:
                # Проверяем, есть ли уже лайк
                like_query = select(NewsLikeOrm).where(
                    NewsLikeOrm.news_id == news_id,
                    NewsLikeOrm.user_id == user_id
                )
                result = await session.execute(like_query)
                existing_like = result.scalars().first()

                if existing_like:
                    # Удаляем лайк
                    delete_query = delete(NewsLikeOrm).where(
                        NewsLikeOrm.news_id == news_id,
                        NewsLikeOrm.user_id == user_id
                    )
                    await session.execute(delete_query)
                    # Уменьшаем счетчик
                    update_query = update(NewsOrm).where(NewsOrm.id == news_id).values(
                        likes_count=NewsOrm.likes_count - 1
                    )
                else:
                    # Добавляем лайк
                    like = NewsLikeOrm(news_id=news_id, user_id=user_id)
                    session.add(like)
                    # Увеличиваем счетчик
                    update_query = update(NewsOrm).where(NewsOrm.id == news_id).values(
                        likes_count=NewsOrm.likes_count + 1
                    )

                await session.execute(update_query)
                await session.commit()

                # Получаем обновленное количество лайков
                news_query = select(NewsOrm.likes_count).where(NewsOrm.id == news_id)
                result = await session.execute(news_query)
                return result.scalar()
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при лайке новости") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при лайке новости") from e

    # Case methods
    @classmethod
    async def get_all_cases(cls, limit: int = 20, offset: int = 0) -> list[CaseOrm]:
        async with new_session() as session:
            try:
                query = select(CaseOrm).order_by(CaseOrm.created_at.desc()).limit(limit).offset(offset)
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении кейсов") from e

    @classmethod
    async def create_case(cls, case_data: SCaseCreate) -> CaseOrm:
        async with new_session() as session:
            try:
                case = CaseOrm(**case_data.model_dump())
                session.add(case)
                await session.commit()
                await session.refresh(case)
                return case
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при создании кейса") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при создании кейса") from e

    @classmethod
    async def participate_in_case(cls, case_id: int, user_id: int) -> int:
        async with new_session() as session:
            try:
                # Проверяем, участвует ли уже пользователь
                participant_query = select(CaseParticipantOrm).where(
                    CaseParticipantOrm.case_id == case_id,
                    CaseParticipantOrm.user_id == user_id
                )
                result = await session.execute(participant_query)
                existing_participant = result.scalars().first()

                if existing_participant:
                    # Удаляем участие
                    delete_query = delete(CaseParticipantOrm).where(
                        CaseParticipantOrm.case_id == case_id,
                        CaseParticipantOrm.user_id == user_id
                    )
                    await session.execute(delete_query)
                    # Уменьшаем счетчик
                    update_query = update(CaseOrm).where(CaseOrm.id == case_id).values(
                        participants_count=CaseOrm.participants_count - 1
                    )
                else:
                    # Добавляем участие
                    participant = CaseParticipantOrm(case_id=case_id, user_id=user_id)
                    session.add(participant)
                    # Увеличиваем счетчик
                    update_query = update(CaseOrm).where(CaseOrm.id == case_id).values(
                        participants_count=CaseOrm.participants_count + 1
                    )

                await session.execute(update_query)
                await session.commit()

                # Получаем обновленное количество участников
                case_query = select(CaseOrm.participants_count).where(CaseOrm.id == case_id)
                result = await session.execute(case_query)
                return result.scalar()
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при участии в кейсе") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при участии в кейсе") from e

    # Vacancy methods
    @classmethod
    async def get_all_vacancies(cls, limit: int = 20, offset: int = 0) -> list[VacancyOrm]:
        async with new_session() as session:
            try:
                query = select(VacancyOrm).order_by(VacancyOrm.created_at.desc()).limit(limit).offset(offset)
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                raise ValueError("Ошибка базы данных при получении вакансий") from e

    @classmethod
    async def create_vacancy(cls, vacancy_data: SVacancyCreate) -> VacancyOrm:
        async with new_session() as session:
            try:
                vacancy = VacancyOrm(**vacancy_data.model_dump())
                session.add(vacancy)
                await session.commit()
                await session.refresh(vacancy)
                return vacancy
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при создании вакансии") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при создании вакансии") from e

    @classmethod
    async def apply_for_vacancy(cls, vacancy_id: int, user_id: int) -> int:
        async with new_session() as session:
            try:
                # Проверяем, есть ли уже заявка
                application_query = select(VacancyApplicationOrm).where(
                    VacancyApplicationOrm.vacancy_id == vacancy_id,
                    VacancyApplicationOrm.user_id == user_id
                )
                result = await session.execute(application_query)
                existing_application = result.scalars().first()

                if existing_application:
                    raise ValueError("Вы уже подали заявку на эту вакансию")

                # Создаем новую заявку
                application = VacancyApplicationOrm(vacancy_id=vacancy_id, user_id=user_id)
                session.add(application)
                await session.commit()
                await session.refresh(application)
                return application.id
            except IntegrityError as e:
                await session.rollback()
                raise ValueError("Ошибка целостности данных при подаче заявки") from e
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка базы данных при подаче заявки") from e

    @classmethod
    async def init_test_content(cls):
        """Инициализация тестового контента"""
        async with new_session() as session:
            try:
                # Тестовые новости
                news_list = [
                    {
                        "title": "Хакатон по разработке мобильных приложений",
                        "author": "Компания Яндекс",
                        "main_text": "Приглашаем всех желающих принять участие в ежегодном хакатоне по мобильной разработке...",
                        "image_url1": "http://example.com/hackathon1.jpg",
                        "image_url2": "http://example.com/hackathon2.jpg",
                        "start_date": "2024-02-01T10:00:00Z",
                        "end_date": "2024-02-02T18:00:00Z",
                        "address": "Москва, ул. Льва Толстого, 16"
                    },
                    {
                        "title": "Конференция по искусственному интеллекту",
                        "author": "Компания VK",
                        "main_text": "Крупнейшая конференция по AI и машинному обучению в этом году...",
                        "image_url1": "http://example.com/ai1.jpg",
                        "image_url2": None,
                        "start_date": "2024-03-15T09:00:00Z",
                        "end_date": "2024-03-16T17:00:00Z",
                        "address": "Санкт-Петербург, Невский проспект, 1"
                    }
                ]

                for news_data in news_list:
                    news = NewsOrm(**news_data)
                    session.add(news)

                # Тестовые кейсы
                cases_list = [
                    {
                        "title": "Разработка системы рекомендаций",
                        "author": "Компания Ozon",
                        "main_text": "Создайте систему рекомендаций товаров для интернет-магазина...",
                        "image_url1": "http://example.com/case1.jpg",
                        "image_url2": "http://example.com/case2.jpg",
                        "start_date": "2024-02-10T00:00:00Z",
                        "end_date": "2024-03-10T23:59:59Z",
                        "address": "Онлайн",
                        "tags": "python, machine learning, рекомендательные системы"
                    },
                    {
                        "title": "Оптимизация пользовательского интерфейса",
                        "author": "Компания Сбер",
                        "main_text": "Проанализируйте и улучшите пользовательский опыт мобильного приложения...",
                        "image_url1": "http://example.com/ui1.jpg",
                        "image_url2": None,
                        "start_date": "2024-02-15T00:00:00Z",
                        "end_date": "2024-03-20T23:59:59Z",
                        "address": "Москва, Кутузовский проспект, 32",
                        "tags": "ui/ux, дизайн, исследование"
                    }
                ]

                for case_data in cases_list:
                    case = CaseOrm(**case_data)
                    session.add(case)

                # Тестовые вакансии
                vacancies_list = [
                    {
                        "title": "Стажер-разработчик Python",
                        "author": "Компания Тинькофф",
                        "main_text": "Ищем начинающего разработчика для работы над внутренними проектами...",
                        "image_url1": "http://example.com/vacancy1.jpg",
                        "image_url2": "http://example.com/vacancy2.jpg",
                        "tags": "python, django, postgresql, docker"
                    },
                    {
                        "title": "Frontend разработчик React",
                        "author": "Компания Lamoda",
                        "main_text": "Требуется опытный фронтенд разработчик для работы над платформой электронной коммерции...",
                        "image_url1": "http://example.com/react1.jpg",
                        "image_url2": None,
                        "tags": "javascript, react, typescript, css"
                    }
                ]

                for vacancy_data in vacancies_list:
                    vacancy = VacancyOrm(**vacancy_data)
                    session.add(vacancy)

                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError("Ошибка при инициализации тестового контента") from e
    
    @classmethod
    async def init_test_content(cls):
        """Инициализация тестового контента"""
        async with new_session() as session:
            try:
                # Тестовые новости
                news_list = [
                    {
                        "title": "Хакатон по разработке мобильных приложений",
                        "author": "Компания Яндекс",
                        "main_text": "Приглашаем всех желающих принять участие в ежегодном хакатоне по мобильной разработке. Участникам предстоит создать инновационные приложения за 48 часов. Лучшие проекты получат гранты на развитие.",
                        "image_url1": "https://example.com/hackathon1.jpg",
                        "image_url2": "https://example.com/hackathon2.jpg",
                        "start_date": datetime(2024, 2, 1, 10, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2024, 2, 2, 18, 0, 0, tzinfo=timezone.utc),
                        "address": "Москва, ул. Льва Толстого, 16",
                        "likes_count": 25
                    },
                    {
                        "title": "Конференция по искусственному интеллекту",
                        "author": "Компания VK",
                        "main_text": "Крупнейшая конференция по AI и машинному обучению в этом году. Выступят ведущие эксперты отрасли, будут представлены новые технологии и исследования в области искусственного интеллекта.",
                        "image_url1": "https://example.com/ai1.jpg",
                        "image_url2": None,
                        "start_date": datetime(2024, 3, 15, 9, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2024, 3, 16, 17, 0, 0, tzinfo=timezone.utc),
                        "address": "Санкт-Петербург, Невский проспект, 1",
                        "likes_count": 42
                    },
                    {
                        "title": "Мастер-класс по веб-разработке",
                        "author": "HTML Academy",
                        "main_text": "Практический мастер-класс для начинающих веб-разработчиков. Изучим современные подходы к созданию веб-приложений, работу с API и основы DevOps.",
                        "image_url1": "https://example.com/web1.jpg",
                        "image_url2": "https://example.com/web2.jpg",
                        "start_date": datetime(2024, 2, 20, 14, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2024, 2, 20, 18, 0, 0, tzinfo=timezone.utc),
                        "address": "Онлайн",
                        "likes_count": 18
                    }
                ]

                for news_data in news_list:
                    # Проверяем, существует ли уже такая новость
                    existing_query = select(NewsOrm).where(NewsOrm.title == news_data["title"])
                    result = await session.execute(existing_query)
                    if not result.scalars().first():
                        news = NewsOrm(**news_data)
                        session.add(news)

                # Тестовые кейсы
                cases_list = [
                    {
                        "title": "Разработка системы рекомендаций",
                        "author": "Компания Ozon",
                        "main_text": "Создайте систему рекомендаций товаров для интернет-магазина. Используйте методы машинного обучения для анализа поведения пользователей и повышения конверсии.",
                        "image_url1": "https://example.com/case1.jpg",
                        "image_url2": "https://example.com/case2.jpg",
                        "start_date": datetime(2024, 2, 10, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2024, 3, 10, 23, 59, 59, tzinfo=timezone.utc),
                        "address": "Онлайн",
                        "tags": "python, machine learning, рекомендательные системы",
                        "participants_count": 15
                    },
                    {
                        "title": "Оптимизация пользовательского интерфейса",
                        "author": "Компания Сбер",
                        "main_text": "Проанализируйте и улучшите пользовательский опыт мобильного приложения. Проведите UX-исследование, предложите решения по улучшению навигации и визуального дизайна.",
                        "image_url1": "https://example.com/ui1.jpg",
                        "image_url2": None,
                        "start_date": datetime(2024, 2, 15, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2024, 3, 20, 23, 59, 59, tzinfo=timezone.utc),
                        "address": "Москва, Кутузовский проспект, 32",
                        "tags": "ui/ux, дизайн, исследование",
                        "participants_count": 8
                    },
                    {
                        "title": "Создание чат-бота для поддержки",
                        "author": "Тинькофф Банк",
                        "main_text": "Разработайте интеллектуального чат-бота для автоматизации ответов на частые вопросы клиентов. Интегрируйте с существующей системой поддержки.",
                        "image_url1": "https://example.com/chatbot1.jpg",
                        "image_url2": "https://example.com/chatbot2.jpg",
                        "start_date": datetime(2024, 3, 1, 0, 0, 0, tzinfo=timezone.utc),
                        "end_date": datetime(2024, 4, 1, 23, 59, 59, tzinfo=timezone.utc),
                        "address": "Онлайн",
                        "tags": "python, nlp, telegram api, django",
                        "participants_count": 22
                    }
                ]

                for case_data in cases_list:
                    existing_query = select(CaseOrm).where(CaseOrm.title == case_data["title"])
                    result = await session.execute(existing_query)
                    if not result.scalars().first():
                        case = CaseOrm(**case_data)
                        session.add(case)

                # Тестовые вакансии
                vacancies_list = [
                    {
                        "title": "Стажер-разработчик Python",
                        "author": "Компания Тинькофф",
                        "main_text": "Ищем начинающего разработчика для работы над внутренними проектами. Требуется знание Python, основы SQL и желание развиваться в backend-разработке.",
                        "image_url1": "https://example.com/vacancy1.jpg",
                        "image_url2": "https://example.com/vacancy2.jpg",
                        "tags": "python, django, postgresql, docker"
                    },
                    {
                        "title": "Frontend разработчик React",
                        "author": "Компания Lamoda",
                        "main_text": "Требуется опытный фронтенд разработчик для работы над платформой электронной коммерции. Знание React, TypeScript и современных инструментов разработки.",
                        "image_url1": "https://example.com/react1.jpg",
                        "image_url2": None,
                        "tags": "javascript, react, typescript, css"
                    },
                    {
                        "title": "Data Analyst",
                        "author": "СберМаркет",
                        "main_text": "Аналитик данных для работы с большими объемами информации. Построение отчетов, анализ метрик, выявление закономерностей и трендов.",
                        "image_url1": "https://example.com/analyst1.jpg",
                        "image_url2": "https://example.com/analyst2.jpg",
                        "tags": "sql, python, tableau, статистика"
                    },
                    {
                        "title": "DevOps инженер",
                        "author": "Рамблер",
                        "main_text": "Настройка и поддержка CI/CD процессов, работа с облачной инфраструктурой, автоматизация развертывания приложений.",
                        "image_url1": "https://example.com/devops1.jpg",
                        "image_url2": None,
                        "tags": "docker, kubernetes, aws, ci/cd"
                    }
                ]

                for vacancy_data in vacancies_list:
                    existing_query = select(VacancyOrm).where(VacancyOrm.title == vacancy_data["title"])
                    result = await session.execute(existing_query)
                    if not result.scalars().first():
                        vacancy = VacancyOrm(**vacancy_data)
                        session.add(vacancy)

                await session.commit()
                print("Тестовый контент успешно создан")
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError(f"Ошибка при инициализации тестового контента: {str(e)}") from e