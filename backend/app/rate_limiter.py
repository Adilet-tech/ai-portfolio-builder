from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import asyncio
import os


class RateLimiter:
    """Простой in-memory rate limiter (для продакшна рекомендуется Redis)."""

    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.requests_per_minute = int(
            os.getenv("RATE_LIMIT_PER_MINUTE", requests_per_minute)
        )
        self.requests_per_hour = int(
            os.getenv("RATE_LIMIT_PER_HOUR", requests_per_hour)
        )
        self.requests: Dict[str, list] = defaultdict(list)
        asyncio.create_task(self._cleanup_old_entries())

    async def _cleanup_old_entries(self):
        """Удаляет старые записи каждые 5 минут."""
        while True:
            await asyncio.sleep(300)
            current_time = datetime.utcnow()

            for client_id in list(self.requests.keys()):
                self.requests[client_id] = [
                    (ts, ep)
                    for ts, ep in self.requests[client_id]
                    if current_time - ts < timedelta(hours=1)
                ]
                if not self.requests[client_id]:
                    del self.requests[client_id]

    def _get_client_id(self, request: Request) -> str:
        """Определяет идентификатор клиента (user_id или IP-адрес)."""
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"

        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0]}"

        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"

    def _count_requests(self, timestamps: list, timeframe: timedelta) -> int:
        """Подсчитывает количество запросов за указанный промежуток времени."""
        current_time = datetime.utcnow()
        return sum(1 for ts, _ in timestamps if current_time - ts < timeframe)

    async def check_rate_limit(
        self, request: Request, endpoint: str = "general"
    ) -> Tuple[bool, dict]:
        """Проверяет лимиты запросов и возвращает флаг доступа и метаинформацию."""
        client_id = self._get_client_id(request)
        current_time = datetime.utcnow()
        timestamps = self.requests[client_id]

        requests_last_minute = self._count_requests(timestamps, timedelta(minutes=1))
        requests_last_hour = self._count_requests(timestamps, timedelta(hours=1))

        info = {
            "limit_minute": self.requests_per_minute,
            "limit_hour": self.requests_per_hour,
            "remaining_minute": max(0, self.requests_per_minute - requests_last_minute),
            "remaining_hour": max(0, self.requests_per_hour - requests_last_hour),
            "reset_minute": int((current_time + timedelta(minutes=1)).timestamp()),
            "reset_hour": int((current_time + timedelta(hours=1)).timestamp()),
        }

        if (
            requests_last_minute >= self.requests_per_minute
            or requests_last_hour >= self.requests_per_hour
        ):
            return False, info

        self.requests[client_id].append((current_time, endpoint))
        return True, info


rate_limiter = RateLimiter()


async def rate_limit_dependency(request: Request):
    """FastAPI dependency для ограничения запросов на уровне эндпоинта."""
    endpoint = f"{request.method}:{request.url.path}"
    allowed, info = await rate_limiter.check_rate_limit(request, endpoint)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later.",
                **info,
            },
        )

    request.state.rate_limit_info = info


async def rate_limit_middleware(request: Request, call_next):
    """Middleware для глобального применения rate limiting."""
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
                **info,
            },
            headers={
                "X-RateLimit-Limit-Minute": str(info["limit_minute"]),
                "X-RateLimit-Limit-Hour": str(info["limit_hour"]),
                "X-RateLimit-Remaining-Minute": str(info["remaining_minute"]),
                "X-RateLimit-Remaining-Hour": str(info["remaining_hour"]),
                "X-RateLimit-Reset-Minute": str(info["reset_minute"]),
                "X-RateLimit-Reset-Hour": str(info["reset_hour"]),
                "Retry-After": "60",
            },
        )

    response = await call_next(request)
    response.headers["X-RateLimit-Limit-Minute"] = str(info["limit_minute"])
    response.headers["X-RateLimit-Remaining-Minute"] = str(info["remaining_minute"])
    response.headers["X-RateLimit-Limit-Hour"] = str(info["limit_hour"])
    response.headers["X-RateLimit-Remaining-Hour"] = str(info["remaining_hour"])

    return response
