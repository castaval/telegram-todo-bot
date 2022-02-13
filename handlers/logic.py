from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from data_base import sqlite_db
from other.create_bot import bot
from keyboards.kb import get_reply_keyboard, get_inline_keyboard, start_inline_keyboard, get_inline_show_keyboard
from handlers.clb import InlineFSM
from aiogram.dispatcher.filters import Text

global list_n


async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, """Привет!\nРад тебя здесь видеть.
Я помогу тебе упорядочить твои повседневные задачи.\nНажми на кнопку снизу, чтобы создать свой первый список задач!""",
                           reply_markup=start_inline_keyboard())


async def stop(message: types.Message, state: FSMContext):
    goals = await sqlite_db.sql_goals_read()
    if goals is None:
        async with state.proxy() as data:
            message_goal = """{}

{} """.format(list(data.values())[0], 'Список пуст')
        await bot.send_message(message.from_user.id, message_goal, reply_markup=get_inline_keyboard())
    else:
        all_goals = ()
        for goal in goals:
            all_goals += goal
        async with state.proxy() as data:
            message_goal = """{}

{}""".format(list(data.values())[0], '\n'.join(all_goals))
        await bot.send_message(message.from_user.id, message_goal, reply_markup=get_inline_keyboard())
    await InlineFSM.new_goal.set()


async def creating_of_new_list(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['list'] = message.text
    await sqlite_db.sql_add_list(message.text)
    await bot.send_message(message.from_user.id, 'Лист создан\nТеперь отправляй мне пункты списка по одному за '
                                                 'сообщение.', reply_markup=get_reply_keyboard())
    await InlineFSM.new_goal.set()


async def creating_of_new_goal(message: types.Message, state: FSMContext):

    await sqlite_db.sql_add_goal(state, message.text)
    await bot.send_message(message.from_user.id, 'Задача добавлена в список')


async def delete_goal(message: types.Message, state: FSMContext):
    await sqlite_db.sql_delete_goal(state, message.text)
    await message.delete()


async def show_lists(message: types.Message):
    await bot.send_message(message.from_user.id, 'Все списки', reply_markup=get_inline_show_keyboard())
    await InlineFSM.show_goals.set()


async def new_list(message: types.Message):
    await bot.send_message(message.from_user.id, 'Отлично! Теперь введите название списка!')
    await InlineFSM.new_list.set()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'], state='*')
    dp.register_message_handler(show_lists, Text(equals='Все списки'), state='*')
    dp.register_message_handler(new_list, Text(equals='Новый список'), state='*')
    dp.register_message_handler(stop, commands=['goal_stop'], state=InlineFSM.new_goal)
    dp.register_message_handler(creating_of_new_list, content_types=["text"], state=InlineFSM.new_list)
    dp.register_message_handler(creating_of_new_goal, content_types=['text'], state=InlineFSM.new_goal)
