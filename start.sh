#!/bin/bash

# Цвета для красивого вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  AI Portfolio Builder - Quick Start       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker не установлен!${NC}"
    echo -e "${YELLOW}Установите Docker: https://www.docker.com/products/docker-desktop${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose не установлен!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker найден${NC}"

# Проверка .env файла
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Файл .env не найден${NC}"
    echo -e "${BLUE}Создаю .env из шаблона...${NC}"
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Создан .env файл${NC}"
        echo -e "${YELLOW}📝 ВАЖНО: Отредактируйте .env и добавьте GEMINI_API_KEY${NC}"
        echo -e "${YELLOW}   Получить ключ: https://makersuite.google.com/app/apikey${NC}"
        read -p "Нажмите Enter после редактирования .env..."
    else
        echo -e "${RED}❌ .env.example не найден${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Файл .env найден${NC}"
fi

# Проверка RSA ключей
if [ ! -f private_key.pem ] || [ ! -f public_key.pem ]; then
    echo -e "${YELLOW}⚠️  RSA ключи не найдены${NC}"
    echo -e "${BLUE}Генерирую RSA ключи...${NC}"
    
    if command -v openssl &> /dev/null; then
        openssl genrsa -out private_key.pem 2048 2>/dev/null
        openssl rsa -in private_key.pem -pubout -out public_key.pem 2>/dev/null
        echo -e "${GREEN}✅ RSA ключи сгенерированы${NC}"
    else
        echo -e "${RED}❌ OpenSSL не установлен${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ RSA ключи найдены${NC}"
fi

# Остановка старых контейнеров
echo ""
echo -e "${BLUE}🛑 Остановка старых контейнеров...${NC}"
docker-compose down 2>/dev/null || docker compose down 2>/dev/null

# Сборка и запуск
echo ""
echo -e "${BLUE}🔨 Сборка и запуск контейнеров...${NC}"
echo -e "${YELLOW}Это может занять несколько минут при первом запуске${NC}"
docker-compose up --build -d || docker compose up --build -d

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Ошибка при запуске контейнеров${NC}"
    exit 1
fi

# Ожидание запуска backend
echo ""
echo -e "${BLUE}⏳ Ожидание запуска backend...${NC}"
sleep 10

# Проверка работы backend
echo -e "${BLUE}🔍 Проверка backend...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend запущен${NC}"
        break
    fi
    echo -n "."
    sleep 2
done

# Создание миграций
echo ""
echo -e "${BLUE}📊 Настройка базы данных...${NC}"

# Проверяем, нужно ли создавать миграции
MIGRATIONS=$(docker-compose exec -T backend ls alembic/versions/ 2>/dev/null | wc -l)

if [ "$MIGRATIONS" -lt 2 ]; then
    echo -e "${YELLOW}Создание миграций...${NC}"
    docker-compose exec -T backend alembic revision --autogenerate -m "Initial tables" || \
    docker compose exec -T backend alembic revision --autogenerate -m "Initial tables"
fi

echo -e "${YELLOW}Применение миграций...${NC}"
docker-compose exec -T backend alembic upgrade head || \
docker compose exec -T backend alembic upgrade head

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Ошибка при создании таблиц${NC}"
    echo -e "${YELLOW}Попробуйте вручную:${NC}"
    echo -e "${YELLOW}  docker-compose exec backend alembic upgrade head${NC}"
else
    echo -e "${GREEN}✅ База данных настроена${NC}"
fi

# Финальная проверка
echo ""
echo -e "${BLUE}🔍 Проверка всех сервисов...${NC}"
sleep 3

# Проверка каждого сервиса
SERVICES=("db:5432" "backend:8000" "frontend:3000")
ALL_OK=true

for SERVICE in "${SERVICES[@]}"; do
    NAME="${SERVICE%%:*}"
    PORT="${SERVICE##*:}"
    
    if docker-compose ps | grep -q "$NAME.*Up" || docker compose ps | grep -q "$NAME.*Up"; then
        echo -e "${GREEN}✅ $NAME работает${NC}"
    else
        echo -e "${RED}❌ $NAME не запущен${NC}"
        ALL_OK=false
    fi
done

# Итоговое сообщение
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
if [ "$ALL_OK" = true ]; then
    echo -e "${BLUE}║${GREEN}  🎉 Все сервисы успешно запущены!        ${BLUE}║${NC}"
else
    echo -e "${BLUE}║${YELLOW}  ⚠️  Некоторые сервисы не запустились    ${BLUE}║${NC}"
fi
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}🌐 Доступные URL:${NC}"
echo -e "   Frontend: ${BLUE}http://localhost:3000${NC}"
echo -e "   Backend:  ${BLUE}http://localhost:8000${NC}"
echo -e "   API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""

echo -e "${YELLOW}📝 Полезные команды:${NC}"
echo -e "   Логи всех сервисов:  ${BLUE}docker-compose logs -f${NC}"
echo -e "   Логи backend:        ${BLUE}docker-compose logs -f backend${NC}"
echo -e "   Логи frontend:       ${BLUE}docker-compose logs -f frontend${NC}"
echo -e "   Остановить:          ${BLUE}docker-compose down${NC}"
echo -e "   Перезапустить:       ${BLUE}docker-compose restart${NC}"
echo ""

# Предложение открыть браузер
read -p "Открыть frontend в браузере? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000
    elif command -v open &> /dev/null; then
        open http://localhost:3000
    else
        echo -e "${YELLOW}Откройте вручную: http://localhost:3000${NC}"
    fi
fi

echo -e "${GREEN}✨ Готово! Удачной работы!${NC}"