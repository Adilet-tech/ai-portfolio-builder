"""
Обновленные модели базы данных с дополнительными полями
"""
from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import EmailStr


class User(SQLModel, table=True):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    
    # Дополнительные поля профиля
    full_name: Optional[str] = Field(default=None, max_length=100)
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(default=None, max_length=500)
    
    # Метаданные
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Настройки
    preferences: Dict = Field(default_factory=dict, sa_column=Column(JSON))


class Portfolio(SQLModel, table=True):
    """Модель портфолио"""
    __tablename__ = "portfolios"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    
    # Основной контент
    about_me: Optional[str] = Field(default=None, max_length=2000)
    headline: Optional[str] = Field(default=None, max_length=200)  # Короткий заголовок
    
    # Навыки (структурированные по категориям)
    skills_structured: Optional[Dict] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Навыки, сгруппированные по категориям"
    )
    
    # Проекты
    projects: Optional[List[Dict]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Список проектов с описаниями"
    )
    
    # Опыт работы
    work_experience: Optional[List[Dict]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="История работы"
    )
    
    # Образование
    education: Optional[List[Dict]] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    
    # Контактная информация
    contact_info: Optional[Dict] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Email, телефон, соцсети"
    )
    
    # Настройки внешнего вида
    template_id: Optional[str] = Field(default="default", max_length=50)
    theme: Optional[str] = Field(default="light", max_length=20)  # light, dark, custom
    color_scheme: Optional[Dict] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Пользовательская цветовая схема"
    )
    
    # Статус публикации
    is_published: bool = Field(default=False)
    slug: Optional[str] = Field(
        default=None,
        unique=True,
        index=True,
        max_length=100,
        description="URL-friendly имя для публичного доступа"
    )
    
    # Метаданные
    views_count: int = Field(default=0, description="Количество просмотров")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    
    # SEO
    meta_title: Optional[str] = Field(default=None, max_length=70)
    meta_description: Optional[str] = Field(default=None, max_length=160)


class Template(SQLModel, table=True):
    """Модель шаблона портфолио"""
    __tablename__ = "templates"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    display_name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    
    # Категория шаблона
    category: str = Field(
        default="general",
        max_length=50,
        description="Например: developer, designer, writer"
    )
    
    # Превью изображение
    preview_url: Optional[str] = None
    
    # HTML/CSS шаблон
    template_html: str = Field(description="HTML шаблон с плейсхолдерами")
    template_css: Optional[str] = Field(default=None)
    
    # Доступность
    is_premium: bool = Field(default=False)
    is_active: bool = Field(default=True)
    
    # Статистика
    usage_count: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GenerationHistory(SQLModel, table=True):
    """История генераций AI (для аналитики и отладки)"""
    __tablename__ = "generation_history"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    
    # Тип генерации
    generation_type: str = Field(
        max_length=50,
        description="about, project, skills, full"
    )
    
    # Входные данные (для отладки)
    input_data: Dict = Field(sa_column=Column(JSON))
    
    # Результат
    output_content: Optional[str] = None
    
    # Метаданные
    model_used: str = Field(default="gpt-4o-mini", max_length=50)
    tokens_used: Optional[int] = None
    generation_time_ms: Optional[int] = None  # Время генерации в миллисекундах
    
    # Статус
    status: str = Field(
        default="success",
        max_length=20,
        description="success, failed, cached"
    )
    error_message: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PortfolioView(SQLModel, table=True):
    """Просмотры портфолио (для аналитики)"""
    __tablename__ = "portfolio_views"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    portfolio_id: int = Field(foreign_key="portfolios.id", index=True)
    
    # Информация о просмотре
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
    
    # Геолокация (опционально)
    country: Optional[str] = Field(default=None, max_length=2)
    city: Optional[str] = Field(default=None, max_length=100)
    
    viewed_at: datetime = Field(default_factory=datetime.utcnow)