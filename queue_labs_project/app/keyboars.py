from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

action_choose = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Записаться в очередь🔥")],
   [KeyboardButton(text="Просмотр очереди👀")],
   [KeyboardButton(text="Удалиться из очереди🚫")],
], resize_keyboard=True, input_field_placeholder="Выберите действие...")