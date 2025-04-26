from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    database_host: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    test_database_host: str
    test_database_username: str
    test_database_password: str
    test_database_name: str

    model_config = SettingsConfigDict(env_file = os.path.join(os.path.dirname(__file__), '..', '.env'))


settings = Settings()