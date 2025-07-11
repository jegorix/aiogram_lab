from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Student, async_session
from datetime import datetime, timezone


async def add_student(
    user_tg_id: int,
    username: str,
    name_fio: str, 
    lab_number: int,
    sub_group: int,
    github_link: str
) -> Student:
    async with async_session() as session:
        async with session.begin():
            student = Student(
                user_tg_id=user_tg_id,
                username=username,
                name_fio=name_fio,
                lab_number=lab_number,
                sub_group=sub_group,
                github_link=github_link,
                created_at = datetime.now(timezone.utc)
            )
            session.add(student)
            await session.flush()
            await session.refresh(student)
            return student