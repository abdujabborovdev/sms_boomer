from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column()
    limit: Mapped[int] = mapped_column()


engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)