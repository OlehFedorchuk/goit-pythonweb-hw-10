from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from itsdangerous import URLSafeTimedSerializer
from os import getenv
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=getenv("MAIL_PASSWORD"),
    MAIL_FROM=getenv("MAIL_FROM"),
    MAIL_PORT=int(getenv("MAIL_PORT")),
    MAIL_SERVER=getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

serializer = URLSafeTimedSerializer(getenv("SECRET_KEY"))

def create_email_token(email: str) -> str:
    return serializer.dumps(email, salt="email-confirm")


def confirm_email_token(token: str) -> str:
    return serializer.loads(
        token,
        salt="email-confirm",
        max_age=3600  
    )


async def send_verification_email(email: str, host: str, token: str):
    verify_url = f"{host}auth/verify?token={token}"

    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"""
        <h2>Email Verification</h2>
        <p>Click the button below to verify your email:</p>
        <a href="{verify_url}"
           style="display:inline-block;padding:10px 20px;
           background:#4CAF50;color:white;text-decoration:none;">
           VERIFY EMAIL
        </a>
        <p>This link will expire in 1 hour.</p>
        """,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)