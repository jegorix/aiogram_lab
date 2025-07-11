from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.keyboars import action_choose, approve_data
from app.validators import Validators
import app.database.requests as rq
router = Router()

# HANDLE COMMAND START
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    # state.clear()
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
    
    
    
# OBLIGATORY FORM
class RegStudent(StatesGroup):
    name_fio = State()
    lab_number = State()
    sub_group = State()
    github_link = State()






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
    await message.answer(student_text, parse_mode="HTML", reply_markup=approve_data)
    
    
    
    # INLINE YES APPROVEMENT -> ADD STUDENT TO THE DATABASE
@router.callback_query(F.data == "approve_yes")
async def approve_yes(callback: CallbackQuery, state: FSMContext):
    
    await callback.answer("Загрузка данных в очередь...")
    student_data = await state.get_data()
    
    try:
        await rq.add_student(
            user_tg_id=callback.message.from_user.id,
            username=callback.message.from_user.username,
            name_fio=student_data['name_fio'],
            lab_number=student_data['lab_number'],
            sub_group=student_data['sub_group'],
            github_link=student_data['github_link']
        )

        await callback.message.answer("Вы успешно записались в очередь!🎉\n"
                                      "Ваше место в очереди можно посмотреть в разделе\n'Просмотр очереди👀'",
                                      reply_markup=action_choose,
                                      parse_mode='HTML')
        
    
    except Exception as e:
        await callback.message.answer("Произошла ошибка при сохранении данных❌\n"
                                      "Попробуйте еще раз", reply_markup=action_choose,
                                      parse_mode='HTML')
        
        print(f"\nОшибка при добавлении в БД: {e}\n")
        
    finally:
        await state.clear()
    
    

    

    # await rq.add_student()
    
