from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

action_choose = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Записаться в очередь🔥")],
   [KeyboardButton(text="Просмотр очереди👀")],
   [KeyboardButton(text="Удалиться из очереди🚫")],
], resize_keyboard=True, input_field_placeholder="Выберите действие...")


approve_data = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="approve_yes")],[InlineKeyboardButton(text="Нет", callback_data="approve_нет")]
])