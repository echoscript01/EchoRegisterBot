import logging
import asyncio


from aiogram import Dispatcher, Bot

# Personal imports

import config


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()