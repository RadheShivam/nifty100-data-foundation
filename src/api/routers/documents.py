from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.get("/")
def documents_root():
    return {
        "message": "Documents router working"
    }