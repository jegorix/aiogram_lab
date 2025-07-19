from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import asyncio


class TypingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], # обработчик, принимает некий объект и его словарь данных и возвращает корутину
        event: Message, # что приходит от юзера, с какими событиями работаем
        data: Dict[str, Any] # дополнительная информация, например fsm состояния
    ) -> Any:
        
        # выполнение самого обработчика
        await event.bot.send_chat_action( 
            chat_id=event.chat.id,
            action="typing"
        )
        
        await asyncio.sleep(0.6)
        
        return await handler(event, data)
        