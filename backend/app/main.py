from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.logger import logger
from app.core.exceptions import global_exception_handler


app = FastAPI(
    title= "Gain Subs",
    version= "1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Global Exception Handler Register
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(api_router, prefix="/api/v1")