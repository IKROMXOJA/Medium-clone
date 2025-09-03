from celery import Celery
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings
import asyncio  # 🔹 bu qo‘shildi

celery_app = Celery(__name__, broker=settings.REDIS_URL, backend=settings.REDIS_URL)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_email_async(message: MessageSchema):
    fm = FastMail(conf)
    await fm.send_message(message)

@celery_app.task
def send_verification_email(email: str, token: str):
    message = MessageSchema(
        subject="Verify your account",
        recipients=[email],
        body=f"Click to verify: {settings.FRONTEND_URL}/verify/{token}",
        subtype="plain"
    )
    asyncio.run(send_email_async(message))  # 🔹 async funksiya to‘g‘ri chaqirilmoqda
