from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN
import logging
from app.handlers import router

from app.database.models import async_main

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    #database create and connect
    await async_main()
    
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExit...\n")