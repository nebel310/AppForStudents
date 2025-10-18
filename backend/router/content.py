from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.content import SNews, SCase, SVacancy, SParticipationResponse, SApplicationResponse, SLikeResponse, SNewsCreate, SCaseCreate, SVacancyCreate, SNewsUpdate, SCaseUpdate, SVacancyUpdate, SContentCreateResponse
from repositories.content import ContentRepository
from models.users import UserOrm
from utils.security import get_current_user, get_current_recruiter




router = APIRouter(
    prefix="",
    tags=['Главная']
)


# Public endpoints - доступны всем
@router.get("/news", response_model=list[SNews])
async def get_all_news(
    limit: int = Query(20, ge=1, le=100, description="Лимит новостей"),
    offset: int = Query(0, ge=0, description="Смещение")
):
    try:
        news = await ContentRepository.get_all_news(limit=limit, offset=offset)
        return [SNews.model_validate(item) for item in news]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/cases", response_model=list[SCase])
async def get_all_cases(
    limit: int = Query(20, ge=1, le=100, description="Лимит кейсов"),
    offset: int = Query(0, ge=0, description="Смещение")
):
    try:
        cases = await ContentRepository.get_all_cases(limit=limit, offset=offset)
        return [SCase.model_validate(item) for item in cases]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/vacancies", response_model=list[SVacancy])
async def get_all_vacancies(
    limit: int = Query(20, ge=1, le=100, description="Лимит вакансий"),
    offset: int = Query(0, ge=0, description="Смещение")
):
    try:
        vacancies = await ContentRepository.get_all_vacancies(limit=limit, offset=offset)
        return [SVacancy.model_validate(item) for item in vacancies]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


# User interaction endpoints - требуют авторизации
@router.post("/news/{news_id}/like", response_model=SLikeResponse)
async def like_news(news_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        likes_count = await ContentRepository.like_news(news_id, current_user.id)
        return SLikeResponse(success=True, likes_count=likes_count)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/cases/{case_id}/participate", response_model=SParticipationResponse)
async def participate_in_case(case_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        participants_count = await ContentRepository.participate_in_case(case_id, current_user.id)
        return SParticipationResponse(success=True, participants_count=participants_count)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/vacancies/{vacancy_id}/apply", response_model=SApplicationResponse)
async def apply_for_vacancy(vacancy_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        application_id = await ContentRepository.apply_for_vacancy(vacancy_id, current_user.id)
        return SApplicationResponse(success=True, application_id=application_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


# Recruiter only endpoints - требуют роль рекрутера
@router.post("/news", response_model=SContentCreateResponse)
async def create_news(news_data: SNewsCreate, current_user: UserOrm = Depends(get_current_recruiter)):
    try:
        news = await ContentRepository.create_news(news_data)
        return SContentCreateResponse(
            id=news.id,
            title=news.title,
            success=True
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.patch("/news/{news_id}", response_model=SNews)
async def update_news(news_id: int, update_data: SNewsUpdate, current_user: UserOrm = Depends(get_current_recruiter)):
    try:
        news = await ContentRepository.update_news(news_id, update_data)
        return SNews.model_validate(news)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/cases", response_model=SContentCreateResponse)
async def create_case(case_data: SCaseCreate, current_user: UserOrm = Depends(get_current_recruiter)):
    try:
        case = await ContentRepository.create_case(case_data)
        return SContentCreateResponse(
            id=case.id,
            title=case.title,
            success=True
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.patch("/cases/{case_id}", response_model=SCase)
async def update_case(case_id: int, update_data: SCaseUpdate, current_user: UserOrm = Depends(get_current_recruiter)):
    try:
        case = await ContentRepository.update_case(case_id, update_data)
        return SCase.model_validate(case)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/vacancies", response_model=SContentCreateResponse)
async def create_vacancy(vacancy_data: SVacancyCreate, current_user: UserOrm = Depends(get_current_recruiter)):
    try:
        vacancy = await ContentRepository.create_vacancy(vacancy_data)
        return SContentCreateResponse(
            id=vacancy.id,
            title=vacancy.title,
            success=True
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.patch("/vacancies/{vacancy_id}", response_model=SVacancy)
async def update_vacancy(vacancy_id: int, update_data: SVacancyUpdate, current_user: UserOrm = Depends(get_current_recruiter)):
    try:
        vacancy = await ContentRepository.update_vacancy(vacancy_id, update_data)
        return SVacancy.model_validate(vacancy)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")