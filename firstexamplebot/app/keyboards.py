from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder





#klava
# main = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text='Category')],
#     [KeyboardButton(text='Basket'), KeyboardButton(text='Contacts')]
# ], 
#                            resize_keyboard=True, input_field_placeholder="Select menu item", selective=True)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Catalog', callback_data='catalog')],
    [InlineKeyboardButton(text='Basket', callback_data='busket'), InlineKeyboardButton(text='Contacts', callback_data='contacts')]
])


choice_yn_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Yes', callback_data='yes'), InlineKeyboardButton(text='No', callback_data='no')]
])

# settings = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Youtube', url='https://www.youtube.com/watch?v=uRJQJcy3f8w')]
# ])


cars = ['Tesla', 'Mercedes', 'BMW', "Ford"]

async def inline_cars():
    # keyboard = ReplyKeyboardBuilder()
    keyboard = InlineKeyboardBuilder()
    
    for car in cars:
        # keyboard.add(KeyboardButton(text=car))
        keyboard.add(InlineKeyboardButton(text=car, url="https://youtube.com"))
        
    return keyboard.adjust(2).as_markup()