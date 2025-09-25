import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import os
import logging
from pydantic import BaseModel, EmailStr
from typing import Optional

class EnquiryData(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    subject: str
    service_type: Optional[str] = None
    budget: Optional[str] = None
    message: str

load_dotenv()

# Email Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Pavishna Groups")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", SMTP_USER)
COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://pavishnagroups.com")
COMPANY_PHONE = os.getenv("COMPANY_PHONE", "+91-1234567890")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_admin_notification_template(enquiry_data: EnquiryData, enquiry_id: str) -> str:
    """HTML template for admin notification"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Enquiry - {COMPANY_NAME}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 300;
        }}
        .content {{
            padding: 30px;
        }}
        .enquiry-card {{
            background: #f8f9ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .detail-row {{
            display: flex;
            margin-bottom: 12px;
            align-items: flex-start;
        }}
        .detail-label {{
            font-weight: 600;
            color: #374151;
            min-width: 100px;
            margin-right: 15px;
        }}
        .detail-value {{
            color: #6b7280;
            flex: 1;
            word-break: break-word;
        }}
        .message-section {{
            background: white;
            border: 2px solid #e5e7eb;
            padding: 20px;
            border-radius: 8px;
            margin: 25px 0;
        }}
        .message-text {{
            line-height: 1.6;
            color: #374151;
            white-space: pre-line;
        }}
        .action-button {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 6px;
            margin: 10px 5px;
            font-weight: 500;
        }}
        .footer {{
            background: #f9fafb;
            padding: 20px;
            text-align: center;
            color: #6b7280;
            font-size: 14px;
        }}
        .urgent-badge {{
            background: #fef3c7;
            color: #92400e;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔔 New Enquiry Received</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">
                Enquiry ID: <strong>{enquiry_id}</strong>
            </p>
        </div>
        
        <div class="content">
            <div class="enquiry-card">
                <h2 style="color: #374151; margin-top: 0; margin-bottom: 20px;">
                    👤 Customer Information
                </h2>
                
                <div class="detail-row">
                    <span class="detail-label">Name:</span>
                    <span class="detail-value"><strong>{enquiry_data.name}</strong></span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Email:</span>
                    <span class="detail-value">
                        <a href="mailto:{enquiry_data.email}" style="color: #667eea;">
                            {enquiry_data.email}
                        </a>
                    </span>
                </div>
                
                {f'<div class="detail-row"><span class="detail-label">Phone:</span><span class="detail-value"><a href="tel:{enquiry_data.phone}" style="color: #667eea;">{enquiry_data.phone}</a></span></div>' if enquiry_data.phone else ''}
                
                {f'<div class="detail-row"><span class="detail-label">Company:</span><span class="detail-value">{enquiry_data.company}</span></div>' if enquiry_data.company else ''}
                
                <div class="detail-row">
                    <span class="detail-label">Subject:</span>
                    <span class="detail-value"><strong>{enquiry_data.subject}</strong></span>
                </div>
                
                {f'<div class="detail-row"><span class="detail-label">Service:</span><span class="detail-value">{enquiry_data.service_type}</span></div>' if enquiry_data.service_type else ''}
                
                {f'<div class="detail-row"><span class="detail-label">Budget:</span><span class="detail-value">{enquiry_data.budget}</span></div>' if enquiry_data.budget else ''}
                
                <div class="detail-row">
                    <span class="detail-label">Received:</span>
                    <span class="detail-value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span>
                </div>
            </div>
            
            <div class="message-section">
                <h3 style="color: #374151; margin-top: 0;">💬 Message</h3>
                <div class="message-text">{enquiry_data.message}</div>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="mailto:{enquiry_data.email}?subject=Re: {enquiry_data.subject}" 
                   class="action-button">
                    📧 Reply to Customer
                </a>
                <a href="tel:{enquiry_data.phone or ''}" 
                   class="action-button" 
                   style="background: #10b981;">
                    📞 Call Customer
                </a>
            </div>
        </div>
        
        <div class="footer">
            <strong>{COMPANY_NAME}</strong><br>
            Automated enquiry notification system<br>
            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""

def get_customer_acknowledgment_template(enquiry_data: EnquiryData, enquiry_id: str) -> str:
    """HTML template for customer acknowledgment"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You - {COMPANY_NAME}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 32px;
            font-weight: 300;
        }}
        .content {{
            padding: 40px;
        }}
        .thank-you-section {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .enquiry-summary {{
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            padding: 20px;
            border-radius: 8px;
            margin: 25px 0;
        }}
        .summary-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 5px 0;
        }}
        .summary-label {{
            font-weight: 600;
            color: #374151;
        }}
        .summary-value {{
            color: #6b7280;
            font-weight: 500;
        }}
        .next-steps {{
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            margin: 25px 0;
            border-radius: 5px;
        }}
        .contact-info {{
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            padding: 20px;
            border-radius: 8px;
            margin: 25px 0;
        }}
        .footer {{
            background: #374151;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .footer a {{
            color: #60a5fa;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Thank You!</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">
                Your enquiry has been received successfully
            </p>
        </div>
        
        <div class="content">
            <div class="thank-you-section">
                <h2 style="color: #374151;">Dear {enquiry_data.name},</h2>
                <p style="color: #6b7280; line-height: 1.6; font-size: 16px;">
                    Thank you for your interest in <strong>{COMPANY_NAME}</strong>. 
                    We have received your enquiry and our team will review it promptly.
                </p>
            </div>
            
            <div class="enquiry-summary">
                <h3 style="color: #065f46; margin-top: 0;">📋 Your Enquiry Summary</h3>
                
                <div class="summary-row">
                    <span class="summary-label">Enquiry ID:</span>
                    <span class="summary-value">{enquiry_id}</span>
                </div>
                
                <div class="summary-row">
                    <span class="summary-label">Subject:</span>
                    <span class="summary-value">{enquiry_data.subject}</span>
                </div>
                
                <div class="summary-row">
                    <span class="summary-label">Submitted:</span>
                    <span class="summary-value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span>
                </div>
                
                {f'<div class="summary-row"><span class="summary-label">Service Type:</span><span class="summary-value">{enquiry_data.service_type}</span></div>' if enquiry_data.service_type else ''}
            </div>
            
            <div class="next-steps">
                <h3 style="color: #1e40af; margin-top: 0;">🚀 What Happens Next?</h3>
                <ul style="color: #374151; line-height: 1.8; margin: 0; padding-left: 20px;">
                    <li><strong>Review:</strong> Our team will carefully review your enquiry within 4 business hours</li>
                    <li><strong>Response:</strong> You'll receive a detailed response within 24 hours</li>
                    <li><strong>Follow-up:</strong> If needed, we'll schedule a call to discuss your requirements</li>
                </ul>
            </div>
            
            <div class="contact-info">
                <h3 style="color: #0c4a6e; margin-top: 0;">📞 Need Immediate Assistance?</h3>
                <p style="color: #0369a1; margin: 10px 0; line-height: 1.6;">
                    <strong>Email:</strong> <a href="mailto:{ADMIN_EMAIL}">{ADMIN_EMAIL}</a><br>
                    {f'<strong>Phone:</strong> <a href="tel:{COMPANY_PHONE}">{COMPANY_PHONE}</a><br>' if COMPANY_PHONE else ''}
                    <strong>Website:</strong> <a href="{COMPANY_WEBSITE}">{COMPANY_WEBSITE}</a>
                </p>
            </div>
            
            <div style="text-align: center; margin: 30px 0; padding: 20px;">
                <p style="color: #6b7280; font-size: 16px;">
                    We appreciate your interest and look forward to working with you!
                </p>
            </div>
        </div>
        
        <div class="footer">
            <p style="margin: 0 0 15px 0;"><strong>{COMPANY_NAME}</strong></p>
            <p style="margin: 0 0 20px 0; opacity: 0.8;">Building Excellence, Delivering Success</p>
            
            <p style="font-size: 12px; opacity: 0.7; margin: 0;">
                This is an automated response. Please do not reply to this email directly.<br>
                © {datetime.now().year} {COMPANY_NAME}. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>
"""

def get_simple_email_template(message: str, subject: str) -> str:
    """Simple HTML template for basic emails"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .content {{
            padding: 30px;
        }}
        .message {{
            line-height: 1.6;
            color: #374151;
            white-space: pre-line;
            font-size: 16px;
        }}
        .footer {{
            background: #f9fafb;
            padding: 20px;
            text-align: center;
            color: #6b7280;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{subject}</h1>
        </div>
        <div class="content">
            <div class="message">{message}</div>
        </div>
        <div class="footer">
            <strong>{COMPANY_NAME}</strong><br>
            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""

def send_email_with_template(to_email: str, subject: str, html_content: str):
    """Send email with HTML template"""
    try:
        msg = MIMEMultipart('alternative')
        msg["From"] = f"{COMPANY_NAME} <{SMTP_USER}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        
        return {"status": "success", "message": "Email sent successfully"}
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return {"status": "error", "message": str(e)}

def send_enquiry_email(enquiry_data: EnquiryData, enquiry_id: str):
    """Send both admin notification and customer acknowledgment emails"""
    try:
        # Send admin notification
        admin_html = get_admin_notification_template(enquiry_data, enquiry_id)
        admin_result = send_email_with_template(
            to_email=ADMIN_EMAIL,
            subject=f"🔔 New Enquiry: {enquiry_data.subject} - {enquiry_data.name}",
            html_content=admin_html
        )
        
        # Send customer acknowledgment
        customer_html = get_customer_acknowledgment_template(enquiry_data, enquiry_id)
        customer_result = send_email_with_template(
            to_email=enquiry_data.email,
            subject=f"✅ Thank you for your enquiry - {COMPANY_NAME}",
            html_content=customer_html
        )
        
        logger.info(f"Enquiry emails sent - ID: {enquiry_id}")
        return {"status": "success", "admin": admin_result, "customer": customer_result}
        
    except Exception as e:
        logger.error(f"Failed to send enquiry emails: {str(e)}")
        return {"status": "error", "message": str(e)}

def send_email(to_email: str, subject: str, message: str):
    """Send simple email with basic template"""
    html_content = get_simple_email_template(message, subject)
    return send_email_with_template(to_email, subject, html_content)
