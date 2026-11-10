import traceback
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logger import logger
from app.core.config import settings


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    
    error_trace = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

    # Logger file me record maintain
    logger.error(
        f"Unhandled Exception on {request.method} {request.url}\n"
        f"Client IP: {request.client.host if request.client else 'Unknown'}\n"
        f"Exception: {str(exc)}\n"
        f"Traceback:\n{error_trace}"
    )

    
    response_content = {
        "status": False,
        "message": "Internal Server Error. Please try again later."
    }

    if not settings.is_prod:
        response_content["error_detail"] = str(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_content
    )