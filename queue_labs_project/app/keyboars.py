from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.locals.memory import load_admins
from app.auxiliary import get_user_info
from aiogram import Bot

ADMINS = load_admins()

action_choose = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Записаться в очередь🔥")],
   [KeyboardButton(text="Просмотр очереди👀")],
   [KeyboardButton(text="Удалиться из очереди🚫")],
], resize_keyboard=True, input_field_placeholder="Выберите действие...")


approve_data = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="approve_yes")],[InlineKeyboardButton(text="Нет", callback_data="approve_no")]
])


show_queue_method = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Быстрый просмотр", callback_data='quick_show')],
    [InlineKeyboardButton(text="Подгруппа-1", callback_data="sub_group-1"), InlineKeyboardButton(text="Подгруппа-2",  callback_data="sub_group-2")],
    [InlineKeyboardButton(text="По номеру лабы", callback_data='lab_number_show')]
])


find_student_method = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Поиск по telegram id", callback_data="find_by-id")],
    [InlineKeyboardButton(text="Поиск по username", callback_data="find_by-username")],
    [InlineKeyboardButton(text="Поиск по фамилии", callback_data="find_by-surname")]
    ]
)

delete_student_method = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="по telegram id", callback_data="delete_by-id")],
    [InlineKeyboardButton(text="по username", callback_data="delete_by-username")],
    [InlineKeyboardButton(text="по фамилии", callback_data="delete_by-surname")]
    ]
)


async def inline_admins(bot: Bot):
    keyboard = InlineKeyboardBuilder()
    current_admin = load_admins()
    admins_info = await get_user_info(bot, list(current_admin))
    
    for user_id, firstname, username in admins_info:
        keyboard.add(InlineKeyboardButton(text=f"{firstname}({username})" if firstname else user_id if username else user_id,
                                          callback_data=f"userid_{user_id}"))
        
    keyboard.adjust(1)
    return keyboard.as_markup()