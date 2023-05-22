from fastapi import (
    BackgroundTasks,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
    status,
)

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List
from models import User
import jwt


config_credentials = dict(dotenv_values(".env"))

conf = ConnectionConfig(
    # MAIL_MAILER=smtp
    # MAIL_HOST=aski.component.astra.co.id
    # MAIL_PORT=25
    # MAIL_USERNAME=online.training@aski.component.astra.co.id
    # MAIL_PASSWORD="MerahPutih123#"
    # MAIL_ENCRYPTION=false
    # MAIL_FROM_ADDRESS="online.training@aski.component.astra.co.id"
    # MAIL_FROM_NAME="${APP_NAME}"
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)


# class EmailSchema(BaseModel):
#     email: List[EmailStr]


async def send_email(email: list, instance: User):
    token_data = {"id": instance.id, "username": instance.username}

    token = jwt.encode(token_data, config_credentials["SECRET"])

    template = f"""
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <title>Document</title>
        </head>

        <body>
            <div style="display: flex; align-items: center; justify-content: center; 
            flex-direction: column;">
                <h3>Account Verification</h3>
                <br>

                <p>Thanks for choosing TOKOTA, please click on the button below
                    to verify your account</p>

                <a style="margin: 1rem; padding: 1rem; border-radius: 0.5rem; 
                    font-size: 1rem; text-decoration: none; background: #0275d8; 
                    color: white;" href=" http://localhost:8000/verification/?token={token}">
                    Verify your email
                </a>

                <p>Please kindly ignore this email if you did not register for
                    TOKOTA and nothing will happend. Thanks
                </p>
            </div>

        </html>
    """

    message = MessageSchema(
        subject="TOKOTA Account Verification Email",
        recipients=email,  # List of recipients
        body=template,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message=message)
