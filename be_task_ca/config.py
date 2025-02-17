from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOGGING_")

    LEVEL_ROOT: str = "INFO"
    LEVEL_SQLALCHEMY: str = "WARNING"


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    CONNECTION_STRING: str = "postgresql://postgres:example@localhost:5432/postgres"
    AUTOCOMMIT: bool = False
    AUTOFLUSH: bool = False


class KeycloakSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="KEYCLOAK_")

    URL: str = "http://localhost:8080"
    REALM: str = "my-shop"

    USER_CLIENT_ID: str = "user-client"
    ADMIN_CLIENT_ID: str = "admin-client"
    ADMIN_CLIENT_SECRET: str = "your-secret"

    @computed_field
    @property
    def ISSUER(self) -> str:
        return f"{self.URL}/realms/{self.REALM}"

    @computed_field
    @property
    def TOKEN_URL(self) -> str:
        return f"{self.URL}/realms/{self.REALM}/protocol/openid-connect/token"

    @computed_field
    @property
    def JWKS_URL(self) -> str:
        return f"{self.URL}/realms/{self.REALM}/protocol/openid-connect/certs"

    @computed_field
    @property
    def USER_URL(self) -> str:
        return f"{self.URL}/admin/realms/{self.REALM}/users"
