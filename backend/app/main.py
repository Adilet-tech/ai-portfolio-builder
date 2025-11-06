from fastapi import FastAPI

app = FastAPI(title="AI Portfolio Builder API")

@app.get("/")
def read_root():
    """
    Тестовый эндпоинт, чтобы проверить, что backend работает.
    """
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/v1/test")
def read_test_endpoint():
    """
    Еще один тестовый эндпоинт.
    """
    return {"data": "API v1 is working"}