from fastapi_mail import FastMail
from fastapi_mail import MessageSchema
from fastapi_mail import ConnectionConfig

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
    USE_CREDENTIALS=True
)

serializer = URLSafeTimedSerializer(
    getenv("SECRET_KEY")
)

def create_email_token(email: str):

    return serializer.dumps(
        email,
        salt="email-confirm"
    )

def confirm_email_token(token: str):

    return serializer.loads(
        token,
        salt="email-confirm",
        max_age=3600
    )

async def send_verification_email(
    email: str,
    host: str,
    token: str
):

    verify_url = f"{host}auth/verify/{token}"

    message = MessageSchema(
        subject="Verify email",
        recipients=[email],
        body=f"""
        <h3>Verify email</h3>
        <a href="{verify_url}">
        VERIFY
        </a>
        """,
        subtype="html"
    )

    fm = FastMail(conf)

    await fm.send_message(message)