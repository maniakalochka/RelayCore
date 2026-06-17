from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Relation Database settings
    POSTGRES_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # Broker settings
    RABBITMQ_URL: str
    NODE_HEALTH_CHECK_QUEUE: str

    # Auth settings
    JWT_SECRET: str
    ACCESS_TOKEN_LIFETIME_S: int
    RESET_PASSWORD_TOKEN_SECRET: str
    VERIFICATION_TOKEN_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore
