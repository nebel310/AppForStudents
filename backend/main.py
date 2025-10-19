import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router.users import router as users_router
from router.content import router as content_router
from router.club import router as club_router
from repositories.users import UserRepository
from repositories.content import ContentRepository
from repositories.club import ClubRepository
from schemas.users import SUserRegister




@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База готова к работе')
    
    # Инициализируем базовые интересы и навыки
    try:
        await UserRepository.init_interests_and_skills()
        print('Базовые интересы и навыки добавлены')
    except Exception as e:
        print(f'Ошибка при инициализации интересов и навыков: {e}')
    
    # Инициализируем тестовый контент
    try:
        await ContentRepository.init_test_content()
        print('Тестовый контент добавлен')
    except Exception as e:
        print(f'Ошибка при инициализации тестового контента: {e}')
    
    # Инициализируем тестовые клубы
    try:
        await ClubRepository.init_test_clubs()
        print('Тестовые клубы добавлены')
    except Exception as e:
        print(f'Ошибка при инициализации тестовых клубов: {e}')
    
    yield
    print('Выключение')


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="CareerHub API",
        version="1.0.0",
        description="API для платформы карьерного развития студентов и рекрутеров",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    secured_paths = {
        # Пользователи
        "/auth/me": {"method": "get", "security": [{"Bearer": []}]},
        "/auth/logout": {"method": "post", "security": [{"Bearer": []}]},
        "/auth/role": {"method": "patch", "security": [{"Bearer": []}]},
        "/auth/interests": {"method": "post", "security": [{"Bearer": []}]},
        "/auth/skills": {"method": "post", "security": [{"Bearer": []}]},
        "/auth/update_me": {"method": "patch", "security": [{"Bearer": []}]},
        "/auth/update_profile": {"method": "patch", "security": [{"Bearer": []}]},
        # Главная - пользовательские взаимодействия
        "/news/{news_id}/like": {"method": "post", "security": [{"Bearer": []}]},
        "/cases/{case_id}/participate": {"method": "post", "security": [{"Bearer": []}]},
        "/vacancies/{vacancy_id}/apply": {"method": "post", "security": [{"Bearer": []}]},
        # Главная - рекрутерские эндпоинты
        "/news": {"method": "post", "security": [{"Bearer": []}]},
        "/news/{news_id}": {"method": "patch", "security": [{"Bearer": []}]},
        "/cases": {"method": "post", "security": [{"Bearer": []}]},
        "/cases/{case_id}": {"method": "patch", "security": [{"Bearer": []}]},
        "/vacancies": {"method": "post", "security": [{"Bearer": []}]},
        "/vacancies/{vacancy_id}": {"method": "patch", "security": [{"Bearer": []}]},
        # Клубы
        "/clubs": {"method": "post", "security": [{"Bearer": []}]},
        "/clubs/{club_id}/join": {"method": "post", "security": [{"Bearer": []}]},
        "/clubs/{club_id}/leave": {"method": "post", "security": [{"Bearer": []}]},
    }
    
    for path, config in secured_paths.items():
        if path in openapi_schema["paths"]:
            openapi_schema["paths"][path][config["method"]]["security"] = config["security"]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(lifespan=lifespan)
app.openapi = custom_openapi
app.include_router(users_router)
app.include_router(content_router)
app.include_router(club_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:3000", "http://localhost:8080", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Раскоментить, когда будешь писать докер.
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        port=3001,
        host="0.0.0.0"
    )