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
    
    
    
async def get_student_id_or_username(user_tg_id: int = None, username: str = None, surname: str = None, lab_number = None) -> Student | None:
    async with async_session() as session:
        if user_tg_id:
            result = await session.execute(
                select(Student).where(Student.user_tg_id == user_tg_id)
            )
        elif username:
            result = await session.execute(
                select(Student).where(Student.username == username)
            )
            
        elif surname:
            result = await session.execute(
                select(Student).where(Student.name_fio.startswith(surname.capitalize()))
            )
        
        elif lab_number:
            result = await session.execute(
                select(Student).where(Student.lab_number == lab_number)
            )
            
        return result.scalars().all()
    
    
    

async def delete_student(
    lab_number: int | None = None,
    user_tg_id: int | None = None,
    username: str | None = None,
    surname: str | None = None,
    delete_all: bool = False,
    param: str | bool = False,
    data: str | bool = False

) -> int:
    async with async_session() as session:
        query = select(Student)
        
        if data:
            if param == "user_tg_id":
                user_tg_id = int(data) if isinstance(data, str) and data.isdigit() else data
                
            elif param == "surname":
                surname = data
                
            elif param == "username":
                username = data
        
        
        conditions = []
        if lab_number:
            conditions.append(Student.lab_number == lab_number)
        
        if user_tg_id:
            conditions.append(Student.user_tg_id == user_tg_id)
            
        if surname:
            conditions.append(Student.name_fio.startswith(surname))
            
        if username:
            conditions.append(Student.username == username)
            
        if conditions:
            query = query.where(*conditions)
        
        query = query.order_by(Student.created_at.asc())
        
        result = await session.execute(query)
        students = result.scalars().all()
        
        if not students:
            return 0
        
        if not delete_all:
            await session.delete(students[0])
            await session.commit()
            return 1
        else:
            for student in students:
                await session.delete(student)
                
            await session.commit()
            return len(students)