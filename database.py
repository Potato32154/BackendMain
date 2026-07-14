from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Settings(BaseSettings):
    DATABASE_URL:str

    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    class Config:
        env_file = ".env"
settings = Settings()
engine=create_engine(settings.DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
class Base(DeclarativeBase):
    pass
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()