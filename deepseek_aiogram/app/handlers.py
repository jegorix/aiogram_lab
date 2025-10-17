from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.generate import ai_generate

router = Router()

class Generate(StatesGroup):
    wait = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать в бот с интеграцией deepseek.\nНапишите ваш запрос")
    await state.clear()
    
    
    
@router.message(Generate.wait)
async def stop_flood(message: Message):
    await message.answer("Подождите! ваш запрос генерируется")    
    
    
@router.message(F.text)
async def generating(message: Message, state: FSMContext):
    await state.set_state(Generate.wait)
    responce = await ai_generate(message.text)
    await message.answer(responce, parse_mode="Markdown") 
    await state.clear()
    
    

    