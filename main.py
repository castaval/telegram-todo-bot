from aiogram import executor
from data_base import sqlite_db
from other.create_bot import dp, set_default_commands
from handlers import logic, clb


async def start(_):
    print('Бот работает')
    await set_default_commands(dp)
    sqlite_db.sql_start()

clb.register_handlers_callback(dp)
logic.register_handlers_client(dp)

executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=start)
