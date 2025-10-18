from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.club import SClub, SClubDetail, SClubJoinResponse, SClubLeaveResponse, SClubCreate
from repositories.club import ClubRepository
from models.users import UserOrm
from utils.security import get_current_user




router = APIRouter(
    prefix="/clubs",
    tags=['Клубы']
)


@router.get("", response_model=list[SClub])
async def get_all_clubs(
    limit: int = Query(20, ge=1, le=100, description="Лимит клубов"),
    offset: int = Query(0, ge=0, description="Смещение")
):
    try:
        clubs = await ClubRepository.get_all_clubs(limit=limit, offset=offset)
        return [SClub.model_validate(club) for club in clubs]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/{club_id}", response_model=SClubDetail)
async def get_club_detail(club_id: int):
    try:
        club_data = await ClubRepository.get_club_with_members(club_id)
        
        # Форматируем участников
        members = []
        for member in club_data["members"]:
            members.append({
                "id": member.id,
                "username": member.username,
                "avatar_url": member.avatar_url,
                "rating": member.rating
            })
        
        return SClubDetail(
            **SClub.model_validate(club_data["club"]).model_dump(),
            members=members
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("", response_model=SClub)
async def create_club(club_data: SClubCreate, current_user: UserOrm = Depends(get_current_user)):
    try:
        club = await ClubRepository.create_club(club_data, current_user.id)
        return SClub.model_validate(club)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/{club_id}/join", response_model=SClubJoinResponse)
async def join_club(club_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        members_count = await ClubRepository.join_club(club_id, current_user.id)
        return SClubJoinResponse(success=True, members_count=members_count)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/{club_id}/leave", response_model=SClubLeaveResponse)
async def leave_club(club_id: int, current_user: UserOrm = Depends(get_current_user)):
    try:
        members_count = await ClubRepository.leave_club(club_id, current_user.id)
        return SClubLeaveResponse(success=True, members_count=members_count)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")