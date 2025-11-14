# 🚀 AI Portfolio Builder

<div align="center">

![AI Portfolio Builder](https://img.shields.io/badge/AI-Portfolio%20Builder-purple?style=for-the-badge&logo=sparkles)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)

**Создавайте профессиональные портфолио за минуты с помощью AI** ✨

[Демо](#-демо) • [Возможности](#-возможности) • [Быстрый старт](#-быстрый-старт) • [Документация](#-документация)

</div>

---

## 📖 О проекте

AI Portfolio Builder — это современное веб-приложение, которое использует искусственный интеллект (Google Gemini) для автоматической генерации профессиональных портфолио.

Просто укажите свои навыки, опыт и проекты — AI создаст красивое описание, структурирует информацию и предложит лучший способ презентации.

### 🎯 Для кого?

- 👨‍💻 **Разработчики** — создайте портфолио проектов
- 🎨 **Дизайнеры** — покажите свои работы
- 📝 **Писатели** — продемонстрируйте статьи
- 🎓 **Студенты** — подготовьтесь к поиску работы
- 💼 **Фрилансеры** — привлекайте клиентов

## ✨ Возможности

### 🤖 AI-генерация контента

- **Раздел "Обо мне"** — профессиональное описание на основе ваших данных
- **Описания проектов** — привлекательные тексты о ваших работах
- **Структурирование навыков** — автоматическая группировка по категориям
- **Headline** — цепляющий заголовок профиля

### 🔐 Безопасность

- **JWT аутентификация** с RS256 (асимметричное шифрование)
- **Argon2** для хеширования паролей
- **Rate limiting** — защита от спама
- **Валидация данных** с помощью Pydantic

### 🎨 Frontend

- **Modern UI** — градиенты, анимации, адаптивный дизайн
- **Real-time preview** — мгновенный предпросмотр
- **Intuitive UX** — понятный интерфейс
- **Dark mode ready** — поддержка темной темы (скоро)

### 🔧 Backend

- **FastAPI** — быстрый и современный Python фреймворк
- **PostgreSQL** — надежная реляционная БД
- **SQLModel** — удобная работа с моделями
- **Alembic** — система миграций
- **Docker** — легкий деплой

## 🚀 Быстрый старт

### Предварительные требования

- [Docker Desktop](https://www.docker.com/products/docker-desktop) (включает Docker Compose)
- [Git](https://git-scm.com/downloads)
- OpenSSL (обычно предустановлен)

### Автоматическая установка (рекомендуется)

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/Adilet-tech/ai-portfolio-builder.git
cd ai-portfolio-builder

# 2. Сделайте скрипт исполняемым
chmod +x start.sh

# 3. Запустите!
./start.sh
```

Скрипт автоматически:

- ✅ Проверит зависимости
- ✅ Создаст .env из шаблона
- ✅ Сгенерирует RSA ключи
- ✅ Запустит Docker контейнеры
- ✅ Создаст таблицы БД
- ✅ Откроет приложение в браузере

### Ручная установка

<details>
<summary>Показать шаги ручной установки</summary>

#### 1. Клонирование

```bash
git clone https://github.com/Adilet-tech/ai-portfolio-builder.git
cd ai-portfolio-builder
```

#### 2. Настройка окружения

```bash
# Создайте .env файл
cp .env.example .env

# Отредактируйте .env и добавьте GEMINI_API_KEY
nano .env  # или vim, code, любой редактор
```

Получите API ключ: https://makersuite.google.com/app/apikey

#### 3. Генерация RSA ключей

```bash
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

#### 4. Запуск Docker

```bash
# Сборка и запуск
docker compose up --build -d

# Проверка статуса
docker compose ps
```

#### 5. Инициализация БД

```bash
# Создание миграций
docker compose exec backend alembic revision --autogenerate -m "Initial tables"

# Применение миграций
docker compose exec backend alembic upgrade head
```

#### 6. Открытие приложения

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

</details>

## 🎮 Использование

### 1. Регистрация

1. Откройте http://localhost:3000
2. Переключитесь на "Регистрация"
3. Введите email, username, пароль
4. Нажмите "Создать аккаунт"

### 2. Вход

1. Введите email и пароль
2. Нажмите "Войти"

### 3. Генерация портфолио

1. Перейдите на вкладку "AI Генератор"
2. Заполните форму:
   - **Имя**: Ваше имя
   - **Навыки**: Python, React, Docker (через запятую)
   - **Опыт**: Количество лет
   - **Индустрия**: Web Development
3. Добавьте проекты (опционально)
4. Нажмите "Сгенерировать портфолио"
5. Подождите 10-15 секунд ⏳
6. Готово! ✨

### 4. Просмотр и публикация

1. Вкладка "Предпросмотр" — посмотрите результат
2. Вкладка "Настройки" — опубликуйте портфолио
3. Поделитесь ссылкой!

## 📂 Структура проекта

```
ai-portfolio-builder/
├── backend/                    # FastAPI приложение
│   ├── app/
│   │   ├── api/               # API роутеры
│   │   │   ├── auth.py        # Аутентификация
│   │   │   ├── users.py       # Пользователи
│   │   │   └── portfolio.py   # Портфолио + AI
│   │   ├── ai_service.py      # Gemini AI интеграция
│   │   ├── models.py          # SQLModel модели
│   │   ├── schemas.py         # Pydantic схемы
│   │   ├── security.py        # JWT + Argon2
│   │   ├── dependencies.py    # FastAPI dependencies
│   │   ├── rate_limiter.py    # Rate limiting
│   │   ├── db.py             # Database setup
│   │   └── main.py           # Главный файл
│   ├── alembic/              # Миграции БД
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                  # Next.js приложение
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.js       # Главная страница
│   │   │   ├── layout.js     # Layout
│   │   │   └── globals.css   # Глобальные стили
│   │   └── components/       # React компоненты
│   ├── public/               # Статические файлы
│   ├── Dockerfile
│   ├── package.json
│   └── next.config.js
│
├── docker-compose.yml        # Docker конфигурация
├── .env                      # Переменные окружения
├── .env.example             # Шаблон .env
├── start.sh                 # Скрипт быстрого запуска
├── private_key.pem          # RSA приватный ключ
├── public_key.pem           # RSA публичный ключ
└── README.md
```

## 🔌 API Endpoints

### Аутентификация

```http
POST /api/v1/auth/register
POST /api/v1/auth/token
```

### Пользователи

```http
GET /api/v1/users/me
```

### Портфолио

```http
POST /api/v1/portfolio/generate/about
POST /api/v1/portfolio/generate/project
POST /api/v1/portfolio/generate/skills-structure
POST /api/v1/portfolio/generate/full
GET  /api/v1/portfolio/me
PUT  /api/v1/portfolio/me/publish
GET  /api/v1/portfolio/{id}/public
```

Полная документация: http://localhost:8000/docs

## 🛠️ Полезные команды

### Docker

```bash
# Просмотр логов
docker compose logs -f
docker compose logs -f backend
docker compose logs -f frontend

# Перезапуск сервисов
docker compose restart
docker compose restart backend

# Остановка
docker compose down

# Остановка с удалением volumes (очистка БД)
docker compose down -v

# Пересборка
docker compose up --build
```

### База данных

```bash
# Подключение к PostgreSQL
docker compose exec db psql -U adikus -d portfolio_db

# Создание миграции
docker compose exec backend alembic revision --autogenerate -m "Description"

# Применение миграций
docker compose exec backend alembic upgrade head

# Откат миграции
docker compose exec backend alembic downgrade -1
```

### Debugging

```bash
# Зайти в контейнер backend
docker compose exec backend bash

# Зайти в контейнер frontend
docker compose exec frontend sh

# Проверка переменных окружения
docker compose exec backend env

# Запуск Python в контейнере
docker compose exec backend python
```

## 🧪 Тестирование

### Через Swagger UI

1. Откройте http://localhost:8000/docs
2. Используйте интерактивную документацию
3. Авторизуйтесь через кнопку "Authorize"

### Через curl

```bash
# Регистрация
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123"
  }'

# Получение токена
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"

# Генерация контента (замените YOUR_TOKEN)
curl -X POST "http://localhost:8000/api/v1/portfolio/generate/about" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "John Doe",
    "skills": ["Python", "React"],
    "experience_years": 3
  }'
```

## 🚀 Деплой на продакшн

### Railway.app (Рекомендуется)

1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Создайте новый проект
3. Добавьте PostgreSQL сервис
4. Подключите GitHub репозиторий
5. Настройте переменные окружения
6. Deploy!

### Vercel + Railway

- **Frontend** на Vercel (бесплатно)
- **Backend + DB** на Railway

### DigitalOcean / AWS

Используйте Docker Compose на VPS

## 🤝 Вклад в проект

Contributions приветствуются!

1. Fork проект
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📝 TODO / Roadmap

- [ ] Выбор шаблонов дизайна
- [ ] Экспорт портфолио в HTML/PDF
- [ ] Кастомизация цветовой схемы
- [ ] SEO оптимизация
- [ ] Email уведомления
- [ ] Интеграция с GitHub для автоимпорта проектов
- [ ] Multilanguage support
- [ ] Dark mode
- [ ] Analytics dashboard

## 👨‍💻 Автор

**Adilet** - [@Adilet-tech](https://github.com/Adilet-tech)

## 🙏 Благодарности

- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Google Gemini](https://ai.google.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)

---

<div align="center">

**⭐ Если проект понравился, поставьте звезду! ⭐**

Made with ❤️ ✨

</div>
