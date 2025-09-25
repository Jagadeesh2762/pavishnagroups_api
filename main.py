from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.src.routes.email_router import email_router

app = FastAPI(title="Pavishna Groups API", description="Central API for all Pavishna Groups services", version="1.0.0", docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json", root_path="/api" )

# Global CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000", "http://13.232.35.2", "https://yourfrontend.com" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_router, prefix="/service", tags=["Email"])


# Health check
@app.get("/health", tags=["Health"])
async def main_health_check():
    return {"status": "Success", "service": "Pavishna Groups API", "uptime": "running"}
