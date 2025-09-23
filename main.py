from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from app.src.routes.email_router import email_router

email_app = FastAPI(title="Email Service API", description="API for sending emails via SMTP", version="1.0.0", docs_url=None, redoc_url="/redoc",  openapi_url="/email/openapi.json" )

email_app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000", "https://yourfrontend.com" ],  allow_credentials=True,  allow_methods=["*"],  allow_headers=["*"], )

@email_app.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html( openapi_url="/service/email/openapi.json", title="Email Service API Docs", swagger_ui_parameters={"defaultModelsExpandDepth": -1} )

api_router = APIRouter()
api_router.include_router(email_router, prefix="/email")

email_app.include_router(api_router)


# Main entry app
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Mount the email service under /service/email
app.mount("/service", email_app)

# Health check
@email_app.get("/health")
async def health_check():
    return {"status": "Success", "service": "Email API", "uptime": "running"}
