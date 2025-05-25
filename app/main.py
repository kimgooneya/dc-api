from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import gallery
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A simple API that scrapes data from DC Inside galleries",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    gallery.router,
    prefix=f"{settings.API_V1_STR}/gallery",
    tags=["gallery"],
)

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "DC Inside Scraper API - Visit /docs for API documentation"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 