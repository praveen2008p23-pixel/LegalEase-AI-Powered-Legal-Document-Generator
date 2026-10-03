from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import APP_NAME
from backend.routes import router

app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    description="AI-powered legal document drafting backend."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "service": APP_NAME,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }