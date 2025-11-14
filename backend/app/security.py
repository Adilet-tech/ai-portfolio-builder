import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

# Конфигурация JWT
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 часа

# Пути к RSA-ключам
PRIVATE_KEY_PATH = "/app/private_key.pem"
PUBLIC_KEY_PATH = "/app/public_key.pem"

try:
    with open(PRIVATE_KEY_PATH, "r") as f:
        PRIVATE_KEY = f.read()
    with open(PUBLIC_KEY_PATH, "r") as f:
        PUBLIC_KEY = f.read()
except FileNotFoundError as e:
    print(f"Ошибка: файл ключа не найден ({e.filename})")
    print(
        "Убедитесь, что 'private_key.pem' и 'public_key.pem' подключены в docker-compose.yml"
    )
    raise EnvironmentError("RSA ключи не найдены")

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Сравнивает обычный и хешированный пароль."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Возвращает хеш пароля."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT-токен, подписанный приватным ключом."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Проверяет JWT-токен и возвращает payload, если он валиден."""
    try:
        return jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
