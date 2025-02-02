from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class UserCredentials(BaseModel):
    username: str
    password: str
    otp: str | None = None


class RefreshRequest(BaseModel):
    refresh_token: str


class UserSignup(UserCredentials):
    first_name: str
    last_name: str
    email: str
