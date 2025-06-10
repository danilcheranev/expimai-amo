from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app import auth

# Создаем приложение
app = FastAPI(
    title="ExpimAI – AI-помощник для amoCRM",
    description="Модульная FastAPI-интеграция для работы внутри amoCRM",
    version="1.0.0"
)

# Разрешаем CORS (для iframe amoCRM)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы и шаблоны
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
templates = Jinja2Templates(directory="templates")

# Базовый роут для проверки
@app.get("/", tags=["Root"])
def root():
    return {"status": "ok", "message": "ExpimAI работает"}

# Эндпоинт статуса
@app.get("/api/status", tags=["Health"])
def status():
    return {"status": "ok"}

# Панель в iframe
@app.get("/amo-panel", response_class=None, tags=["UI"])
async def amo_panel(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Подключаем маршруты авторизации и другие
app.include_router(auth.router, prefix="", tags=["Auth"])
