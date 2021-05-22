from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    # MAIL_USERNAME="centarnitnp@gmail.com",
    MAIL_USERNAME="centarnitnp@gmail.com",
    MAIL_PASSWORD='centarnitnp11',
    MAIL_FROM="centarnitnp@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)
