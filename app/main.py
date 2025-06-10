from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import auth

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/api/status")
def status():
    return {"status": "ok"}

@app.get("/amo-panel")
def amo_panel(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(auth.router)
