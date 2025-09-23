from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from app.src.utils.email_utils import send_email

email_router = APIRouter()

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str

@email_router.post("/send")
async def send_email_api(request: EmailRequest):
    return send_email(request.to, request.subject, request.body)
