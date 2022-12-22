import os
import re
import uuid
from app.schemas.user import UserCreate
from typing import Optional, Union
from fastapi import Depends, Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, InvalidPasswordException
from app.models.user import User
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from app.database import get_user_db
from dotenv import load_dotenv
load_dotenv()

SECRET = 'SECRET'
#conf_mail = ConnectionConfig(
#    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
 #   MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
 #   MAIL_FROM=os.getenv('MAIL_FROM'),
 #   MAIL_PORT=int(os.getenv('MAIL_PORT')),
 #   MAIL_SERVER=os.getenv('MAIL_SERVER'),
 #   MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME'),
  #  MAIL_TLS=True,
  #  MAIL_SSL=False,
  #  USE_CREDENTIALS=True,
   # TEMPLATE_FOLDER=f"{os.path.abspath(os.curdir)}/app/templates/email"
#)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        uppercaseRegxp = re.search("[A-Z]", password)
        lowercaseRegExp = re.search("[a-z]", password)
        digitsRegExp = re.search("[0-9]", password)
        specialCharRegExp = re.search("[#?!@$%^&*-]", password)

        if(len(password) < 8):
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )
        if uppercaseRegxp == None:
            raise InvalidPasswordException(
                reason="Password should contain at least one uppercase"
            )
        if lowercaseRegExp == None:
            raise InvalidPasswordException(
                reason="Password should contain at least one lowercase"
            )
        if digitsRegExp == None:
            raise InvalidPasswordException(
                reason="Password should contain at least one digits"
            )
        if specialCharRegExp == None:
            raise InvalidPasswordException(
                reason="Password should contain at least one special characters"
            )  

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        pass

       # email_to = [user.email]

       # message = MessageSchema(
        #   subject=email_content.get('subject'),
            #recipients=email_to,
        #    template_body=email_content.get('body')
        #)

        #fm = FastMail(conf_mail)
        #await fm.send_message(message, template_name="forgot_password.html")
        #print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        email_content = {
            "subject": "Confirmer votre inscription",
            "body": {
                'reset_url': f"{os.getenv('FRONT_URL')}/verify-account/{str(user.id)}/{token}"
            }
        }
        email_to = [user.email]

        #message = MessageSchema(
        #    subject=email_content.get('subject'),
        #    recipients=email_to,
        #    template_body=email_content.get('body')
        #)
        #fm = FastMail(conf_mail)
        #await fm.send_message(message, template_name="verify_account.html")
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
