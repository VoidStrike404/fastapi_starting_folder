import os
from datetime import timedelta

from authx import AuthX, AuthXConfig
from dotenv import load_dotenv

load_dotenv()

def get_auth_config():
    config = AuthXConfig()
    config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    config.JWT_TOKEN_LOCATION = ["COOKIES"]

    config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
    config.JWT_REFRESH_COOKIE_NAME = "my_refresh_token"

    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    config.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    return config

def get_auth_security():
    config = get_auth_config()
    security = AuthX(config=config)
    return security

DATABASE_URL = os.getenv("DATABASE_URL")