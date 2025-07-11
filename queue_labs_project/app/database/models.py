from sqlalchemy import BigInteger, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime, timezone

engine = create_async_engine(url="sqlite+aiosqlite:///db_students.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_tg_id = mapped_column(BigInteger, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    name_fio: Mapped[str] = mapped_column(String(100), nullable=False)
    lab_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    sub_group: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    github_link: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        index=True
    )
    
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)