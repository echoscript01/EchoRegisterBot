from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




admin_button = [
    [
        KeyboardButton(text="Разблокировать пользователя")
    ]
]

admin_add = ReplyKeyboardMarkup(keyboard=admin_button, resize_keyboard=True)