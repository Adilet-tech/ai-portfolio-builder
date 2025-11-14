import os
import json
from typing import Optional, Dict, List
import google.generativeai as genai
from datetime import datetime, timedelta
import hashlib


class GeminiAIService:
    """Сервис для генерации контента портфолио с использованием Google Gemini API."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Environment variable 'GEMINI_API_KEY' is required.")

        genai.configure(api_key=self.api_key)

        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(self.model_name)

        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        self._cache: Dict[str, tuple] = {}
        self.cache_ttl = timedelta(hours=1)

    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        """Создаёт уникальный ключ кеша на основе промпта и параметров."""
        cache_data = json.dumps({"prompt": prompt, **kwargs}, sort_keys=True)
        return hashlib.md5(cache_data.encode()).hexdigest()

    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Возвращает значение из кеша, если оно ещё не устарело."""
        if cache_key in self._cache:
            content, timestamp = self._cache[cache_key]
            if datetime.utcnow() - timestamp < self.cache_ttl:
                return content
            del self._cache[cache_key]
        return None

    def _save_to_cache(self, cache_key: str, content: str):
        """Сохраняет результат в кеш и очищает старые записи."""
        self._cache[cache_key] = (content, datetime.utcnow())
        if len(self._cache) > 100:
            current_time = datetime.utcnow()
            self._cache = {
                k: v
                for k, v in self._cache.items()
                if current_time - v[1] < self.cache_ttl
            }

    def _clean_json_response(self, text: str) -> str:
        """Удаляет markdown и обёртки вокруг JSON-ответа Gemini."""
        text = text.strip()
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)
        if text.startswith("```"):
            text = text.replace("```", "", 1)
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]

        start, end = text.find("{"), text.rfind("}") + 1
        return text[start:end].strip() if start != -1 and end > start else text

    async def generate_about_section(
        self,
        name: str,
        skills: List[str],
        experience_years: Optional[int] = None,
        industry: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """Генерирует раздел 'Обо мне'."""
        cache_key = self._get_cache_key(
            "about",
            name=name,
            skills=skills,
            experience_years=experience_years,
            industry=industry,
        )
        if use_cache and (cached := self._get_from_cache(cache_key)):
            return cached

        skills_text = ", ".join(skills)
        prompt = f"""
Напиши профессиональный и привлекательный раздел "Обо мне" для портфолио.

Данные:
- Имя: {name}
- Навыки: {skills_text}
{f"- Опыт: {experience_years} лет" if experience_years else ""}
{f"- Индустрия: {industry}" if industry else ""}

Требования:
1. От первого лица
2. 3–4 абзаца (300–400 слов)
3. Профессиональный, но дружелюбный тон
4. Без клише и шаблонов
5. На русском языке

Верни только текст без заголовков и форматирования.
"""
        try:
            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )
            content = response.text.strip()
            if use_cache:
                self._save_to_cache(cache_key, content)
            return content
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")

    async def generate_project_description(
        self,
        project_name: str,
        technologies: List[str],
        brief_description: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """Генерирует краткое описание проекта."""
        cache_key = self._get_cache_key(
            "project", name=project_name, tech=technologies, desc=brief_description
        )
        if use_cache and (cached := self._get_from_cache(cache_key)):
            return cached

        tech_text = ", ".join(technologies)
        brief_text = (
            f"\nКраткое описание: {brief_description}" if brief_description else ""
        )
        prompt = f"""
Напиши привлекательное описание проекта для портфолио.

Данные:
- Название: {project_name}
- Технологии: {tech_text}{brief_text}

Требования:
1. 2–3 абзаца (150–250 слов)
2. Подчеркни технические решения и результаты
3. Используй активный залог
4. Без шаблонных фраз
5. На русском языке

Верни только текст описания.
"""
        try:
            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )
            content = response.text.strip()
            if use_cache:
                self._save_to_cache(cache_key, content)
            return content
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")

    async def suggest_skills_structure(
        self, skills: List[str], use_cache: bool = True
    ) -> Dict[str, List[str]]:
        """Группирует навыки по категориям и возвращает структуру в формате JSON."""
        cache_key = self._get_cache_key("skills_structure", skills=sorted(skills))
        if use_cache and (cached := self._get_from_cache(cache_key)):
            try:
                return json.loads(cached)
            except json.JSONDecodeError:
                pass

        skills_text = ", ".join(skills)
        prompt = f"""
Сгруппируй навыки по логическим категориям и верни строго валидный JSON:
Навыки: {skills_text}

Формат:
{{
  "Frontend": ["React"],
  "Backend": ["FastAPI"],
  "Database": ["PostgreSQL"]
}}

Без markdown и пояснений.
"""
        try:
            json_config = {**self.generation_config, "temperature": 0.3}
            response = self.model.generate_content(
                prompt, generation_config=json_config
            )
            content = self._clean_json_response(response.text.strip())
            result = json.loads(content)
            if use_cache:
                self._save_to_cache(cache_key, json.dumps(result))
            return result
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return {"All Skills": skills}
        except Exception as e:
            raise Exception(f"Error generating skills structure: {e}")

    async def generate_headline(
        self,
        name: str,
        skills: List[str],
        industry: Optional[str] = None,
        use_cache: bool = True,
    ) -> str:
        """Создаёт короткий профессиональный headline для портфолио."""
        cache_key = self._get_cache_key(
            "headline", name=name, skills=skills, industry=industry
        )
        if use_cache and (cached := self._get_from_cache(cache_key)):
            return cached

        skills_text = ", ".join(skills[:5])
        prompt = f"""
Создай короткий профессиональный headline для портфолио.

Данные:
- Имя: {name}
- Навыки: {skills_text}
{f"- Индустрия: {industry}" if industry else ""}

Требования:
1. До 12 слов
2. Формат: "[Специальность] с опытом в [область]"
3. Без имени человека
4. На русском языке

Примеры:
- Full-Stack разработчик с фокусом на Python и React
- Backend инженер, создающий масштабируемые системы
"""
        try:
            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )
            content = response.text.strip().strip('"').strip("'")
            if use_cache:
                self._save_to_cache(cache_key, content)
            return content
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")

    async def generate_full_portfolio(
        self, user_data: dict, use_cache: bool = True
    ) -> dict:
        """Формирует полный набор контента портфолио."""
        result = {}

        if "name" in user_data and "skills" in user_data:
            result["headline"] = await self.generate_headline(
                name=user_data["name"],
                skills=user_data["skills"],
                industry=user_data.get("industry"),
                use_cache=use_cache,
            )

            result["about"] = await self.generate_about_section(
                name=user_data["name"],
                skills=user_data["skills"],
                experience_years=user_data.get("experience_years"),
                industry=user_data.get("industry"),
                use_cache=use_cache,
            )

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

        if "skills" in user_data:
            result["skills_structure"] = await self.suggest_skills_structure(
                skills=user_data["skills"], use_cache=use_cache
            )

        return result


try:
    ai_service = GeminiAIService()
except Exception as e:
    print(f"⚠️ Warning: Gemini AI Service initialization failed: {e}")
    ai_service = None
