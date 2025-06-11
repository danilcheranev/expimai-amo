from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.config import AMO_CLIENT_ID, AMO_REDIRECT_URI

router = APIRouter()

@router.get("/auth")
def start_auth():
    url = (
        f"https://www.amocrm.ru/oauth?"
        f"client_id={AMO_CLIENT_ID}&"
        f"redirect_uri={AMO_REDIRECT_URI}&"
        f"response_type=code&mode=post_message"
    )
    return RedirectResponse(url)

@router.get("/oauth")
async def oauth_callback(code: str):
    # Здесь обмен code → tokens
    return {"received_code": code}
