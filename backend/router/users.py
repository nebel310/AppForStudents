from fastapi import APIRouter, Depends, HTTPException
from schemas.users import SUserRegister, SUserLogin, SUser, SUserRoleUpdate, SInterest, SSkill, SUserInterestsUpdate, SUserSkillsUpdate, SUserWithInterestsSkills
from repositories.users import UserRepository
from models.users import UserOrm
from utils.security import get_current_user, oauth2_scheme, create_access_token




router = APIRouter(
    prefix="/auth",
    tags=['Пользователи']
)


@router.post("/register", response_model=dict)
async def register_user(user_data: SUserRegister):
    try:
        user_id = await UserRepository.register_user(user_data)
        return {"success": True, "user_id": user_id, "message": "Регистрация прошла успешно"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/login", response_model=dict)
async def login_user(login_data: SUserLogin):
    try:
        user = await UserRepository.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Неверный email или пароль")
        
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = await UserRepository.create_refresh_token(user.id)
        return {
            "success": True, 
            "message": "Вы вошли в аккаунт", 
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/refresh", response_model=dict)
async def refresh_token(refresh_token: str):
    try:
        user = await UserRepository.get_user_by_refresh_token(refresh_token)
        if not user:
            raise HTTPException(status_code=400, detail="Неверный refresh токен")
        
        new_access_token = create_access_token(data={"sub": user.email})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/logout", response_model=dict)
async def logout(token: str = Depends(oauth2_scheme), current_user: UserOrm = Depends(get_current_user)):
    try:
        await UserRepository.add_to_blacklist(token)
        await UserRepository.revoke_refresh_token(current_user.id)
        return {"success": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/me", response_model=SUser)
async def get_current_user_info(current_user: UserOrm = Depends(get_current_user)):
    try:
        return SUser.model_validate(current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.patch("/role", response_model=dict)
async def update_user_role(role_data: SUserRoleUpdate, current_user: UserOrm = Depends(get_current_user)):
    try:
        user = await UserRepository.update_user_role(current_user.id, role_data)
        return {"success": True, "role": user.role}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/interests", response_model=list[SInterest])
async def get_all_interests():
    try:
        interests = await UserRepository.get_all_interests()
        return [SInterest.model_validate(interest) for interest in interests]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/skills", response_model=list[SSkill])
async def get_all_skills():
    try:
        skills = await UserRepository.get_all_skills()
        return [SSkill.model_validate(skill) for skill in skills]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/interests", response_model=dict)
async def update_user_interests(interests_data: SUserInterestsUpdate, current_user: UserOrm = Depends(get_current_user)):
    try:
        interests = await UserRepository.update_user_interests(current_user.id, interests_data)
        return {
            "success": True, 
            "interests": [SInterest.model_validate(interest) for interest in interests]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/skills", response_model=dict)
async def update_user_skills(skills_data: SUserSkillsUpdate, current_user: UserOrm = Depends(get_current_user)):
    try:
        skills = await UserRepository.update_user_skills(current_user.id, skills_data)
        return {
            "success": True, 
            "skills": [SSkill.model_validate(skill) for skill in skills]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")