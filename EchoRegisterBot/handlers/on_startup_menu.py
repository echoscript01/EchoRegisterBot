
import logging

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from app import bot
from utils.db_api import Users
from keyboards.inline.users_invite import inline_invite_add
from keyboards.inline.users_links import inline_users_links_add

db = Users()

router = Router()



class RegisterUsers(StatesGroup):
    first_question = State()
    second_question = State()
    third_question = State()
    


@router.message(Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    username = message.from_user.username    
    
    if username is not None:
        if not db.user_exists(user_id):
            await bot.send_message(user_id, text="<b>Добро пожаловать.\n\nДля того чтобы мы могли принять вас в бота, ответьте на пару вопросов</b>", parse_mode="HTML")
            await bot.send_message(user_id, text="1. Сколько времени в день вы готовы уделять на работу?")
            await state.set_state(RegisterUsers.first_question)
            
    if username is not None:
        if db.user_exists(user_id):
            await bot.send_message(user_id, text="<b>Вы уже зарегистрированы в боте, полезные ссылки ниже</b>", reply_markup=inline_users_links_add, parse_mode="HTML")
    else:
        await bot.send_message(user_id, text="У вас не установлен <b>username</b>(имя пользователя)\n\nУстановите его и напишите /start", parse_mode="HTML")
        
        
        
@router.message(RegisterUsers.first_question)
async def answer_first_question(message: types.Message, state: FSMContext):
    # Сохраняем ответ пользователя и переключаемся на следующий вопрос
    answer = message.text
    await state.update_data(first_question=answer)
    await message.answer("2. Почему выбрали именно нашу команду?")
    await state.set_state(RegisterUsers.second_question)
    
    
    
# Аналогичные обработчики для остальных вопросов
@router.message(RegisterUsers.second_question)
async def answer_second_question(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(second_question=answer)
    await message.answer("3. В каких тимах раньше состояли? Какие были профиты")
    await state.set_state(RegisterUsers.third_question)



@router.message(RegisterUsers.third_question)
async def answer_third_question(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    admin_ids = db.get_admin_user_ids()  # Получаем все user_id администраторов
    username = message.from_user.username
    await message.answer("Ваша заявка была успешно отправлена, ожидайте решения администраторов.")
    context_data = await state.get_data()
    answer = message.text

    first_question = context_data.get('first_question', '')  # Если значение не найдено, установим пустую строку
    second_question = context_data.get('second_question', '')  # Аналогично
    await state.update_data(third_question=answer)
    third_question = answer

    db.add_user(user_id, username, accept=3)  # Добавляем пользователя в базу данных с accept=3

    user_data = (f"<b>Пришла новая заявка</b>\n\n" \
                f"<b>ID:</b> <code>{user_id}</code>\n" \
                f"<b>username:</b> @{username}\n\n" \
                f"<b>Первый ответ:</b> {first_question}\n" \
                f"<b>Второй ответ:</b> {second_question}\n" \
                f"<b>Третий ответ:</b> {third_question}")

    for admin_id in admin_ids:
        if admin_id:
            await bot.send_message(admin_id, user_data, reply_markup=inline_invite_add, parse_mode="HTML")
        else:
            print("Ошибка: admin_id не найден.")

    await state.clear()