from fastapi import APIRouter

router = APIRouter(
    prefix="/valuation",
    tags=["Valuation"]
)

@router.get("/")
def valuation_root():
    return {
        "message": "Valuation router working"
    }