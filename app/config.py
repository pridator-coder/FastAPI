from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "postgres"
    database_password: str = "3k423n24b2k322k4nj342j"
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    class Config:
        env_file = ".env"
settings = Settings()
