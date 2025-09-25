from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from app.src.routes.email_router import email_router

# ---------------------------
# Email Service Sub-App
# ---------------------------
email_app = FastAPI(title="Pavishna Groups Email API", description="Handles email-related services", version="1.0.0", openapi_url="/openapi.json", docs_url=None, redoc_url=None, root_path="/api/service/email" )

email_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000", "http://13.232.35.2", "https://yourfrontend.com" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Swagger for email app
@email_app.get("/docs", include_in_schema=False)
async def email_docs():
    return get_swagger_ui_html(openapi_url="/service/email/openapi.json", title="Email Service API Docs", swagger_ui_parameters={"defaultModelsExpandDepth": -1}, )

# Attach email router inside email_app
email_router_api = APIRouter()
email_router_api.include_router(email_router, prefix="/email")
email_app.include_router(email_router_api)


# ---------------------------
# Main App (All Pavishna APIs)
# ---------------------------
main_app = FastAPI(title="Pavishna Groups Main API", description="Central API for all Pavishna Groups services", version="1.0.0", docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json", root_path="/api" )

# Global middleware for all services
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000", "http://13.232.35.2", "https://yourfrontend.com" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the email service under /service/email
main_app.mount("/service/email", email_app)

# ✅ If you also want email endpoints to show in main docs:
main_app.include_router(email_router, prefix="/email", tags=["Email"])

# Health check for Main API
@main_app.get("/health", tags=["Health"])
async def main_health_check():
    return {"status": "Success", "service": "Main API", "uptime": "running"}


# Entrypoint
app = main_app
