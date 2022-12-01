from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..config import get_api_host


conf = ConnectionConfig(
    MAIL_USERNAME="it-aces",
    MAIL_PASSWORD="anqzvckgtmamgbyo",
    MAIL_FROM="it-aces@yandex.ru",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_FROM_NAME="IT-aces scope service",
    MAIL_SSL=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

API_HOST = get_api_host()


async def send_confirm_email(email, code):

    html = f"""
    <p>Email confirmation code</p>
    <p>Your code is</p>
    <p><em>{code}</em></p>
    <p>...or you can just click the link below</p>
    <a href="{API_HOST}/accounts/confirm?email={email}&code={code}">Confirm my email</a>
    """

    message = MessageSchema(
        subject="Email confirmation",
        recipients=[email],
        body=html,
        subtype='html'
        )

    fm = FastMail(conf)
    return await fm.send_message(message, template_name='email.html')
