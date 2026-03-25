from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.config.settings import settings
from app.database.connection import init_db
from app.routes.candidate_routes import router as candidate_router

app = FastAPI(title=settings.APP_TITLE)

# Resolve absolute paths for static files
STATIC_DIR = os.path.join(settings.BASE_DIR, "static")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include routers
app.include_router(candidate_router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
