import asyncio
from config import TOKEN
from aiogram import Bot, Dispatcher, F
import logging 

from aiogram.filters import CommandStart, Command
from aiogram.types import Message

bot = Bot(token=TOKEN)
dp = Dispatcher()

#reply usage
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Hello.\nYour id = {message.from_user.id}\nUsername = {message.from_user.username}\n' \
        f"Your name = {message.from_user.first_name}")
    
#F.text usage and compare with param
@dp.message(F.text.lower() == 'как дела?')
async def how_are_you(message: Message):
    await message.answer("I am fine, thx, what about you?")
    
# get photo id [-1] means quality
@dp.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(f"Your photo id = {message.photo[-1].file_id}")
    
# echo answers
# @dp.message(F.text)
# async def echo_answer(message: Message):
#     await message.answer(message.text)
    
    
# photo = uniq pic id or url link
@dp.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMcaGgNpqngDa0ieE198HcwoW1R-doAAmv1MRu8QUFLfizS6-wYVhQBAAMCAAN5AAM2BA',
                               caption='Sasoid', has_spoiler=True)

    
@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('This is help command')
    

async def main():
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit...')