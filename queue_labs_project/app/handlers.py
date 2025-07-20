from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboars as kb 
from app.validators import Validators
import app.database.requests as rq
from app.database.models import Student
from app.logging import log_event
from app.locals.memory import load_admins, save_admins
from app.auxiliary import get_user_info
# from config import ADMINS as admin_1

ADMINS = load_admins()

router = Router()

# HANDLE COMMAND START
@router.message(CommandStart())
async def cmd_start(message: Message):
    log_event(message, "/start")
    welcome_text = """
     <b>    Добро пожаловать в бота для очереди лаб!👋</b>
     
    Данный бот, как нетрудно догадаться, позволяет
    записаться в онлайн очередь для сдачи лабы.
    
    📌 <i>Основные команды:</i>
    1. Встать в очередь
    2. Показать текущую очередь
    3. Покинуть очередь
    
    Для дополнительных справок
    используйте команду <b>/help</b>

    Первый записавшийся сдаёт первым!🤓
    """
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=kb.action_choose)
    
    
@router.message(Command("help"))
async def cmd_help(message: Message):
    log_event(message)
    help_text = """
    <b>📚 Список доступных команд:</b>

    <b>Для всех пользователей:</b>
    /start - Начать работу с ботом
    /delete - Удалить несколько записей
    /find - Найти записи по параметру

    <b>Для администраторов:</b>
    /admin - Проверка на админа
    /admins - Список админов
    /add_admin- Добавить админа
    /del_admin - Удалить админа
    
     <b>Дополнительно:</b>
     /about - информация о создателе
     
    <i>Вы также можете использовать кнопки меню</i>
    """
  
    await message.answer(help_text, parse_mode="HTML")
    
    
    
    
    
# OBLIGATORY REGISTER FORM 
class RegStudent(StatesGroup):
    name_fio = State()
    lab_number = State()
    sub_group = State()
    github_link = State()
    
    
# OBLIGATORY LabNumber FORM   
class LabNumber(StatesGroup):
    lab_number = State()


class UserData(StatesGroup):
    search_param = State()
    user_credentials = State()
    
    
    
    
    
    
    
    # CANCEL IMPLEMENTATION
@router.message(F.text.startswith("Отмена"))
async def cancel(message: Message, state: FSMContext):
    log_event(message)
    await state.clear()
    await message.answer(
        "Действие отменено✅",
        )    
    return
    
    
@router.message(Command("about"))
async def about(message: Message, bot: Bot):
    log_event(message, "/about")
    sticker_id = "CAACAgIAAxkBAAIGVWh8LR9YcoPVjBgqQ1008Qub7c8GAALwZgACFJJoSg5uXuOo5IbFNgQ"
    
    about_text = """
    
📂 <b>Previewk</b>:
- Hello, I'm the <b>founder & developer</b> of this project.
- Username: @novac_jr

🔧 <b>Tech Stack</b>:
- Built with 🐍 Python using <b>Aiogram</b> framework
- Deployed on <b>Not yet</b> 
- Database: <b>SQLite/PostgreSQL</b>

💻 <b>My GitHub</b>: 
<a href="https://github.com/jegorix">github.com/jegorix</a>

📚 <b>Features</b>:
- Queue management system
- Admin controls
- Real-time updates

🚀 The bot is constantly evolving!
    """
    
    await message.answer(about_text, parse_mode="HTML", disable_web_page_preview=True)
    
    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker = sticker_id
    )


# @router.message(F.sticker)
# async def get_sticker_id(message: Message):
#     sticker_id = message.sticker.file_id
#     await message.answer(f"Sticker id: {sticker_id}")



# HANDLE COMMAND PUSH TO QUEUE
@router.message(F.text.startswith("Записаться"))
async def cmd_push(message: Message, state: FSMContext):
    log_event(message)
    await state.set_state(RegStudent.name_fio)
    await message.answer("Хорошо, начнем процесс добавления в очередь!\nВам придется ответить на несколько вопросов")
    # можно добавить ok or no buttons
    await message.answer("Введите ваше фио (Иванов Иван Иванович)")
    
    
@router.message(RegStudent.name_fio)
async def set_fio(message: Message, state: FSMContext):
    log_event(message)
    if not Validators.fio_validate(message.text): #validator
        await message.reply("Неверный формат ФИО, попробуйте еще раз!")
        return

    await state.update_data(name_fio=message.text)
    await state.set_state(RegStudent.lab_number)
    await message.answer("Введите номер лабораторной работы")
    
    
@router.message(RegStudent.lab_number)
async def set_lab_number(message: Message, state: FSMContext):
    log_event(message)
    number = Validators.lab_number_validate(message.text)
    if not number:
        await message.reply("Неверный номер лабораторной работы, введите чисто!")
        return
    
    await state.update_data(lab_number=number)
    await state.set_state(RegStudent.sub_group)
    await message.answer("Введите номер вашей подгруппы")
    
    
@router.message(RegStudent.sub_group)
async def set_subgroup(message: Message, state: FSMContext):
    log_event(message)
    sub_group_number = Validators.sub_group_validate(message.text)
    
    if not sub_group_number:
        await message.reply("Неверный номер подгруппы, введите 1 или 2!")
        return
    
    await state.update_data(sub_group=sub_group_number)
    await state.set_state(RegStudent.github_link)
    await message.answer("Отправьте ссылку с сайта github с вашим кодом")
    
    
    
@router.message(RegStudent.github_link)
async def get_github_link(message: Message, state: FSMContext):
    log_event(message)
    github_link = Validators.github_link_validate(message.text)
    if not github_link:
        await message.reply("Неверный формат ссылки, проверьте ее корректность")
        return
    
    await state.update_data(github_link=github_link)
    
    student_data = await state.get_data()
    
    student_text = f"""
     <b>    Проверка предоставленных данных</b>
     
    Пожалуйста еще раз проверьте корректность
    введенных вами данных, так как они будут
    записаны в электронную очередь.
    
    📌 <i>Данные пользователя {message.from_user.username}:</i>
    1. ФИО: {student_data['name_fio']}
    2. Лабораторная работа №{student_data['lab_number']}
    3. Подгруппа-{student_data['sub_group']}
    4. Ссылка на github:\n  {student_data['github_link']}

    Данные верны?
    """
    await message.answer(student_text, parse_mode="HTML", reply_markup=kb.approve_data, disable_web_page_preview=True)
    
    
    
    # INLINE YES APPROVEMENT -> ADD STUDENT TO THE DATABASE
@router.callback_query(F.data == "approve_yes")
async def approve_yes(callback: CallbackQuery, state: FSMContext):
    log_event(callback, "В очередь добавлен новый пользователь")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Загрузка данных в очередь...")
    student_data = await state.get_data()
    
    try:
        await rq.add_student(
            user_tg_id=callback.from_user.id,
            username=callback.from_user.username,
            name_fio=student_data['name_fio'],
            lab_number=student_data['lab_number'],
            sub_group=student_data['sub_group'],
            github_link=student_data['github_link']
        )

        await callback.message.answer("Вы успешно записались в очередь!🎉\n"
                                      "Ваше место в очереди можно посмотреть в разделе\n'Просмотр очереди👀'",
                                      reply_markup=kb.action_choose,
                                      parse_mode='HTML',
                                      disable_web_page_preview=True)
        
    
    except Exception as e:
        await callback.message.answer("Произошла ошибка при сохранении данных❌\n"
                                      "Попробуйте еще раз", reply_markup=kb.action_choose,
                                      parse_mode='HTML',
                                      disable_web_page_preview=True)
        
        print(f"\nОшибка при добавлении в БД: {e}\n")
        
    finally:
        await state.clear()
        
        
    
    #INLINE NO APPROVEMENT
@router.callback_query(F.data == "approve_no")
async def approve_no(callback: CallbackQuery, state: FSMContext):
    log_event(callback,"approve_no")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Отмена...")
    await state.clear()
    await callback.message.edit_text("Процесс записи отменен!\nЧтобы начать сначала нажмите на конпку\n'Записаться в очередь🔥'")
    
    
    
    
    
    
 # QUEUE SHOWING
@router.message(F.text.startswith("Просмотр"))
async def show_menu(message: Message):
    log_event(message)
    await message.answer("Выберите способ представления очереди", reply_markup=kb.show_queue_method)
    
    
    
async def viewing_message(callback: CallbackQuery | Message, students: list[Student], responce: list[str]) -> list[str]:
    await callback.answer("Загрузка очереди...")
    log_event(callback)
    if not students:
        await callback.message.answer("Очередь пуста!")
        return responce
    
    for idx, student in enumerate(students, start=1):
        time_str = student.created_at.strftime('%d.%m в %H:%M')
        responce.append(
            f"{idx}. {student.name_fio} - ({student.username})\n"
            f"Лабораторная работа №{student.lab_number}\n"
            f"Подгруппа-{student.sub_group}\n"
            f"Ссылка на github:\n{student.github_link}\n"
            f"Добавлен {time_str}\n"
        )
    
    return responce
    
    
    
@router.callback_query(F.data == "quick_show")
async def quick_show(callback: CallbackQuery):
    log_event(callback)
    students = await rq.get_students_sorted(sort_by_time=True)
    
    responce = ["<b>Текущая очередь отсортированная по времени добавления</b>\n"]

    updated_responce = await viewing_message(callback, students, responce)
    
    if updated_responce:
        await callback.message.answer("\n\n".join(updated_responce), parse_mode="HTML", disable_web_page_preview=True)



@router.callback_query(F.data.startswith("sub_group-"))
async def sub_group_show(callback: CallbackQuery):
    log_event(callback)
    group_number = int(callback.data.split("-")[1])
    students = await rq.get_students_sorted(sub_group=group_number)
    responce = [f"<b>Текущая очередь отсортированная по номеру подгруппы\n\nПодгруппа-{group_number}</b>\n"]
    updated_responce = await viewing_message(callback, students, responce)
    
    if updated_responce:
        await callback.message.answer("\n\n".join(updated_responce), parse_mode="HTML", disable_web_page_preview=True)


@router.callback_query(F.data == "lab_number_show")
async def lab_number_show(callback: CallbackQuery, state: FSMContext):
    log_event(callback)
    await callback.message.answer("Введите номер лабораторной работы")
    await state.set_state(LabNumber.lab_number)
    
    
@router.message(LabNumber.lab_number)
async def get_lab_number(message: Message, state: FSMContext):
    log_event(message)
    number = Validators.lab_number_validate(message.text)
    if not number:
        await message.reply("Неверный номер лабораторной работы, введите число!")
        return
    
    await state.clear()
    
    students = await rq.get_students_sorted(lab_number=number)
    responce = [f"<b>Текущая очередь отсортированная по номеру лабы\nЛаба №{number}</b>\n"]
    
    updated_responce = await viewing_message(message, students, responce)
    
    if updated_responce:
        await message.answer("\n\n".join(updated_responce), parse_mode="HTML", disable_web_page_preview=True)
    
    
    
    
    
     # HANDLE COMMAND FIND STUDENT
@router.message(Command("find"))
async def cmd_find_student(message: Message, state: FSMContext):
    log_event(message, "/find")
    await state.clear()
    await message.answer("Выберите ключевой параметр поиска студента", reply_markup=kb.find_student_method)


@router.callback_query(F.data.startswith("find_by-"))
async def handle_finding(callback: CallbackQuery, state: FSMContext):
    log_event(callback)
    await callback.answer("Обработка запроса...")
    param = callback.data.split('-')[1]
    await state.update_data(search_param=param)
    
    param = "фамилию" if param == "surname" else param
    await callback.message.answer(f"Введите {param} пользователя, которого вы хотите найти")
    await state.set_state(UserData.user_credentials)
        
    

@router.message(UserData.user_credentials)
async def get_user_credentials(message: Message, state: FSMContext):
    log_event(message)
    data = await state.get_data()
    param = data['search_param']
    search_value = message.text
    students = None

    
    if param == "id":
        id = Validators.lab_number_validate(message.text)
        if not id:
            await message.reply("Неверный формат telegram id. Попробуйте еще раз!")
            return
            
        students = await rq.get_student_id_or_username(user_tg_id=id)
    
    
    elif param == "username":
        students = await rq.get_student_id_or_username(username=search_value)
        
    elif param == "surname":
        param = "фамилии"
        students = await rq.get_student_id_or_username(surname=search_value)
        
    if not students:
        param = "фамилией" if param == "фамилии" else param
        await message.answer(f"Пользователь с {param}: {search_value} не найден!")
        await state.clear()
        return
        
    responce = [f"<b>Найдено {len(students)} записей для {param}: {search_value}</b>\n\n"]

    responce = await viewing_message(message, students, responce)
    
    if responce:
        await message.answer("\n".join(responce), parse_mode="HTML", disable_web_page_preview=True)

    await state.clear()
    
    
    
class HandleDelete(StatesGroup):
    user_data = State()
    lab = State()    
    is_delete_all = State()
    is_admin = State()
    
    
    
# DELETE STUDENT FROM QUEUE
@router.message(F.text.startswith("Удалиться"))
async def delete_from_queue(message: Message, state: FSMContext):
    log_event(message)
    
    current_user = await rq.get_student_id_or_username(user_tg_id=message.from_user.id)
    if not current_user:
        await message.answer("❌ Ваших записей нет в очереди!\nУ вас нет права удалять пользователей")
        await state.clear()
        return
    
    await state.clear()
    await state.update_data(current_user_id=current_user[0].user_tg_id)
    
    await message.answer("Выберите ключевой параметр удаления", reply_markup=kb.delete_student_method)
    
    
@router.callback_query(F.data.startswith("delete_by-"))
async def handle_deleting(callback: CallbackQuery, state: FSMContext):
    log_event(callback)
    await callback.answer("Обработка запроса...")
    param = callback.data.split('-')[1]
    await state.update_data(search_param=param)
    
    param = "фамилию" if param == "surname" else param
    await callback.message.answer(f"Введите {param} пользователя для удаления")
    await state.set_state(HandleDelete.user_data)
    
    
    
@router.message(HandleDelete.user_data)
async def handle_credentials(message: Message, state: FSMContext):
    log_event(message)
    data = await state.get_data()
    param = data["search_param"]
    value = message.text
    current_user_id = data.get("current_user_id")

    if param == "id":
        id = Validators.lab_number_validate(value)
        if not id:
            await message.reply("Неверный формат telegram id. Попробуйте еще раз!")
            return
        
        if int(value) != current_user_id:
            await message.answer("❌ Ваших записей нет в очереди!\nУ вас нет права удалять пользователей")
            await state.clear()
            return
        
        value = int(value)
        await state.update_data(user_credentials=value)
    
    else:
        await state.update_data(user_credentials=value)
        
    
    if data.get("is_delete_all", False):
        
        students = await rq.get_student_id_or_username(**{param: value})
        
        if not students:
            await message.answer("❌ Записи не найдены")
            await state.clear()
            return
        
        if any(s.user_tg_id != current_user_id for s in students):
            await message.answer("❌ Ваших записей нет в очереди!\nУ вас нет права удалять пользователей")
            await state.clear()
            return
        
        deleted_count = await rq.delete_student(data=value, delete_all=True, param=param)
        log_event(message, f"Удалено {deleted_count} записей из очереди")
        await state.clear()
        await message.answer(
        f"✅ Удалено записей: {deleted_count} по параметру {param}: {value}" if deleted_count > 0
        else "❌ Записи не найдены"
        ) 
        return 
    
        
    await state.set_state(HandleDelete.lab)
    await message.answer("Введите номер лабы удаляемого пользователя")
    
    
    
    
@router.message(HandleDelete.lab)
async def get_lab_num(message: Message, state: FSMContext):
    log_event(message)
    if not Validators.lab_number_validate(message.text):
        await message.reply("Неверный номер лабы. Попробуйте еще раз!")
        return
    
    data = await state.get_data()
    param = data["search_param"]
    delete_user_data = data["user_credentials"]
    lab_number = message.text
    
    is_admin = message.from_user.id in ADMINS
    
    
    current_user: list[Student] = await rq.get_student_id_or_username(user_tg_id=message.from_user.id)
    
    current_user_id: int | str = current_user[0].user_tg_id
    
    
    kwargs = {
        "lab_number": lab_number,
        param: delete_user_data
    }
    
    
    # if param == "id":
    #    kwargs["user_tg_id"] = delete_user_data
        
    # elif param == "username":
    #     kwargs["username"] = delete_user_data
        
    # elif param == "surname":
    #     kwargs["surname"] = delete_user_data
        
    
   
    
    
    students = await rq.get_student_id_or_username(**kwargs)
    
    if not is_admin:
        students = [student for student in students if student.user_tg_id == current_user_id]
        if not students:
            await message.answer("❌ Вы можете удалять только свои собственные записи")
            await state.clear()
            return
        
    if not students:
       await message.answer("❌ Записи не найдены")
       await state.clear()
       return
        
    
    responce = [f"<b>Найдено {len(students)} записей для {param}: {delete_user_data}\nЛаба №{lab_number}</b>\n\n"]
    responce = await viewing_message(message, students, responce)
    
    log_event(message, "Из очереди удален пользователь")
    
    if responce:
        await message.answer("\n".join(responce), parse_mode="HTML", disable_web_page_preview=True)
        
        
    
    
    
    if students:
        if param in ["id", "username"]:
            deleted_count = await rq.delete_student(**kwargs)
        else:
            deleted_count = await rq.delete_students_by_id(
                [s.user_tg_id for s in students],
                lab_number
            )
    else:
        deleted_count = 0
         
         
    response = (
        f"✅ Удалено записей: {deleted_count}" if deleted_count > 0
        else "❌ Записи не найдены"
    )     

    await message.answer(response)
    await state.clear()
    

    

# DELETE ALL RECORDS FROM USER
@router.message(Command("delete"))
async def cmd_delete(message: Message, state: FSMContext):
   log_event(message, "/delete")
   
   is_admin = message.from_user.id in ADMINS
   
   current_user = await rq.get_student_id_or_username(user_tg_id=message.from_user.id)
   if not current_user:
        await message.answer("❌ Ваших записей нет в очереди!\nУ вас нет права удалять пользователей")
        await state.clear()
        return
       
   
   await state.clear()
   await state.update_data(is_delete_all=True,
                           is_admin=is_admin)
   
   text = (
        "Выберите параметр для удаления ВСЕХ записей\n"
        "⚠️ Вы администратор!" if is_admin else
        "Вы можете удалять только свои записи"
    )
   
   await message.answer(text, reply_markup=kb.delete_student_method)

class AddAdmin(StatesGroup):
    admin_set = State()
    admin_reset = State()
    
    
    # ADMIN ADD AND REMOVE LOGIC
@router.message(Command("add_admin"))
async def add_admin(message: Message, state: FSMContext):
    log_event(message)
    is_admin = message.from_user.id
    
    if is_admin not in ADMINS:
        await message.answer("❌ У вас недостаточно прав для данной операции")
        return
    
    await message.answer("Введите ID пользователя, которого вы хотите сделать админом")
    await state.set_state(AddAdmin.admin_set)
    
    
@router.message(AddAdmin.admin_set)
async def admin_set(message: Message, state: FSMContext, bot: Bot):
    log_event(message)
    new_admin_id = Validators.lab_number_validate(message.text)
    
    if not new_admin_id:
        await message.relpy("Неверный формат ID!\nПопробуйте еще раз")
        return
        
    ADMINS.add(new_admin_id)
    save_admins(ADMINS)
    log_event(message, "ДОБАВЛЕН НОВЫЙ АДМИН")
    user_info = await get_user_info(bot, [new_admin_id])
    user_id, name, username = user_info[0]
    await message.answer(f"✅ Пользователь {name if name else new_admin_id}({username if username else new_admin_id}) добавлен в админы!")
    await state.clear()
    
        
        
        
        #DELETE ADMIN
@router.message(Command("del_admin"))
async def remove_admin(message: Message, bot: Bot):
    log_event(message)
    is_admin = message.from_user.id
    
    if is_admin not in ADMINS:
        await message.answer("❌ У вас недостаточно прав для данной операции")
        return
    
    await message.answer("Выберите пользователя, которого вы хотите лишить права быть админом", reply_markup=await kb.inline_admins(bot))
    


@router.callback_query(F.data.startswith("userid_"))
async def admin_reset(callback: CallbackQuery, bot: Bot):
    log_event(callback.message)
    rm_admin_id = int(callback.data.split("_")[1])
    print(rm_admin_id)
    await callback.answer("Удаление админа...")
   
    if rm_admin_id not in ADMINS:
        await callback.message.reply("❌ Данный пользователь не является админом!")
   
    ADMINS.remove(rm_admin_id)
    save_admins(ADMINS)
    log_event(callback.message, "УДАЛЕН АДМИН")
    user_info = await get_user_info(bot, [rm_admin_id])
    user_id, name, username = user_info[0]
    # добавить имя удаляемому админ
    await callback.message.answer(f"✅ Пользователь {name if name else user_id}({username if username else user_id}) удалён из админов.")
    
    
    
    
@router.message(Command("admins"))
async def show_admins(message: Message, bot: Bot):
    log_event(message)
    
    current_admins = load_admins()
    
    if not current_admins:
        await message.answer("Список админов пуст.")
        return
    
    admins_info = await get_user_info(bot, list(current_admins))
    if not admins_info:
        await message.answer("Не удалось получить информацию об админах.")
        return
    
    admins_list = "\n".join(
        f"• {firstname} (@{username}) - id: {user_id}" if username else f"• {firstname} - id: {user_id}"
        for user_id, firstname, username in admins_info
        )
    
    await message.answer(f"📌 Админы:\n{admins_list}")
    
    
    
@router.message(Command("admin"))
async def admins_approve(message: Message):
    log_event(message)
    current_admins = load_admins()
    if int(message.from_user.id) in current_admins:
        await message.answer("✅ Вы являетесь админом!")
        return
    await message.answer("❌ Вы не являетесь админом!")
    
    

    
    
    
# добавить кнопку отмена
# добавить информацию о существующих командах /add_admin и так далее
# добавить анимацию печатания текста через middleware


#     from datetime import datetime

# # Пример вывода в сообщении
# create_time = student.create_at.strftime("%d.%m.%Y %H:%M")
# await message.answer(f"Вы записались в очередь в {create_time} (МСК)")
    

    # await rq.add_student()
    
    