import asyncio
from config import TOKEN
from aiogram import Bot, Dispatcher
import logging 



bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit...')