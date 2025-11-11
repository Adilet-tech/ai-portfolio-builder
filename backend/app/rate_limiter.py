"""
Rate Limiter для защиты API от злоупотреблений
Использует in-memory хранилище (для продакшна лучше использовать Redis)
"""
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import asyncio
import os


class RateLimiter:
    """
    Простой in-memory rate limiter
    Для продакшна рекомендуется использовать Redis
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000
    ):
        self.requests_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", requests_per_minute))
        self.requests_per_hour = int(os.getenv("RATE_LIMIT_PER_HOUR", requests_per_hour))
        
        # Хранилище запросов: {client_id: [(timestamp, endpoint), ...]}
        self.requests: Dict[str, list] = defaultdict(list)
        
        # Запускаем фоновую очистку старых записей
        asyncio.create_task(self._cleanup_old_entries())
    
    async def _cleanup_old_entries(self):
        """Очистка старых записей каждые 5 минут"""
        while True:
            await asyncio.sleep(300)  # 5 минут
            current_time = datetime.utcnow()
            
            for client_id in list(self.requests.keys()):
                # Удаляем записи старше 1 часа
                self.requests[client_id] = [
                    (ts, ep) for ts, ep in self.requests[client_id]
                    if current_time - ts < timedelta(hours=1)
                ]
                
                # Удаляем пустые ключи
                if not self.requests[client_id]:
                    del self.requests[client_id]
    
    def _get_client_id(self, request: Request) -> str:
        """
        Получение идентификатора клиента
        Использует user_id если авторизован, иначе IP адрес
        """
        # Пытаемся получить user_id из токена
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"
        
        # Fallback на IP адрес
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0]}"
        
        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"
    
    def _count_requests(self, timestamps: list, timeframe: timedelta) -> int:
        """Подсчет запросов в указанном временном окне"""
        current_time = datetime.utcnow()
        return sum(
            1 for ts, _ in timestamps
            if current_time - ts < timeframe
        )
    
    async def check_rate_limit(
        self,
        request: Request,
        endpoint: str = "general"
    ) -> Tuple[bool, dict]:
        """
        Проверка rate limit
        
        Returns:
            (allowed, info_dict)
        """
        client_id = self._get_client_id(request)
        current_time = datetime.utcnow()
        
        # Получаем историю запросов клиента
        timestamps = self.requests[client_id]
        
        # Подсчитываем запросы
        requests_last_minute = self._count_requests(
            timestamps,
            timedelta(minutes=1)
        )
        requests_last_hour = self._count_requests(
            timestamps,
            timedelta(hours=1)
        )
        
        # Информация для заголовков
        info = {
            "limit_minute": self.requests_per_minute,
            "limit_hour": self.requests_per_hour,
            "remaining_minute": max(0, self.requests_per_minute - requests_last_minute),
            "remaining_hour": max(0, self.requests_per_hour - requests_last_hour),
            "reset_minute": int((current_time + timedelta(minutes=1)).timestamp()),
            "reset_hour": int((current_time + timedelta(hours=1)).timestamp()),
        }
        
        # Проверяем лимиты
        if requests_last_minute >= self.requests_per_minute:
            return False, info
        
        if requests_last_hour >= self.requests_per_hour:
            return False, info
        
        # Добавляем текущий запрос
        self.requests[client_id].append((current_time, endpoint))
        
        return True, info


# Глобальный экземпляр rate limiter
rate_limiter = RateLimiter()


async def rate_limit_dependency(request: Request):
    """
    Dependency для FastAPI endpoints
    
    Использование:
    @router.post("/generate", dependencies=[Depends(rate_limit_dependency)])
    """
    endpoint = f"{request.method}:{request.url.path}"
    allowed, info = await rate_limiter.check_rate_limit(request, endpoint)
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later.",
                "limit_minute": info["limit_minute"],
                "limit_hour": info["limit_hour"],
                "reset_minute": info["reset_minute"],
                "reset_hour": info["reset_hour"],
            }
        )
    
    # Добавляем заголовки с информацией о лимитах
    request.state.rate_limit_info = info


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware для автоматического применения rate limiting ко всем запросам
    
    Добавьте в main.py:
    app.add_middleware(rate_limit_middleware)
    """
    # Пропускаем некоторые эндпоинты (например, health check)
    if request.url.path in ["/health", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    endpoint = f"{request.method}:{request.url.path}"
    allowed, info = await rate_limiter.check_rate_limit(request, endpoint)
    
    if not allowed:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later.",
                "limit_minute": info["limit_minute"],
                "limit_hour": info["limit_hour"],
                "reset_minute": info["reset_minute"],
                "reset_hour": info["reset_hour"],
            },
            headers={
                "X-RateLimit-Limit-Minute": str(info["limit_minute"]),
                "X-RateLimit-Limit-Hour": str(info["limit_hour"]),
                "X-RateLimit-Remaining-Minute": str(info["remaining_minute"]),
                "X-RateLimit-Remaining-Hour": str(info["remaining_hour"]),
                "X-RateLimit-Reset-Minute": str(info["reset_minute"]),
                "X-RateLimit-Reset-Hour": str(info["reset_hour"]),
                "Retry-After": "60",
            }
        )
    
    # Продолжаем обработку запроса
    response = await call_next(request)
    
    # Добавляем заголовки rate limit в ответ
    response.headers["X-RateLimit-Limit-Minute"] = str(info["limit_minute"])
    response.headers["X-RateLimit-Remaining-Minute"] = str(info["remaining_minute"])
    response.headers["X-RateLimit-Limit-Hour"] = str(info["limit_hour"])
    response.headers["X-RateLimit-Remaining-Hour"] = str(info["remaining_hour"])
    
    return response