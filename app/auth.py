from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def test_auth():
    return {"msg": "auth работает"}
