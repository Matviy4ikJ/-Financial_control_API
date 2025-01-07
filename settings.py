from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine, AsyncSession)
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra="allow")
    DEBUG: bool = True

    DB_USER: str = 'sqlite'
    DB_PASSWORD: str = "sqlite"
    DB_NAME: str = "financial_control"

    SECRET_KEY: str = "secret_key-123"

    def sqlite_dsn(self) -> str:
        return f"sqlite+aiosqlite:///./{self.DB_NAME}.db"


settings_app = Settings()

DATABASE_URL = settings_app.sqlite_dsn()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_session() -> AsyncSession:
    async with async_session() as sess:
        yield sess
