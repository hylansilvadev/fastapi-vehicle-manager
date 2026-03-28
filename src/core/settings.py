from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Por padrão, vamos tentar conectar no PostgreSQL
    DATABASE_URL: str = 'postgresql://postgres:postgres@localhost:5432/postgres'

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )


settings = Settings()
