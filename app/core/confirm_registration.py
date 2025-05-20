from services.service_email import send_email
from core.urls import VERIFICATION_BASE_URL

def mail_body(email):
    verification_url = f"{VERIFICATION_BASE_URL}?email={email}"

    return f"""
        <p>Dear user,</p>
        <p>Thank you for creating an account. Please confirm your email address.</p>
        <p><a href="{verification_url}">Click here to verify your email address</a></p>
        <p>If you did not attempt to register, you can safely ignore this email.</p>
        """


subject = "Email Verification"
sender = "adaptiveproject2025@gmail.com"
password = "whvu qagh hnug ukuz"


def mail_verification_email(email):
    send_email(subject, mail_body(email), sender, email, password)
