from fastapi import APIRouter

router = APIRouter(
    prefix="/peers",
    tags=["Peers"]
)

@router.get("/")
def peers_root():
    return {
        "message": "Peers router working"
    }