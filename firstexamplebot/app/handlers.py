from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

from app.middlewares import TestMiddleWare, AntiSpamMiddleware, LoggingMiddleware 

router = Router()

# MIDDLEWARE CONNECT
# router.message.middleware(TestMiddleWare())
# router.message.outer_middleware(TestMiddleWare()) # works anyway
router.message.outer_middleware(AntiSpamMiddleware())
router.message.middleware(LoggingMiddleware()) # works when filter catches


class Reg(StatesGroup):
    name = State()
    number = State()
    


#reply usage
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Hello.\nYour id = {message.from_user.id}\nUsername = {message.from_user.username}\n' \
        f"Your name = {message.from_user.first_name}", reply_markup=kb.main) # or kb.main or kb.settings or await inline_cars
    
#F.text usage and compare with param
@router.message(F.text.lower() == 'как дела?')
async def how_are_you(message: Message):
    await message.answer("I am fine, thx, what about you?")
    
# get photo id [-1] means quality
@router.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(f"Your photo id = {message.photo[-1].file_id}")
    
    
    
# GET STICKER ID
@router.message(F.sticker)
async def get_sticker_id(message: Message):
    await message.answer(f"Your sticker id = {message.sticker.file_id}")    
    

    
# echo answers
# @router.message(F.text)
# async def echo_answer(message: Message):
#     await message.answer(message.text)
    
    
# photo = uniq pic id or url link
@router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMcaGgNpqngDa0ieE198HcwoW1R-doAAmv1MRu8QUFLfizS6-wYVhQBAAMCAAN5AAM2BA',
                               caption='Sasoid', has_spoiler=True)
    


    
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('This is help command')
    
    
@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer("You have selected catalog", show_alert=False)
    # await callback.message.answer('Hello!', reply_markup= await kb.inline_cars())
    await callback.message.edit_text('Hello!', reply_markup= await kb.inline_cars())
    # await callback.message.edit_text('was clicked!')
    
    
def is_phone_number_valid(phone_number: str) ->bool:
    cleaned_phone_number = ''.join(n for n in phone_number if n.isdigit() or n == '+')
    
    if len(cleaned_phone_number) == 13 and cleaned_phone_number.startswith('+375'):
        return True
    
    elif len(cleaned_phone_number) == 12 and cleaned_phone_number.startswith('375'):
        return True
    
    elif len(cleaned_phone_number) == 11 and cleaned_phone_number.startswith('80'):
        return True
    
    return False


    
    # STATE REGISTRATION 
@router.message(Command('reg'))
async def reg_first(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите Ваше имя')
    
    
@router.message(Reg.name)
async def reg_second(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer("Введите номер телефона")
    

@router.message(Reg.number)
async def reg_number(message: Message, state: FSMContext):
    if not is_phone_number_valid(message.text):
        await message.answer("Uncorrect number. Try again!")
        return
    
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f"Thx, register has completed\nYour name: {data['name']}\nYour phone number: {data['number']}")
    
    await state.clear()
    
    
# PIZZA ORDER

class PizzaOrder(StatesGroup):
    name = State()
    number = State()
    adress = State()

@router.message(Command('pizza'))
async def start_order(message: Message, state: FSMContext):
    await state.set_state(PizzaOrder.name)
    await message.answer('Enter your name')
    
@router.message(PizzaOrder.name)
async def second_step_order(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(PizzaOrder.number)
    await message.answer('Enter your phone number')
    
@router.message(PizzaOrder.number)
async def third_step_order(message: Message, state: FSMContext):
    if not is_phone_number_valid(message.text):
        await message.reply('Uncorrect phone number. Please, try again')
        return
    
    await state.update_data(number=message.text)
    await state.set_state(PizzaOrder.adress)
    await message.answer('Enter your adress')
    
    
@router.message(PizzaOrder.adress)
async def forth_step_order(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)
    user_data = await state.get_data()
    await message.answer("Get INFO successfully!\n"
                   f"Name: {user_data['name']}\n"
                   f"Number: {user_data['number']}\n"
                   f"Adress: {user_data['adress']}\n"
                   "\nIs information correct?", reply_markup=kb.choice_yn_keyboard)
    await state.clear()
    
# END PIZZA ORDER



# IMPLEMENT APPROVE INLINE BUTTONS
@router.callback_query(F.data == 'yes')
async def yes_choice(callback: CallbackQuery):
    
    sticker_approved_id = "CAACAgEAAxkBAAIBXGhqV7Xh70uGMbWPiPIAAZi7KA5PqAACGwQAAkEjmEahxBjObzqRLTYE"
    
    await callback.answer("Sounds great! Processing...")
    await callback.message.edit_text("Data received and sent to processing\nPlease wait")
    await callback.message.answer_sticker(sticker=sticker_approved_id)
    
@router.callback_query(F.data == 'no')
async def no_choice(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Ok, so we will try again...")
    await callback.message.delete()
    
    await state.set_state(PizzaOrder.name)
    await callback.message.answer("Re-Entry\nEnter name again")
