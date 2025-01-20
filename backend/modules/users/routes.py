from fastapi import APIRouter


router = APIRouter()


@router.get("/health", tags=["Health check"])
async def health_check():
    return {"status": "ok"}
