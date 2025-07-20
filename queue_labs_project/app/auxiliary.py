from aiogram import Bot 

async def get_user_info(bot: Bot, users_id: list[int]) -> list:
    names = []
    try:
        for user_id in users_id:
            user = await bot.get_chat(user_id)
            names.append((user_id, user.first_name, user.username))
    except Exception as e:
        print(f"Ошибка при получении информации о пользователе {user_id}: {e}")
        names.append((f"[ID: {user_id}]", None))
        
    return names
    