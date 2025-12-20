import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('EMAIL_ADDRESS')
SENDER_APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')

def _send_email(to_email: str, subject: str, body: str):
    """
    Private helper function to send emails.
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def send_application_approved_email(to_email: str, password: str, hotel_name: str):
    """
    Sends an approval email with login credentials.
    """

    subject = "Your Hotel Application Has Been Approved!"
    body = f"""
Hello,

Congratulations! Your hotel **{hotel_name}** has been successfully approved.

You can now log in using the temporary credentials below:

Temporary Password: **{password}**

Please make sure to change your password after logging in.

Welcome aboard!
— Mystay Team
    """

    _send_email(to_email, subject, body)


def send_application_rejected_email(to_email: str, hotel_name: str, reason: str = None):
    """
    Sends a rejection email with optional reason.
    """

    subject = "Hotel Application Status"
    reason_text = f"Reason: {reason}\n\n" if reason else ""

    body = f"""
Hello,

Thank you for applying to register your hotel **{hotel_name}**.

Unfortunately, your application has been **rejected** at this time.
{reason_text}
You may reapply after addressing the issues.

Best regards,
— Mystay Team
    """

    _send_email(to_email, subject, body)

def send_password_reset_email(to_email: str, reset_link: str):
    subject = "Reset Your Password"

    body = f"""
        Hello,

        You requested to reset your password.

        Please click the link below to set a new password:
        {reset_link}

        This link will expire in 30 minutes.

        If you did not request this, please ignore this email.

        Best regards,
        Support Team
    """

    _send_email(
        to_email=to_email,
        subject=subject,
        body=body
    )
