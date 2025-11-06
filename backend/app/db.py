import os
import time
from sqlalchemy.exc import OperationalError 
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
from . import models

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL, echo=True) 

def create_db_and_tables():
    print("Попытка подключиться к БД и создать таблицы...")

    retries = 5  
    delay = 5    

    while retries > 0:
        try:
            SQLModel.metadata.create_all(engine)

            print("✅ Таблицы успешно созданы (или уже существуют).")
            break 

        except OperationalError as e:
            retries -= 1
            print(f"⚠️ База данных не готова... {e}")
            if retries > 0:
                print(f"Повторная попытка через {delay} сек. (Осталось {retries} попыток)")
                time.sleep(delay)
            else:
                print("🚫 Не удалось подключиться к БД после всех попыток.")
                raise 

def get_session():
    """
    Функция-генератор, которая предоставляет сессию
    для одного API-запроса.
    """
    with Session(engine) as session:
        yield session