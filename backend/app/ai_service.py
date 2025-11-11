"""
AI Service для генерации контента портфолио с использованием Google Gemini
"""

import os
import json
from typing import Optional, Dict, List
import google.generativeai as genai
from functools import lru_cache
import hashlib
from datetime import datetime, timedelta
import re


class GeminiAIService:
    """Сервис для работы с Google Gemini API"""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        # Конфигурация Gemini
        genai.configure(api_key=self.api_key)

        # Модель (используем актуальное название)
        # Доступные модели: gemini-1.5-flash, gemini-1.5-pro
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(self.model_name)

        # Настройки генерации
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        # Простой кеш для избежания повторных запросов
        self._cache: Dict[str, tuple] = {}  # {cache_key: (content, timestamp)}
        self.cache_ttl = timedelta(hours=1)

    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        """Генерация ключа кеша на основе промпта и параметров"""
        cache_data = json.dumps({"prompt": prompt, **kwargs}, sort_keys=True)
        return hashlib.md5(cache_data.encode()).hexdigest()

    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Получение из кеша если не истек TTL"""
        if cache_key in self._cache:
            content, timestamp = self._cache[cache_key]
            if datetime.utcnow() - timestamp < self.cache_ttl:
                return content
            else:
                del self._cache[cache_key]
        return None

    def _save_to_cache(self, cache_key: str, content: str):
        """Сохранение в кеш"""
        self._cache[cache_key] = (content, datetime.utcnow())

        # Очистка старых записей (простая стратегия)
        if len(self._cache) > 100:
            current_time = datetime.utcnow()
            self._cache = {
                k: v
                for k, v in self._cache.items()
                if current_time - v[1] < self.cache_ttl
            }

    def _clean_json_response(self, text: str) -> str:
        """
        Очистка ответа от markdown и лишнего текста
        Gemini иногда оборачивает JSON в ```json ... ```
        """
        # Удаляем markdown код блоки
        text = text.strip()
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)
        if text.startswith("```"):
            text = text.replace("```", "", 1)
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]

        # Удаляем возможный текст до и после JSON
        # Ищем первую { и последнюю }
        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end > start:
            text = text[start:end]

        return text.strip()

    async def generate_about_section(
        self,
        name: str,
        skills: List[str],
        experience_years: Optional[int] = None,
        industry: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """
        Генерация раздела "Обо мне"
        """
        # Проверка кеша
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

        # Формирование промпта
        skills_text = ", ".join(skills)
        experience_text = (
            f" с {experience_years} годами опыта" if experience_years else ""
        )
        industry_text = f" в сфере {industry}" if industry else ""

        prompt = f"""Напиши профессиональный и привлекательный раздел "Обо мне" для портфолио.

Данные:
- Имя: {name}
- Навыки: {skills_text}
{f"- Опыт: {experience_years} лет" if experience_years else ""}
{f"- Индустрия: {industry}" if industry else ""}

Требования:
1. Текст должен быть от первого лица
2. Длина 3-4 абзаца (примерно 300-400 слов)
3. Профессиональный, но дружелюбный тон
4. Подчеркни уникальность и страсть к делу
5. Не используй клише типа "я страстный специалист"
6. Используй конкретные достижения если они подразумеваются из опыта
7. Пиши на русском языке

Верни только текст без заголовков и форматирования."""

        try:
            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )

            content = response.text.strip()

            # Сохраняем в кеш
            if use_cache:
                self._save_to_cache(cache_key, content)

            return content

        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    async def generate_project_description(
        self,
        project_name: str,
        technologies: List[str],
        brief_description: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """
        Генерация описания проекта
        """
        cache_key = self._get_cache_key(
            "project", name=project_name, tech=technologies, desc=brief_description
        )

        if use_cache:
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached

        tech_text = ", ".join(technologies)
        brief_text = (
            f"\nКраткое описание: {brief_description}" if brief_description else ""
        )

        prompt = f"""Напиши привлекательное описание проекта для портфолио.

Данные:
- Название: {project_name}
- Технологии: {tech_text}{brief_text}

Требования:
1. Длина 2-3 абзаца (150-250 слов)
2. Подчеркни технические решения и результаты
3. Используй активный залог
4. Избегай очевидных фраз
5. Покажи бизнес-ценность проекта
6. Пиши на русском языке

Верни только описание без заголовков."""

        try:
            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )

            content = response.text.strip()

            if use_cache:
                self._save_to_cache(cache_key, content)

            return content

        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    async def suggest_skills_structure(
        self, skills: List[str], use_cache: bool = True
    ) -> Dict[str, List[str]]:
        """
        Группировка навыков по категориям
        """
        cache_key = self._get_cache_key("skills_structure", skills=sorted(skills))

        if use_cache:
            cached = self._get_from_cache(cache_key)
            if cached:
                try:
                    return json.loads(cached)
                except:
                    pass  # Если кеш поврежден, продолжаем

        skills_text = ", ".join(skills)

        prompt = f"""Сгруппируй следующие навыки по логическим категориям.

Навыки: {skills_text}

Верни результат СТРОГО в JSON формате без каких-либо дополнительных пояснений:
{{
  "Frontend": ["React", "..."],
  "Backend": ["FastAPI", "..."],
  "Database": ["PostgreSQL", "..."]
}}

Возможные категории: Frontend, Backend, Database, DevOps, Design, Tools, Soft Skills, Other.
Распредели ВСЕ навыки по подходящим категориям.
Верни ТОЛЬКО валидный JSON, без markdown, без текста до или после JSON."""

        try:
            # Используем более низкую temperature для более предсказуемого JSON
            json_config = self.generation_config.copy()
            json_config["temperature"] = 0.3

            response = self.model.generate_content(
                prompt, generation_config=json_config
            )

            content = response.text.strip()

            # Очистка ответа
            content = self._clean_json_response(content)

            # Парсим JSON
            result = json.loads(content)

            if use_cache:
                self._save_to_cache(cache_key, json.dumps(result))

            return result

        except json.JSONDecodeError as e:
            # Если JSON невалиден, возвращаем простую структуру
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {content}")

            # Fallback: простая группировка
            return {"All Skills": skills}

        except Exception as e:
            raise Exception(f"Error generating skills structure: {str(e)}")

    async def generate_headline(
        self,
        name: str,
        skills: List[str],
        industry: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """
        Генерация короткого заголовка (headline) для портфолио
        Например: "Full-Stack разработчик с фокусом на Python и React"
        """
        cache_key = self._get_cache_key(
            "headline", name=name, skills=skills, industry=industry
        )

        if use_cache:
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached

        skills_text = ", ".join(skills[:5])  # Берем топ-5 навыков
        industry_text = f" в сфере {industry}" if industry else ""

        prompt = f"""Создай короткий профессиональный заголовок (headline) для портфолио.

Данные:
- Имя: {name}
- Ключевые навыки: {skills_text}
{f"- Индустрия: {industry}" if industry else ""}

Требования:
1. Длина: максимум 10-12 слов
2. Формат: "[Специальность] с опытом в [технологии/область]"
3. Конкретный и привлекательный
4. Без имени человека в заголовке
5. На русском языке

Примеры хороших заголовков:
- "Full-Stack разработчик с фокусом на Python и React"
- "Frontend инженер, создающий современные веб-приложения"
- "Backend разработчик, специализирующийся на высоконагруженных системах"

Верни только заголовок, без кавычек и пояснений."""

        try:
            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )

            content = response.text.strip().strip('"').strip("'")

            if use_cache:
                self._save_to_cache(cache_key, content)

            return content

        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    async def generate_full_portfolio(
        self, user_data: dict, use_cache: bool = True
    ) -> dict:
        """
        Генерация полного контента портфолио
        """
        result = {}

        # Генерация headline
        if "name" in user_data and "skills" in user_data:
            result["headline"] = await self.generate_headline(
                name=user_data["name"],
                skills=user_data["skills"],
                industry=user_data.get("industry"),
                use_cache=use_cache,
            )

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
            for project in user_data["projects"]:
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
                        "url": project.get("url"),
                        "github_url": project.get("github_url"),
                    }
                )

        # Структурирование навыков
        if "skills" in user_data:
            result["skills_structure"] = await self.suggest_skills_structure(
                skills=user_data["skills"], use_cache=use_cache
            )

        return result


# Глобальный экземпляр сервиса
try:
    ai_service = GeminiAIService()
except Exception as e:
    print(f"⚠️  Warning: Could not initialize Gemini AI Service: {e}")
    ai_service = None
