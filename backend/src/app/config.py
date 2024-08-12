from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    sqlalchemy_db_url: str

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
