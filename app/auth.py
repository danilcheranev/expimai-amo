from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def redirect_to_auth():
    return {"msg": "auth endpoint working"}
