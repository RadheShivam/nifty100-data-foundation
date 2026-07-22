from fastapi import APIRouter

router = APIRouter(
    prefix="/screener",
    tags=["Screener"]
)

@router.get("/")
def screener_root():
    return {
        "message": "Screener router working"
    }