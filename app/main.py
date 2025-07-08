from fastapi import FastAPI
from app.api.v1.routes import router as api_router

app = FastAPI(title="Lawsetu API", description="API for Lawsetu", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}