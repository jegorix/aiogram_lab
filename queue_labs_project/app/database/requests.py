from sqlalchemy import select, asc, desc, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Student, async_session
from datetime import datetime, timezone, timedelta
import asyncio

MOSCOW_TZ = timezone(timedelta(hours=3))
db_write_lock = asyncio.Lock()

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
        
        query = select(Student)
        
        conditions = []
        if user_tg_id:
            conditions.append(Student.user_tg_id == user_tg_id)

        if username:
            conditions.append(Student.username == username)
            
        if surname:
            conditions.append(Student.name_fio.startswith(surname.capitalize()))
        
        if lab_number:
            conditions.append(Student.lab_number == lab_number)
            
        if conditions:
            query = query.where(*conditions)
            
        result = await session.execute(query)
        return result.scalars().all()
    
        # FIX OUTPUT IN DELETING, SHOULD USE CONDITIONS LIST
    
    
    

async def delete_student(
    lab_number: int | None = None,
    user_tg_id: int | None = None,
    username: str | None = None,
    surname: str | None = None,
    delete_all: bool = False,
    **kwargs
    # param: str | bool = False,
    # data: str | bool = False

) -> int:
    async with db_write_lock:
        async with async_session() as session:
            
            conditions = []
            if lab_number:
                conditions.append(Student.lab_number == lab_number)
            
            if user_tg_id:
                conditions.append(Student.user_tg_id == user_tg_id)
                
            if surname:
                conditions.append(Student.name_fio.startswith(surname))
                
            if username:
                conditions.append(Student.username == username)
                
            for key, value in kwargs.items():
                if hasattr(Student, key):
                    conditions.append(getattr(Student, key) == value)
            
            if not conditions:
                return 0
            
            stmt = delete(Student).where(and_(*conditions))
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount
        
        
async def delete_students_by_id(user_ids: list[int], lab_number: int) -> int:
    async with db_write_lock:
        async with async_session() as session:
            result = await session.execute(
                delete(Student).where(
                    Student.user_tg_id.in_(user_ids),
                    Student.lab_number == lab_number
                )
            )
            await session.commit()
            return result.rowcount