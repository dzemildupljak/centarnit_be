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


# from sqlalchemy.orm import Session
# from blog.helpers.hashing import pwd_cxt

#################
# bind = op.get_bind()
# session = Session(bind=bind)
# hs_password = pwd_cxt.hash('sysadmin')
# insert_sysadmin_sql = "INSERT INTO USERS (NAME,EMAIL,ROLE,USERNAME,PASSWORD) VALUES ('sysadmin','sysadmin@mail.com', 'sysadmin','sysadmin','{var_password}')"
# session.execute(insert_sysadmin_sql.format(var_password=hs_password))
#################
