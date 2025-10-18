from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.content import SNews, SCase, SVacancy, SParticipationResponse, SApplicationResponse, SLikeResponse
from repositories.content import ContentRepository
from models.users import UserOrm
from utils.security import get_current_user




router = APIRouter(
    prefix="",
    tags=['Контент']
)


# News endpoints
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


@router.post("/news/{news_id}/like", response_model=SLikeResponse)
async def like_news(news_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        likes_count = await ContentRepository.like_news(news_id, current_user.id)
        return SLikeResponse(success=True, likes_count=likes_count)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


# Cases endpoints
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


@router.post("/cases/{case_id}/participate", response_model=SParticipationResponse)
async def participate_in_case(case_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        participants_count = await ContentRepository.participate_in_case(case_id, current_user.id)
        return SParticipationResponse(success=True, participants_count=participants_count)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


# Vacancies endpoints
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


@router.post("/vacancies/{vacancy_id}/apply", response_model=SApplicationResponse)
async def apply_for_vacancy(vacancy_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        application_id = await ContentRepository.apply_for_vacancy(vacancy_id, current_user.id)
        return SApplicationResponse(success=True, application_id=application_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")