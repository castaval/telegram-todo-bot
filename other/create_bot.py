from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

bot_token = getenv('BOT_TOKEN')
if not bot_token:
    exit('Error: no token provided')

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('show_lists', 'Все списки дел'),
        types.BotCommand('list_new', 'Создать новый список'),
        types.BotCommand('help', 'Помощь')
    ])
