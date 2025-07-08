from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Каталог')],
        [KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Контакты'), KeyboardButton(text='О нас')]
], resize_keyboard=True, input_field_placeholder='Choose menu option...')

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Футболки', callback_data='t-shirts')],
    [InlineKeyboardButton(text='Кроссовки', callback_data='sneakers')],
    [InlineKeyboardButton(text='Кепки', callback_data='caps')]
])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер телефона', request_contact=True)]],
                                 resize_keyboard=True)