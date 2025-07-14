from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

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
    [InlineKeyboardButton(text="Поиск по username", callback_data="find_by-username")]
    ]
)