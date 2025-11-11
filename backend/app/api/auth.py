from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pydantic import EmailStr

from app import schemas, models, security
from app.db import get_session

# Создаем новый роутер.
# Мы будем подключать его к основному приложению в main.py
router = APIRouter()


@router.post("/register", response_model=schemas.UserPublic)
def register_user(
    # 1. Принимаем данные, которые совпадают со схемой UserCreate
    user_data: schemas.UserCreate,
    # 2. Получаем сессию базы данных
    session: Session = Depends(get_session),
):
    """
    Регистрирует нового пользователя.
    """
    
    # 3. Ищем, не занят ли этот email
    statement_email = select(models.User).where(models.User.email == user_data.email)
    existing_user_email = session.exec(statement_email).first()
    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # 4. Ищем, не занят ли этот username (из твоей новой модели)
    statement_username = select(models.User).where(models.User.username == user_data.username)
    existing_user_username = session.exec(statement_username).first()
    if existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # 5. Если все свободно, хешируем пароль
    hashed_password = security.get_password_hash(user_data.password)

    # 6. Создаем новый объект User (исправлено, с username)
    new_user = models.User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
        # (Все остальные поля, такие как is_active,
        #  возьмут значения по умолчанию из models.py)
    )

    # 7. Добавляем в БД, сохраняем, обновляем
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # 8. Возвращаем публичные данные о юзере
    return new_user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    # 1. FastAPI по-умному принимает данные из form-data (username и password)
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    Аутентифицирует пользователя и возвращает JWT-токен.
    
    ВНИМАНИЕ: OAuth2PasswordRequestForm требует, чтобы поле email
    приходило под именем 'username' в form-data.
    """

    # 2. Ищем пользователя по email (OAuth2 называет это 'username')
    statement = select(models.User).where(models.User.email == form_data.username)
    user = session.exec(statement).first()

    # 3. Проверяем, что юзер найден И что пароль верный
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            # Это стандартный заголовок для 401
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Если все верно, создаем токен.
    # "sub" (subject) - это стандартное имя "claims" для ID/email пользователя
    access_token = security.create_access_token(data={"sub": user.email})

    # 5. Возвращаем токен по схеме Token
    return {"access_token": access_token, "token_type": "bearer"}