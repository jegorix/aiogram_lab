from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.keyboars import action_choose, approve_data, show_queue_method, find_student_method
from app.validators import Validators
import app.database.requests as rq
from app.database.models import Student
router = Router()

# HANDLE COMMAND START
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    state.clear()
    welcome_text = """
     <b>    Добро пожаловать в бота для очереди лаб!👋</b>
     
    Данный бот, как нетрудно догадаться, позволяет
    записаться в онлайн очередь для сдачи лабы.
    
    📌 <i>Основные команды:</i>
    1. Встать в очередь
    2. Показать текущую очередь
    3. Покинуть очередь

    Первый записавшийся сдаёт первым!🤓
    """
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=action_choose)
    
    
    
    
    
# OBLIGATORY REGISTER FORM 
class RegStudent(StatesGroup):
    name_fio = State()
    lab_number = State()
    sub_group = State()
    github_link = State()
    
    
# OBLIGATORY LabNumber FORM   
class LabNumber(StatesGroup):
    lab_number = State()


class UserData(StatesGroup):
    search_param = State()
    user_credentials = State()

        




# HANDLE COMMAND PUSH TO QUEUE
@router.message(F.text.startswith("Записаться"))
async def cmd_push(message: Message, state: FSMContext):
    await state.set_state(RegStudent.name_fio)
    await message.answer("Хорошо, начнем процесс добавления в очередь!\nВам придется ответить на несколько вопросов")
    # можно добавить ok or no buttons
    await message.answer("Введите ваше фио (Иванов Иван Иванович)")
    
    
@router.message(RegStudent.name_fio)
async def set_fio(message: Message, state: FSMContext):
    if not Validators.fio_validate(message.text): #validator
        await message.reply("Неверный формат ФИО, попробуйте еще раз!")
        return

    await state.update_data(name_fio=message.text)
    await state.set_state(RegStudent.lab_number)
    await message.answer("Введите номер лабораторной работы")
    
    
@router.message(RegStudent.lab_number)
async def set_lab_number(message: Message, state: FSMContext): 
    number = Validators.lab_number_validate(message.text)
    if not number:
        await message.reply("Неверный номер лабораторной работы, введите чисто!")
        return
    
    await state.update_data(lab_number=number)
    await state.set_state(RegStudent.sub_group)
    await message.answer("Введите номер вашей подгруппы")
    
    
@router.message(RegStudent.sub_group)
async def set_subgroup(message: Message, state: FSMContext):
    sub_group_number = Validators.sub_group_validate(message.text)
    
    if not sub_group_number:
        await message.reply("Неверный номер подгруппы, введите 1 или 2!")
        return
    
    await state.update_data(sub_group=sub_group_number)
    await state.set_state(RegStudent.github_link)
    await message.answer("Отправьте ссылку с сайта github с вашим кодом")
    
    
    
@router.message(RegStudent.github_link)
async def get_github_link(message: Message, state: FSMContext):
    github_link = Validators.github_link_validate(message.text)
    if not github_link:
        await message.reply("Неверный формат ссылки, проверьте ее корректность")
        return
    
    await state.update_data(github_link=github_link)
    
    student_data = await state.get_data()
    
    student_text = f"""
     <b>    Проверка предоставленных данных</b>
     
    Пожалуйста еще раз проверьте корректность
    введенных вами данных, так как они будут
    записаны в электронную очередь.
    
    📌 <i>Данные пользователя {message.from_user.username}:</i>
    1. ФИО: {student_data['name_fio']}
    2. Лабораторная работа №{student_data['lab_number']}
    3. Подгруппа-{student_data['sub_group']}
    4. Ссылка на github:\n  {student_data['github_link']}

    Данные верны?
    """
    await message.answer(student_text, parse_mode="HTML", reply_markup=approve_data, disable_web_page_preview=True)
    
    
    
    # INLINE YES APPROVEMENT -> ADD STUDENT TO THE DATABASE
@router.callback_query(F.data == "approve_yes")
async def approve_yes(callback: CallbackQuery, state: FSMContext):
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Загрузка данных в очередь...")
    student_data = await state.get_data()
    
    try:
        await rq.add_student(
            user_tg_id=callback.from_user.id,
            username=callback.from_user.username,
            name_fio=student_data['name_fio'],
            lab_number=student_data['lab_number'],
            sub_group=student_data['sub_group'],
            github_link=student_data['github_link']
        )

        await callback.message.answer("Вы успешно записались в очередь!🎉\n"
                                      "Ваше место в очереди можно посмотреть в разделе\n'Просмотр очереди👀'",
                                      reply_markup=action_choose,
                                      parse_mode='HTML',
                                      disable_web_page_preview=True)
        
    
    except Exception as e:
        await callback.message.answer("Произошла ошибка при сохранении данных❌\n"
                                      "Попробуйте еще раз", reply_markup=action_choose,
                                      parse_mode='HTML',
                                      disable_web_page_preview=True)
        
        print(f"\nОшибка при добавлении в БД: {e}\n")
        
    finally:
        await state.clear()
        
        
    
    #INLINE NO APPROVEMENT
@router.callback_query(F.data == "approve_no")
async def approve_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Отмена...")
    await state.clear()
    await callback.message.edit_text("Процесс записи отменен!\nЧтобы начать сначала нажмите на конпку\n'Записаться в очередь🔥'")
    
    
    
    
    
    
 # QUEUE SHOWING
@router.message(F.text.startswith("Просмотр"))
async def show_menu(message: Message):
    await message.answer("Выберите способ представления очереди", reply_markup=show_queue_method)
    
    
    
async def viewing_message(callback: CallbackQuery | Message, students: list[Student], responce: list[str]) -> list[str]:
    await callback.answer("Загрузка очереди...")
    
    if not students:
        await callback.message.answer("Очередь пуста!")
        return responce
    
    for idx, student in enumerate(students, start=1):
        time_str = student.created_at.strftime("%H:%M %d.%m")
        responce.append(
            f"{idx}. {student.name_fio} - ({student.username})\n"
            f"Лабораторная работа №{student.lab_number}\n"
            f"Подгруппа-{student.sub_group}\n"
            f"Ссылка на github:\n{student.github_link}\n"
            f"Добавлен в {time_str}\n"
        )
    
    return responce
    
    
    
@router.callback_query(F.data == "quick_show")
async def quick_show(callback: CallbackQuery):
   
    students = await rq.get_students_sorted(sort_by_time=True)
    
    responce = ["<b>Текущая очередь отсортированная по времени добавления</b>\n"]

    updated_responce = await viewing_message(callback, students, responce)
    
    if updated_responce:
        await callback.message.answer("\n\n".join(updated_responce), parse_mode="HTML", disable_web_page_preview=True)



@router.callback_query(F.data.startswith("sub_group-"))
async def sub_group_show(callback: CallbackQuery):
    group_number = int(callback.data.split("-")[1])
    students = await rq.get_students_sorted(sub_group=group_number)
    responce = [f"<b>Текущая очередь отсортированная по номеру подгруппы\n\nПодгруппа-{group_number}</b>\n"]
    updated_responce = await viewing_message(callback, students, responce)
    
    if updated_responce:
        await callback.message.answer("\n\n".join(updated_responce), parse_mode="HTML", disable_web_page_preview=True)


@router.callback_query(F.data == "lab_number_show")
async def lab_number_show(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите номер лабораторной работы")
    await state.set_state(LabNumber.lab_number)
    
    
@router.message(LabNumber.lab_number)
async def get_lab_number(message: Message, state: FSMContext):
    number = Validators.lab_number_validate(message.text)
    if not number:
        await message.reply("Неверный номер лабораторной работы, введите число!")
        return
    
    await state.clear()
    
    students = await rq.get_students_sorted(lab_number=number)
    responce = [f"<b>Текущая очередь отсортированная по номеру лабы\nЛаба №{number}</b>\n"]
    
    updated_responce = await viewing_message(message, students, responce)
    
    if updated_responce:
        await message.answer("\n\n".join(updated_responce), parse_mode="HTML", disable_web_page_preview=True)
    
    
    
    
    
     # HANDLE COMMAND FINDSTUDENT
@router.message(Command("find"))
async def cmd_find_student(message: Message):
    await message.answer("Выберите ключевой параметр поиска студента", reply_markup=find_student_method)


@router.callback_query(F.data.startswith("find_by-"))
async def handle_finding(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Обработка запроса...")
    param = callback.data.split('-')[1]
    await state.update_data(search_param=param)
    
    await callback.message.answer(f"Введите {param} пользователя, которого вы хотите найти")
    await state.set_state(UserData.user_credentials)
        
    

@router.message(UserData.user_credentials)
async def get_user_credentials(message: Message, state: FSMContext):
    
    data = await state.get_data()
    param = data['search_param']
    search_value = message.text
    students = None

    
    if param == "id":
        id = Validators.lab_number_validate(message.text)
        if not id:
            await message.reply("Неверный формат telegram id. Попробуйте еще раз!")
            return
            
        students = await rq.get_student_id_or_username(user_tg_id=id)
    
    
    elif param == "username":
        students = await rq.get_student_id_or_username(username=search_value)
        
    elif param == "surname":
        param = "фамилии"
        students = await rq.get_student_id_or_username(surname=search_value)
        
    if not students:
        param = "фамилией" if param == "фамилии" else param
        await message.answer(f"Пользователь с {param}: {search_value} не найден!")
        await state.clear()
        return
        
    responce = [f"<b>Найдено {len(students)} записей для {param}: {search_value}</b>\n\n"]

    responce = await viewing_message(message, students, responce)
    
    if responce:
        await message.answer("\n".join(responce), parse_mode="HTML", disable_web_page_preview=True)

    await state.clear()
    
    
    
    
    
    
    

#     from datetime import datetime

# # Пример вывода в сообщении
# create_time = student.create_at.strftime("%d.%m.%Y %H:%M")
# await message.answer(f"Вы записались в очередь в {create_time} (МСК)")
    

    # await rq.add_student()
    
