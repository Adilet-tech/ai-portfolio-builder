from sqlmodel import SQLModel
from typing import Optional

# Базовая схема для User
class UserBase(SQLModel):
    email: str

# Схема для создания User (Регистрация)
class UserCreate(UserBase):
    password: str

# Схема для возврата User (Публичные данные)
class UserPublic(UserBase):
    id: int

# Схема для токена (Ответ при логине)
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Схема для данных ВНУТРИ токена
class TokenData(SQLModel):
    email: Optional[str] = None