from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram import F, Router
import app.keyboards as kb

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

class Register(StatesGroup):
    name = State()
    age = State()
    phone_number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Welcome!', reply_markup=kb.main)
    
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("You have pushed on help button")
    
@router.message(F.text.lower() == 'привет')
async def cmd_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.username}!")
    
@router.message(F.text == 'Каталог')
async def catalog_option(message: Message):
    await message.reply("Выберите категорию товара:", reply_markup=kb.catalog)
    
@router.callback_query(F.data == 't-shirts')
async def t_shirt(callback: CallbackQuery):
    await callback.answer("Вы выбрали категорию", show_alert=True)
    await callback.message.delete()
    await callback.message.answer("Вы выбрали категорию футболок")
    
    
    
# REGISTER STATE
@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')
    
@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')

@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.phone_number)
    await message.answer('Введите ваш номер телефона', reply_markup=kb.get_number)
    
@router.message(Register.phone_number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f"Имя: {data['name']}\nВозраст: {data['age']}\nНомер телефона: {data['phone_number']}")
    await state.clear()