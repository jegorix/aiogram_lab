from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

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
    await message.answer(welcome_text, parse_mode="HTML")