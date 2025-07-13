from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Student, async_session
from datetime import datetime, timezone, timedelta

MOSCOW_TZ = timezone(timedelta(hours=3))

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
                created_at = datetime.now(MOSCOW_TZ)
            )
            session.add(student)
            await session.flush()
            await session.refresh(student)
            return student
        
    
    
async def get_students_sorted(
    lab_number: int | None = None,
    sub_group: int | None = None,
    sort_by_time: bool = True
) -> list[Student]:
    async with async_session() as session:
        query = select(Student)
        
        if lab_number is not None:
            query = query.where(Student.lab_number == lab_number)
            
        if sub_group is not None:
            query = query.where(Student.sub_group == sub_group)
            
        if sort_by_time:
            query = query.order_by(Student.created_at.asc())
        
        else:
            query = query.order_by(
                Student.lab_number.asc(),
                Student.sub_group.asc(),
                Student.created_at.asc()
            )
            
        result = await session.execute(query)
        return result.scalars().all()