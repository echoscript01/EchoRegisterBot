from aiogram import Router, types, F
from aiogram.filters.command import Command

from loader import bot
from utils.db_api import Users
from keyboards.default.admin_keyboard import admin_add

router = Router()

db = Users()

@router.message(F.text == "/admin")
async def admin_panel(message: types.Message):
    user_id = message.from_user.id
    
    if db.is_user_admin(user_id):
        await message.answer(text="Вы открыли админ панель", reply_markup=admin_add)
            
    else:
        pass
            
@router.message(F.text == "Разблокировать пользователя")
async def admin_panel(message: types.Message):
    user_id = message.from_user.id
    
    if db.is_user_admin(user_id):
        await message.answer(text=
                        "<b>Вы выбрали функцию разблокировки пользователя.</b>\n\n"\
                        "<b>Чтобы воспользоваться данной командой введите:</b>\n"\
                        "<code>/unblock</code> 123456\n\n<b>"\
                        "[Вместо цифр введите реальный ID пользователя.]</b>\n\n"\
                        "Если вы не знаете ID, воспользуйтесь командой: /find", parse_mode="HTML")
        
    else:
        pass
    
    
@router.message(Command("unblock"))
async def unblock_user(message: types.Message):
    user_id = message.from_user.id
    
    if db.is_user_admin(user_id):
        parts = message.text.split()  # Получаем аргументы после команды
        if len(parts) == 2:  # Проверяем, есть ли две части (команда и ID пользователя)
            try:
                user_to_unblock = int(parts[1])  # Получаем ID пользователя для разблокировки
                blocked_users = db.select_blocked_users()  # Получаем заблокированных пользователей
                if user_to_unblock in [user[0] for user in blocked_users]:  # Проверяем, есть ли ID пользователя среди заблокированных
                    db.delete_user(user_to_unblock)  # Удаляем пользователя из базы данных
                    await message.answer(f"Пользователь с ID {user_to_unblock} разблокирован.\n\nЕму нужно снова отправить заявку в бота.")
                    await bot.send_message(user_to_unblock, "Вы были разблокированы в боте.\n\nОтправьте заявку в бота повторно.")
                else:
                    await message.answer(f"Пользователь с ID {user_to_unblock} не заблокирован.")
            except ValueError:
                await message.answer("Неверный формат ID пользователя.")
        else:
            await message.answer("Используйте /unblock ID пользователя.")
    else:
        pass

@router.message(Command("find"))
async def find_blocked_users(message: types.Message):
    user_id = message.from_user.id
    
    if db.is_user_admin(user_id):
        blocked_users = db.select_blocked_users()
        if blocked_users:
            response = "Заблокированные пользователи:\n"
            for user_id, username in blocked_users:
                response += f"ID: {user_id}\nusername: @{username}\n\n"
            await message.answer(response)
        else:
            await message.answer("Нет заблокированных пользователей.")
    else:
        pass