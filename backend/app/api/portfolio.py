"""
API роутер для работы с портфолио и AI генерацией
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import BaseModel, Field

from app.db import get_session
from app.dependencies import get_current_user
from app.models import User, Portfolio
from app.ai_service import ai_service
from app.rate_limiter import rate_limit_dependency


router = APIRouter(prefix="/api/v1/portfolio", tags=["Portfolio"])


# ==================== Schemas ====================

class ProjectInput(BaseModel):
    """Схема для ввода данных о проекте"""
    name: str = Field(..., min_length=1, max_length=200)
    technologies: List[str] = Field(default_factory=list)
    brief_description: Optional[str] = Field(None, max_length=500)
    url: Optional[str] = None
    github_url: Optional[str] = None


class GenerateAboutRequest(BaseModel):
    """Запрос на генерацию раздела 'Обо мне'"""
    name: str
    skills: List[str] = Field(..., min_items=1)
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    industry: Optional[str] = None


class GenerateProjectRequest(BaseModel):
    """Запрос на генерацию описания проекта"""
    project_name: str
    technologies: List[str]
    brief_description: Optional[str] = None


class GenerateFullPortfolioRequest(BaseModel):
    """Запрос на генерацию полного портфолио"""
    name: str
    skills: List[str]
    experience_years: Optional[int] = None
    industry: Optional[str] = None
    projects: List[ProjectInput] = Field(default_factory=list)


class PortfolioResponse(BaseModel):
    """Ответ с данными портфолио"""
    id: int
    user_id: int
    about_me: Optional[str]
    skills_structured: Optional[dict]
    projects: Optional[List[dict]]
    template_id: Optional[str]
    is_published: bool


# ==================== Endpoints ====================

@router.post(
    "/generate/about",
    dependencies=[Depends(rate_limit_dependency)],
    response_model=dict
)
async def generate_about_section(
    request: GenerateAboutRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Генерация раздела "Обо мне" с помощью AI
    
    **Rate Limit**: 60 запросов/минута, 1000 запросов/час
    """
    try:
        about_text = await ai_service.generate_about_section(
            name=request.name,
            skills=request.skills,
            experience_years=request.experience_years,
            industry=request.industry
        )
        
        return {
            "success": True,
            "content": about_text
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate content: {str(e)}"
        )


@router.post(
    "/generate/project",
    dependencies=[Depends(rate_limit_dependency)],
    response_model=dict
)
async def generate_project_description(
    request: GenerateProjectRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Генерация описания проекта с помощью AI
    
    **Rate Limit**: 60 запросов/минута, 1000 запросов/час
    """
    try:
        description = await ai_service.generate_project_description(
            project_name=request.project_name,
            technologies=request.technologies,
            brief_description=request.brief_description
        )
        
        return {
            "success": True,
            "content": description
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate content: {str(e)}"
        )


@router.post(
    "/generate/skills-structure",
    dependencies=[Depends(rate_limit_dependency)],
    response_model=dict
)
async def structure_skills(
    skills: List[str],
    current_user: User = Depends(get_current_user)
):
    """
    Автоматическая группировка навыков по категориям
    
    **Rate Limit**: 60 запросов/минута, 1000 запросов/час
    """
    try:
        structure = await ai_service.suggest_skills_structure(skills)
        
        return {
            "success": True,
            "structure": structure
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to structure skills: {str(e)}"
        )


@router.post(
    "/generate/full",
    dependencies=[Depends(rate_limit_dependency)],
    response_model=dict
)
async def generate_full_portfolio(
    request: GenerateFullPortfolioRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Генерация полного портфолио со всеми разделами
    
    **Rate Limit**: 60 запросов/минута, 1000 запросов/час
    
    Этот эндпоинт:
    1. Генерирует раздел "Обо мне"
    2. Генерирует описания всех проектов
    3. Структурирует навыки по категориям
    4. Сохраняет результат в базу данных
    """
    try:
        # Подготовка данных
        user_data = {
            "name": request.name,
            "skills": request.skills,
            "experience_years": request.experience_years,
            "industry": request.industry,
            "projects": [p.model_dump() for p in request.projects]
        }
        
        # Генерация контента
        generated_content = await ai_service.generate_full_portfolio(user_data)
        
        # Проверяем, есть ли уже портфолио у пользователя
        statement = select(Portfolio).where(Portfolio.user_id == current_user.id)
        existing_portfolio = session.exec(statement).first()
        
        if existing_portfolio:
            # Обновляем существующее
            existing_portfolio.about_me = generated_content.get("about")
            existing_portfolio.skills_structured = generated_content.get("skills_structure")
            existing_portfolio.projects = generated_content.get("projects")
            portfolio = existing_portfolio
        else:
            # Создаем новое
            portfolio = Portfolio(
                user_id=current_user.id,
                about_me=generated_content.get("about"),
                skills_structured=generated_content.get("skills_structure"),
                projects=generated_content.get("projects"),
                is_published=False
            )
            session.add(portfolio)
        
        session.commit()
        session.refresh(portfolio)
        
        return {
            "success": True,
            "portfolio_id": portfolio.id,
            "content": generated_content
        }
    
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate portfolio: {str(e)}"
        )


@router.get("/me", response_model=PortfolioResponse)
async def get_my_portfolio(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Получение портфолио текущего пользователя"""
    statement = select(Portfolio).where(Portfolio.user_id == current_user.id)
    portfolio = session.exec(statement).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found. Create one first."
        )
    
    return portfolio


@router.put("/me/publish")
async def publish_portfolio(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Публикация/снятие с публикации портфолио"""
    statement = select(Portfolio).where(Portfolio.user_id == current_user.id)
    portfolio = session.exec(statement).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    portfolio.is_published = not portfolio.is_published
    session.commit()
    
    return {
        "success": True,
        "is_published": portfolio.is_published,
        "message": "Portfolio published" if portfolio.is_published else "Portfolio unpublished"
    }


@router.get("/{portfolio_id}/public")
async def get_public_portfolio(
    portfolio_id: int,
    session: Session = Depends(get_session)
):
    """Получение опубликованного портфолио (публичный доступ)"""
    statement = select(Portfolio).where(
        Portfolio.id == portfolio_id,
        Portfolio.is_published == True
    )
    portfolio = session.exec(statement).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found or not published"
        )
    
    # Получаем данные пользователя (без чувствительной информации)
    user = session.get(User, portfolio.user_id)
    
    return {
        "portfolio": portfolio,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }