from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime

from app.api.routes import api
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="AI Kupci-Dobavljaci",
    description="AI-powered application for processing customer and supplier ledger cards",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path("static")
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(api.router, prefix="/api")

@app.get("/")
async def root(request):
    """Render the main application page."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "current_year": datetime.now().year
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 