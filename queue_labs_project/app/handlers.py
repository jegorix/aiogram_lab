from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.keyboars import action_choose
from app.validators import Validators

router = Router()

# HANDLE COMMAND START
@router.message(CommandStart())
async def cmd_start(message: Message):
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
class RegStudent(State):
    name_fio = State()
    lab_number = State()
    sub_group = State()
    git_hub_link = State()


# HANDLE COMMAND PUSH TO QUEUE

@router.message(F.text.startswith("Записаться"))
async def cmd_push(message: Message, state: FSMContext):
    state.set_state(RegStudent.name_fio)
    message.answer("Хорошо, начнем процесс добавления в очередь!\nВам придется ответить на несколько вопросов")
    # можно добавить ok or no buttons
    message.answer("Введите ваше фио (Иванов Иван Иванович)")
    
@router.message(RegStudent.name_fio)
async def set_fio(message: Message, state: FSMContext):
    if not Validators.valid_fio(message.text): #validators file?
        message.answer("Извините, неверный формат ФИО, попробуйте еще раз!")
        return

    await state.update_data(name_fio=message.text)
    await state.set_state(RegStudent.lab_number)
    await message.answer("Введите номер лабораторной работы")
    

