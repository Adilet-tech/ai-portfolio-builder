import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

# --- НАСТРОЙКИ JWT (RS256) ---
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 день

# --- ЧТЕНИЕ КЛЮЧЕЙ ИЗ ФАЙЛОВ ---
# Эти файлы монтируются в /app через docker-compose.yml
PRIVATE_KEY_PATH = "/app/private_key.pem"
PUBLIC_KEY_PATH = "/app/public_key.pem"

try:
    # Читаем ПРИВАТНЫЙ ключ
    with open(PRIVATE_KEY_PATH, "r") as f:
        PRIVATE_KEY = f.read()
    
    # Читаем ПУБЛИЧНЫЙ ключ
    with open(PUBLIC_KEY_PATH, "r") as f:
        PUBLIC_KEY = f.read()
except FileNotFoundError as e:
    print(f"ОШИБКА: Файл ключа не найден по пути {e.filename}")
    print("Убедись, что 'private_key.pem' и 'public_key.pem' смонтированы в docker-compose.yml")
    raise EnvironmentError("Файлы ключей не найдены.")
# --- КОНЕЦ БЛОКА ЧТЕНИЯ ---


# --- НАСТРОЙКИ HASH-ПАРОЛЕЙ ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли обычный пароль с хешированным.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Хеширует обычный пароль.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает новый JWT-токен, подписывая его ПРИВАТНЫМ ключом.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    # Мы используем PRIVATE_KEY для подписи
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Проверяет (валидирует) JWT-токен с помощью ПУБЛИЧНОГО ключа.
    Возвращает данные (payload) или None, если токен невалиден.
    """
    try:
        # Мы используем PUBLIC_KEY для проверки
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Если подпись неверна, истек срок или токен некорректен
        return None