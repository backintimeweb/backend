import os
from typing import Any

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL: Any = os.getenv("DATABASE")
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
session = async_session()
Base = declarative_base()
