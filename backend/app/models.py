from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Text, Column 
from typing import Optional, List



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str

    # Связь: Один User может иметь много Portfolios
    portfolios: List["Portfolio"] = Relationship(back_populates="user")


class Portfolio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    style: str = Field(index=True) 
    generated_about_me: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Связь "Один ко многим" с User
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="portfolios")

    # Связь: Одно Portfolio может иметь много Projects и Skills
    projects: List["Project"] = Relationship(back_populates="portfolio")
    skills: List["Skill"] = Relationship(back_populates="portfolio")


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str = Field(sa_column=Column(Text))

    # Связь "Один ко многим" с Portfolio
    portfolio_id: int = Field(foreign_key="portfolio.id")
    portfolio: Portfolio = Relationship(back_populates="projects")


class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
    # Связь "Один ко многим" с Portfolio
    portfolio_id: int = Field(foreign_key="portfolio.id")
    portfolio: Portfolio = Relationship(back_populates="skills")