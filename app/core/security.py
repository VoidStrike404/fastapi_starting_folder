from fastapi import Response

def set_auth_cookies(response: Response, access_token: str, refresh_token: str, config):
    cookie_params = {
        "httponly": True,
        "secure": False, # Change to True when the project moves to HTTPS (production)
        "samesite": "lax"
    }

    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=access_token,
        **cookie_params
    )

    response.set_cookie(
        key=config.JWT_REFRESH_COOKIE_NAME,
        value=refresh_token,
        **cookie_params
    )