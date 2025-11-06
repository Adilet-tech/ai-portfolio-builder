from fastapi import APIRouter, Depends
from app import schemas, models
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/me", response_model=schemas.UserPublic)
def read_users_me(
    current_user: models.User = Depends(get_current_user)
):
    """
    Защищенный эндпоинт. 
    Возвращает данные о ТЕКУЩЕМ залогиненном пользователе.
    """
    return current_user