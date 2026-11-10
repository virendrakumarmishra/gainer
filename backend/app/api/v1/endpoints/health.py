from fastapi import APIRouter
from app.core.logger import logger

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "message": "Server is up and running"}

@router.get("/")
def test():
    logger.info("Hello Logger")
    return {"status": "ok", "message": "Everything looks good"}

@router.get("/test-error")
def trigger_error():
    # Intentionally crash logic
    result = 1 / 0
    return {"result": result}