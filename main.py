from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from app.src.utils.email_utils import send_email

app = FastAPI()


class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str

@app.post("/send-email/")
def send_email_endpoint(request: EmailRequest):
    result = send_email(request.to, request.subject, request.body)
    return result