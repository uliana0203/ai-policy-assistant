import os
from typing import Dict
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# SendGrid Email Utility for AI Policy Research Assistant
# ==========================================================

def send_email(subject: str, html_body: str, recipient: str) -> Dict[str, str]:
    """
    Sends an HTML email using SendGrid.
    Uses API key and sender email from environment variables.

    Required .env variables:
        SENDGRID_API_KEY=<your_sendgrid_key>
        SENDER_EMAIL=<verified_sender_email>
    """
    api_key = os.environ.get("SENDGRID_API_KEY")
    sender_email = os.environ.get("SENDER_EMAIL")

    # Validate environment setup
    if not api_key:
        print("SENDGRID_API_KEY not found in environment!")
        return {"status": "error", "message": "Missing SENDGRID_API_KEY"}

    if not sender_email:
        print("SENDER_EMAIL not found in environment!")
        return {"status": "error", "message": "Missing SENDER_EMAIL"}

    try:
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        from_email = Email(sender_email)
        to_email = To(recipient)
        content = Content("text/html", html_body)
        mail = Mail(from_email, to_email, subject, content).get()

        response = sg.client.mail.send.post(request_body=mail)

        print(f"Email sent to: {recipient} | Status: {response.status_code}")
        return {"status": "success", "recipient": recipient}

    except Exception as e:
        print(f"Email sending error: {e}")
        return {"status": "error", "message": str(e)}
