from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram import F, Router
import app.keyboards as kb

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.database.requests as rq

router = Router()

# COMMAND START
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в магазин кроссовок!', reply_markup=kb.main)
    
    
@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup= await kb.categories())
    
@router.callback_query(F.data.startswith("category_"))
async def category(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]
    category_choosen = await rq.get_category_name(category_id)
    await callback.answer(f"Вы выбрали категорию {category_choosen.name}")
    await callback.message.answer("Выберите товар по категории",
                                  reply_markup=await kb.items(category_id))
    
@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery):
    item_id = callback.data.split('_')[1]
    item_data = await rq.get_item_name(item_id)
    category = await rq.get_category_name(item_data.category)
    await callback.answer(f"Вы выбрали товар {item_data.name}")
    await callback.message.answer(f"Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}$\nБренд: {category.name}")