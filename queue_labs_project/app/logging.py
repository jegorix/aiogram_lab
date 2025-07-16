import logging
from aiogram.types import Message, CallbackQuery
from datetime import datetime

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logging/bot_logging.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("BotLogger")

logger = setup_logger()

def log_event(event: Message | CallbackQuery, action: str = ""):
    user = event.from_user
    action_text = action
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    if not action_text:
        if isinstance(event, Message):
            action_text = event.text or "Message without text"
        elif isinstance(event, CallbackQuery):
            action_text = str(event.data) or "Callback without data"
    
    log_message = (
        f"[{current_time}] | "
        f"User: {user.id} | "
        f"Username: @{user.username} | "
        f"Name: {user.first_name} | "
        f"Action: {action_text}\n"
    )
    logger.info(log_message)