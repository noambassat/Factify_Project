# api/api_main.py
from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(
    title="Factify Document Metadata API",
    description="Mock API for accessing classified and structured document metadata.",
    version="1.0.0"
)

app.include_router(router)

