import httpx
import jwt

from be_task_ca.auth.schema import UserCredentials, UserSignup
from be_task_ca.config import KeycloakSettings
from be_task_ca.exceptions import (
    TokenExpiredError,
    TokenInvalidError,
    TokenMalformedError,
    UserException,
    UserLoginError,
    UserSignupError,
    UserTokenRefreshException,
)

settings = KeycloakSettings()


jwks_client = jwt.PyJWKClient(settings.JWKS_URL, cache_keys=True)


def authenticate_token(token):
    signing_key = jwks_client.get_signing_key_from_jwt(token).key
    algorithm = jwt.get_unverified_header(token).get("alg")

    try:
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=algorithm,
            audience=['account'],
            issuer=settings.ISSUER,
            options={"verify_exp": True},
        )
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token expired")
    except jwt.DecodeError:
        raise TokenMalformedError("Malformed token")
    except jwt.InvalidTokenError as e:
        raise TokenInvalidError(str(e))
    return payload


async def get_admin_token() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.TOKEN_URL,
            data={
                "client_id": settings.ADMIN_CLIENT_ID,
                "client_secret": settings.ADMIN_CLIENT_SECRET,
                "grant_type": "client_credentials",
            },
        )

    if response.status_code != 200:
        raise UserException(status_code=response.status_code, message=response.text)

    return response.json()["access_token"]


async def create_user(user: UserSignup) -> int:
    admin_token = await get_admin_token()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.USER_URL,
            json={
                "username": user.username,
                "email": user.email,
                "enabled": True,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "credentials": [
                    {
                        "type": "password",
                        "value": user.password,
                        "temporary": False,
                    }
                ],
            },
            headers={
                "Authorization": f"Bearer {admin_token}",
            },
        )

    if response.status_code not in [200, 201]:
        raise UserSignupError(status_code=response.status_code, message=response.text)

    return response.status_code


async def login_user(credentials: UserCredentials) -> tuple[int, dict]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.TOKEN_URL,
            data={
                "client_id": settings.USER_CLIENT_ID,
                "grant_type": "password",
                "username": credentials.username,
                "password": credentials.password,
                "otp": credentials.otp,
                "scope": "openid profile email",
            },
        )

    if response.status_code != 200:
        raise UserLoginError(status_code=response.status_code, message=response.text)

    return response.status_code, response.json()


async def refresh_token(refresh_token: str) -> tuple[int, dict]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.TOKEN_URL,
            data={
                "client_id": settings.USER_CLIENT_ID,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        )

    if response.status_code != 200:
        raise UserTokenRefreshException(
            status_code=response.status_code, message=response.text
        )

    return response.status_code, response.json()
