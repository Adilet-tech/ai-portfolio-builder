"""
AI Service для генерации контента портфолио
Работает на Google Gemini API (gemini-2.5-flash-preview)
Включает обработку ошибок, кеширование и streaming
"""

import os
import json
import hashlib
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from functools import lru_cache
from fastapi import HTTPException
import google.generativeai as genai


class AIService:
    """Сервис для работы с Google Gemini API"""

    def __init__(self):
        # 1. Используем GOOGLE_API_KEY из .env
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            print(f"КРИТИЧЕСКАЯ ОШИБКА: Не удалось настроить Google API. {e}")

        # 2. Используем GOOGLE_MODEL_NAME из .env
        self.model_name = os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash-preview")

        # 3. Настройки по умолчанию для Gemini
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]

        # 4. Инициализируем модель Gemini
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )

        # 5. Твоя логика кеширования (остается без изменений!)
        self._cache: Dict[str, tuple] = {}  # {cache_key: (content, timestamp)}
        self.cache_ttl = timedelta(hours=1)

    # --- Твои функции кеширования (без изменений) ---
    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        cache_data = json.dumps({"prompt": prompt, **kwargs}, sort_keys=True)
        return hashlib.md5(cache_data.encode()).hexdigest()

    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        if cache_key in self._cache:
            content, timestamp = self._cache[cache_key]
            if datetime.utcnow() - timestamp < self.cache_ttl:
                return content
            else:
                del self._cache[cache_key]
        return None

    def _save_to_cache(self, cache_key: str, content: str):
        self._cache[cache_key] = (content, datetime.utcnow())
        if len(self._cache) > 100:
            current_time = datetime.utcnow()
            self._cache = {
                k: v
                for k, v in self._cache.items()
                if current_time - v[1] < self.cache_ttl
            }

    # --- Конец функций кеширования ---

    async def generate_about_section(
        self,
        name: str,
        skills: List[str],
        experience_years: Optional[int] = None,
        industry: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """Генерация раздела "Обо мне" (на Gemini)"""

        cache_key = self._get_cache_key(
            "about",
            name=name,
            skills=skills,
            experience_years=experience_years,
            industry=industry,
        )

        if use_cache:
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached

        # Твой промпт (без изменений)
        skills_text = ", ".join(skills)
        prompt_data = f"""Данные:
- Имя: {name}
- Навыки: {skills_text}
{f"- Опыт: {experience_years} лет" if experience_years else ""}
{f"- Индустрия: {industry}" if industry else ""}

Требования:
1. Текст должен быть от первого лица
2. Длина 3-4 абзаца
3. Профессиональный, но дружелюбный тон
4. Подчеркни уникальность и страсть к делу
5. Не используй клише типа "я страстный специалист"
6. Используй конкретные достижения если они подразумеваются из опыта

Верни только текст без заголовков и форматирования."""

        # Системный промпт для Gemini
        system_prompt = "Ты профессиональный копирайтер, специализирующийся на создании портфолио и резюме."
        full_prompt = f"{system_prompt}\n\n{prompt_data}"

        try:
            # 6. Заменяем вызов OpenAI на Gemini (асинхронный)
            response = await self.model.generate_content_async(full_prompt)
            content = response.text.strip()

            if use_cache:
                self._save_to_cache(cache_key, content)

            return content

        except Exception as e:
            print(f"ОШИБКА GEMINI API: {e}")
            raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")

    async def generate_project_description(
        self,
        project_name: str,
        technologies: List[str],
        brief_description: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """Генерация описания проекта (на Gemini)"""

        cache_key = self._get_cache_key(
            "project", name=project_name, tech=technologies, desc=brief_description
        )

        if use_cache:
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached

        # Твой промпт (без изменений)
        tech_text = ", ".join(technologies)
        brief_text = (
            f"\nКраткое описание: {brief_description}" if brief_description else ""
        )

        prompt_data = f"""Данные:
- Название: {project_name}
- Технологии: {tech_text}{brief_text}

Требования:
1. Длина 2-3 абзаца
2. Подчеркни технические решения и результаты
3. Используй активный залог
4. Избегай очевидных фраз
5. Покажи бизнес-ценность проекта

Верни только описание без заголовков."""

        system_prompt = "Ты технический писатель, создающий описания проектов для портфолио разработчиков."
        full_prompt = f"{system_prompt}\n\n{prompt_data}"

        try:
            # 7. Заменяем вызов OpenAI на Gemini (асинхронный)
            response = await self.model.generate_content_async(full_prompt)
            content = response.text.strip()

            if use_cache:
                self._save_to_cache(cache_key, content)

            return content

        except Exception as e:
            print(f"ОШИБКА GEMINI API: {e}")
            raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")

    async def suggest_skills_structure(
        self, skills: List[str], use_cache: bool = True
    ) -> Dict[str, List[str]]:
        """Группировка навыков по категориям (на Gemini)"""

        cache_key = self._get_cache_key("skills_structure", skills=sorted(skills))

        if use_cache:
            cached_content = self._get_from_cache(cache_key)
            if cached_content:
                try:
                    return json.loads(cached_content)
                except json.JSONDecodeError:
                    del self._cache[cache_key]  # Удаляем "сломанный" кеш

        # Твой промпт (без изменений, он идеален для Gemini)
        skills_text = ", ".join(skills)
        prompt_data = f"""Сгруппируй следующие навыки по логическим категориям.

Навыки: {skills_text}

Верни результат СТРОГО в JSON формате:
{{
  "Frontend": ["React", "..."],
  "Backend": ["FastAPI", "..."],
  "Другое": ["..."]
}}

Категории могут быть: Frontend, Backend, Database, DevOps, Design, Tools, Soft Skills и т.д.
Верни ТОЛЬКО JSON, без пояснений."""

        system_prompt = "Ты эксперт в структурировании технических навыков. Всегда отвечай только валидным JSON."
        full_prompt = f"{system_prompt}\n\n{prompt_data}"

        try:
            # 8. Задаем Gemini Config для принудительного JSON
            json_generation_config = genai.GenerationConfig(
                response_mime_type="application/json"
            )

            # 9. Заменяем вызов OpenAI на Gemini (асинхронный)
            response = await self.model.generate_content_async(
                full_prompt,
                generation_config=json_generation_config,  # <--- Принудительный JSON
            )

            content = response.text.strip()

            # Парсим JSON
            result = json.loads(content)

            if use_cache:
                self._save_to_cache(cache_key, content)

            return result

        except (Exception, json.JSONDecodeError) as e:
            print(f"ОШИБКА GEMINI API (JSON): {e}")
            raise HTTPException(
                status_code=500, detail=f"Error generating skills structure: {e}"
            )

    #
    # 10. Твоя функция-оркестратор (БЕЗ ИЗМЕНЕНИЙ)
    #
    async def generate_full_portfolio(
        self, user_data: dict, use_cache: bool = True
    ) -> dict:
        """
        Генерация полного контента портфолио
        (Эта функция работает без изменений, т.к. она просто
         вызывает другие методы этого класса)
        """
        result = {}

        # Генерация "Обо мне"
        if "name" in user_data and "skills" in user_data:
            result["about"] = await self.generate_about_section(
                name=user_data["name"],
                skills=user_data["skills"],
                experience_years=user_data.get("experience_years"),
                industry=user_data.get("industry"),
                use_cache=use_cache,
            )

        # Генерация описаний проектов
        if "projects" in user_data:
            result["projects"] = []
            for project in user_data.get("projects", []):
                if not project.get("name"):
                    continue  # Пропускаем пустые проекты
                description = await self.generate_project_description(
                    project_name=project["name"],
                    technologies=project.get("technologies", []),
                    brief_description=project.get("brief_description"),
                    use_cache=use_cache,
                )
                result["projects"].append(
                    {
                        "name": project["name"],
                        "description": description,
                        "technologies": project.get("technologies", []),
                    }
                )

        # Структурирование навыков
        if "skills" in user_data and user_data["skills"]:
            result["skills_structure"] = await self.suggest_skills_structure(
                skills=user_data["skills"], use_cache=use_cache
            )

        return result


# Глобальный экземпляр сервиса (без изменений)
ai_service = AIService()
