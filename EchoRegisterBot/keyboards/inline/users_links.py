from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_users_links = [
    [
        InlineKeyboardButton(text="Чат 💬", url="https://t.me/echoscript"),
        InlineKeyboardButton(text="Выплаты 💰", url="https://t.me/echoscript")
    ]
]

inline_users_links_add = InlineKeyboardMarkup(inline_keyboard=inline_users_links)