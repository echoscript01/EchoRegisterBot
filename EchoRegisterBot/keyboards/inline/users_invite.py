from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_invite_kb = [
    [
        InlineKeyboardButton(text="Принять", callback_data="accept"),
        InlineKeyboardButton(text="Отклонить", callback_data="decline")
    ]
]

inline_invite_add = InlineKeyboardMarkup(inline_keyboard=inline_invite_kb)