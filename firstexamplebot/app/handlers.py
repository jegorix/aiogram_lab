from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import F, Router

router = Router()


#reply usage
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Hello.\nYour id = {message.from_user.id}\nUsername = {message.from_user.username}\n' \
        f"Your name = {message.from_user.first_name}")
    
#F.text usage and compare with param
@router.message(F.text.lower() == 'как дела?')
async def how_are_you(message: Message):
    await message.answer("I am fine, thx, what about you?")
    
# get photo id [-1] means quality
@router.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(f"Your photo id = {message.photo[-1].file_id}")
    
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