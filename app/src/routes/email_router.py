from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from app.src.utils.email_utils import send_email, send_enquiry_email
from typing import Optional
from uuid import uuid4

email_router = APIRouter(prefix="/email", tags=["Email"] )

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str

class EnquiryData(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    subject: str
    service_type: Optional[str] = None
    budget: Optional[str] = None
    message: str

@email_router.post("/send")
async def send_email_api(request: EmailRequest):
    return send_email(request.to, request.subject, request.body)

@email_router.post("/send-enquiry")
async def send_email_enquiry_api(request: EnquiryData):
    enquiry_id = str(uuid4())
    return send_enquiry_email(request, enquiry_id)
