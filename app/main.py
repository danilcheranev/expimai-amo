from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app import auth
from app.duplicates import router as duplicates_router

app = FastAPI(
    title="ExpimAI – AI-помощник для amoCRM",
    version="1.0.0",
    description="Модульная FastAPI-интеграция для работы внутри amoCRM"
)

# CORS для iframe
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Статика и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Root + health
@app.get("/", tags=["Root"])
def root():
    return {"status": "ok", "message": "ExpimAI запущен"}

@app.get("/api/status", tags=["Health"])
def status():
    return {"status": "ok"}

# UI iframe
@app.get("/amo-panel", tags=["UI"], response_class=None)
async def amo_panel(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# OAuth
app.include_router(auth.router, prefix="", tags=["Auth"])
# Дубликаты
app.include_router(duplicates_router, prefix="", tags=["Duplicates"])
