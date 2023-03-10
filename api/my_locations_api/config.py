from os import getenv


class DatabaseConfig:
    DB_ENGINE: str = "postgresql+asyncpg"
    DB_USER: str = getenv("POSTGRES_USER", "user")
    DB_PASSWORD: str = getenv("POSTGRES_PASSWORD", "password")
    DB_HOST: str = getenv("GATEWAY_ADDRESS", "172.28.5.254")
    DB_PORT: str = getenv("POSTGRES_PORT", "5432")
    DB_NAME: str = getenv("POSTGRES_DB", "locations")
