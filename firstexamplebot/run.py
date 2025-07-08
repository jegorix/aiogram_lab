import asyncio
from config import TOKEN
from aiogram import Bot, Dispatcher
import logging 
from app.handlers import router
# from app.middlewares import LoggingMiddleware

bot = Bot(token=TOKEN)
dp = Dispatcher()


# dp.message.middleware(LoggingMiddleware())


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit...')