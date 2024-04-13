from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlite_db: str
    sqlite_db_url: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
