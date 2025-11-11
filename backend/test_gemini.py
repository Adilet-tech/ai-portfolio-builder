"""
Скрипт для тестирования Gemini API
Запуск: docker compose run --rm backend python test_gemini.py
"""

import os
import asyncio
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

try:
    import google.generativeai as genai

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  google-generativeai не установлен")
    print("Установите: pip install google-generativeai")

# --- ИСПРАВЛЕНИЯ: ---
# 1. Ищем ПРАВИЛЬНЫЙ ключ
API_KEY = os.getenv("GOOGLE_API_KEY")
# 2. Читаем имя модели из .env, как в ai_service.py
#    (По умолчанию 'models/gemini-2.5-flash', если в .env не найдено)
MODEL_NAME = os.getenv("GOOGLE_MODEL_NAME", "models/gemini-2.5-flash")
# --- КОНЕЦ ИСПРАВЛЕНИЙ ---


async def test_basic_generation():
    """Базовый тест генерации текста"""
    print("\n" + "=" * 50)
    print("TEST 1: Базовая генерация текста")
    print("=" * 50)

    if not API_KEY:
        print("❌ GOOGLE_API_KEY не найден в .env файле")
        return False

    print(f"✅ API Key найден: {API_KEY[:4]}...")
    print(f"✅ Модель: {MODEL_NAME}")  # <--- Используем переменную MODEL_NAME

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            MODEL_NAME
        )  # <--- Используем переменную MODEL_NAME

        prompt = "Напиши короткое приветствие для портфолио веб-разработчика (максимум 2 предложения)"
        print(f"\n📝 Промпт: {prompt}")
        print("\n⏳ Генерация...")

        response = await model.generate_content_async(prompt)

        print(f"\n✅ Ответ получен:")
        print(f"📄 {response.text}")
        return True

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        return False


async def test_about_section_generation():
    """Тест генерации раздела 'Обо мне'"""
    print("\n" + "=" * 50)
    print("TEST 2: Генерация раздела 'Обо мне'")
    print("=" * 50)

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            MODEL_NAME
        )  # <--- Используем переменную MODEL_NAME

        test_data = {
            "name": "Адилет",
            "skills": ["Python", "React", "FastAPI", "PostgreSQL", "Docker"],
            "experience_years": 3,
            "industry": "Web Development",
        }
        skills_text = ", ".join(test_data["skills"])

        prompt = f"""Напиши профессиональный и привлекательный раздел "Обо мне" для портфолио.
Данные:
- Имя: {test_data["name"]}
- Навыки: {skills_text}
- Опыт: {test_data["experience_years"]} лет
- Индустрия: {test_data["industry"]}
Требования:
1. Текст от первого лица
2. Длина 3-4 абзаца
3. Профессиональный, но дружелюбный тон
Верни только текст без заголовков и форматирования."""

        print(f"\n📝 Тестовые данные (Имя: {test_data['name']}, Навыки: {skills_text})")
        print("\n⏳ Генерация...")

        response = await model.generate_content_async(prompt)

        print(f"\n✅ Сгенерированный текст:")
        print("─" * 50)
        print(response.text)
        print("─" * 50)
        return True

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        return False


async def test_json_generation():
    """Тест генерации структурированного JSON"""
    print("\n" + "=" * 50)
    print("TEST 3: Генерация JSON (структура навыков)")
    print("=" * 50)

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            MODEL_NAME
        )  # <--- Используем переменную MODEL_NAME

        skills = ["React", "Python", "FastAPI", "PostgreSQL", "Docker", "Figma", "Git"]
        skills_text = ", ".join(skills)

        prompt = f"""Сгруппируй следующие навыки по логическим категориям.
Навыки: {skills_text}
Верни результат СТРОГО в JSON формате.
Верни ТОЛЬКО JSON, без пояснений и без markdown форматирования (```json)."""

        print(f"\n📝 Навыки для группировки: {skills_text}")
        print("\n⏳ Генерация...")

        # Новые модели Gemini отлично работают с JSON-режимом
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json"
        )
        response = await model.generate_content_async(
            prompt, generation_config=generation_config
        )
        result_text = response.text.strip()

        print(f"\n✅ Сгенерированный JSON:")
        print(result_text)

        try:
            parsed = json.loads(result_text)
            print("\n✅ JSON валиден!")
            print(f"📊 Категорий: {len(parsed)}")
            for category, items in parsed.items():
                print(f"   - {category}: {', '.join(items)}")
            return True
        except json.JSONDecodeError as e:
            print(f"\n⚠️  JSON невалиден: {e}")
            return False

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        return False


async def test_rate_limits():
    """Тест нескольких последовательных запросов"""
    print("\n" + "=" * 50)
    print("TEST 4: Последовательные запросы (Rate Limits)")
    print("=" * 50)

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            MODEL_NAME
        )  # <--- Используем переменную MODEL_NAME

        print("\n⏳ Выполнение 5 запросов подряд...")

        tasks = []
        for i in range(5):
            prompt = f"Придумай название для проекта #{i+1} на тему искусственного интеллекта (одно слово)"
            tasks.append(model.generate_content_async(prompt))

        responses = await asyncio.gather(*tasks)

        for i, response in enumerate(responses):
            print(f"   {i+1}. {response.text.strip()}")

        print("\n✅ Все запросы выполнены успешно")
        return True

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        if "quota" in str(e).lower() or "rate" in str(e).lower():
            print(
                "💡 Возможно превышен лимит запросов. Проверьте квоты в Google AI Studio."
            )
        return False


async def main():
    """Запуск всех тестов"""
    print("\n" + "🧪 " + "=" * 48)
    print("🧪  ТЕСТИРОВАНИЕ GEMINI API")
    print("🧪 " + "=" * 48)

    if not GEMINI_AVAILABLE:
        print("\n❌ Установите библиотеку: pip install google-generativeai")
        return

    # Тест 1 должен выполниться первым и проверить API-ключ
    test1_passed = await test_basic_generation()
    if not test1_passed:
        print(
            "\n⚠️  Тест 1 не пройден. API-ключ не найден или невалиден. Дальнейшие тесты остановлены."
        )
        results = [False, False, False, False]
    else:
        # Запускаем остальные тесты параллельно
        results = [test1_passed]
        other_tests = await asyncio.gather(
            test_about_section_generation(), test_json_generation(), test_rate_limits()
        )
        results.extend(other_tests)

    # Итоги
    print("\n" + "=" * 50)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 50)

    passed = sum(1 for r in results if r)  # Считаем True
    total = len(results)

    print(f"\n✅ Пройдено: {passed}/{total}")

    if passed == total:
        print("\n🎉 Все тесты пройдены! Gemini API работает корректно.")
    else:
        print("\n⚠️  Некоторые тесты не прошли.")
        print("\n💡 Рекомендации:")
        print("   - Проверьте GOOGLE_API_KEY в .env файле")
        print("   - Убедитесь, что API включен в Google AI Studio")
        print("   - Проверьте квоты и лимиты")


if __name__ == "__main__":
    asyncio.run(main())
