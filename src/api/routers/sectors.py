from fastapi import APIRouter

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"]
)

@router.get("/")
def sectors_root():
    return {
        "message": "Sectors router working"
    }