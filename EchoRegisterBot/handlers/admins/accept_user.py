from aiogram import Router, types

from loader import bot
from utils.db_api import Users
from keyboards.inline.users_links import inline_users_links_add


router = Router()

db = Users()

@router.callback_query()
async def accept_user_to_bot(callback: types.CallbackQuery):
    
    if db.get_admin_user_ids():
        if callback.data == "accept":

            user_to_accept = db.select_user_state()
            for user_id in user_to_accept:
                db.update_user_state_accept()
                await bot.send_message(user_id[0], text="<b>Поздравляю! Ваша заявка была рассмотрена и вы были приняты.\n\nНиже находятся полезные ссылки</b>",reply_markup=inline_users_links_add, parse_mode="HTML")

        else:
            user_to_accept = db.select_user_state()
            for user_id in user_to_accept:
                db.update_user_state_decline()
                await bot.send_message(user_id[0], text="Извините, ваша заявка была отклонена и вы были забанены.")
    else:
        pass
