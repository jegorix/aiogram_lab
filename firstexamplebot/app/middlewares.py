from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject

import time


# inner middleware
class TestMiddleWare(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], # обработчик, принимает некий объект и его словарь данных и возвращает корутину
        event: Message, # что приходит от юзера, с какими событиями работаем
        data: Dict[str, Any] # дополнительная информация, например fsm состояния
    ) -> Any:
        
        user = data['event_from_user']
        print(f'\nUser INFO: {user}\n')
        print("\nДействиe до обработчика:")
        result = await handler(event, data) # выполнение самого обработчика
        print("Действие после обработчика:\n")
        return result



class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        print(f"\nNew message received: '{event.text}' from '{event.from_user.username}'\n")
        return await handler(event, data)
    
    
    
class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self):
        self.user_last_message = {}
    
    async def __call__(self,
                 handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                 event: Message,
                 data: Dict[str, Any]
    )->Any:
        user_id = event.from_user.id
        current_time = time.time()
        
        if user_id in self.user_last_message:
            if current_time - self.user_last_message[user_id] < 0.5:
                await event.answer("Do not spam!")
                return 
            
        self.user_last_message[user_id] = current_time
        return await handler(event, data)
        
    
    
# WHAT DATA CONTAINS:
# {
#     'event_from_user': User,  # Объект пользователя, отправившего сообщение
#     'event_chat': Chat,       # Объект чата, куда пришло сообщение
#     'bot': Bot,              # Экземпляр вашего бота
#     'state': FSMContext,     # Текущее состояние пользователя (если используется FSM)
#     'raw_state': str|None,    # Сырое состояние (если используется FSM)
#     'update': Update,        # Полное обновление от Telegram
#     'command': Command,      # Информация о команде (если это команда)
#     'args': list[str],       # Аргументы команды
#     'kwargs': dict[str, Any] # Дополнительные аргументы
# }