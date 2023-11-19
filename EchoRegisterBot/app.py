# Imports

from loader import Bot, Dispatcher, logging, asyncio, config, dp, bot


from handlers import on_startup_menu
from handlers.admins import accept_user, admin_panel



bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

async def main():
    """Start polling new updates"""
    
    dp.include_routers(
        on_startup_menu.router,
        accept_user.router,
        admin_panel.router
        )
    
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO) 
    asyncio.run(main())