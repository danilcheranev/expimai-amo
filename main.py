from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="ExpimAI – AI-помощник для amoCRM")

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Проверка статуса сервера
@app.get("/api/status")
def status():
    return {"status": "ExpimAI is running"}

# Панель, которая отрисовывается в iframe внутри amoCRM
@app.get("/amo-panel", response_class=HTMLResponse)
async def amo_panel(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
