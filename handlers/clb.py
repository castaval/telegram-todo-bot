from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db
from keyboards.kb import get_inline_keyboard, get_delete_keyboard
from other.create_bot import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext


class InlineFSM(StatesGroup):
    new_list = State()
    new_goal = State()
    show_goals = State()
    new_goal_in_list = State()
    delete_goal = State()


async def new_list(call: types.CallbackQuery):
    await call.message.answer('Отлично! Теперь введите название списка!')
    await InlineFSM.new_list.set()
    await call.answer()


async def delete_lists(call: types.CallbackQuery, state: FSMContext):
    name_list = await sqlite_db.sql_delete_list(state)
    await call.message.answer('Список {} удален'.format(name_list))
    await call.answer()


async def delete_goals_on(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(call.message.text, reply_markup=get_delete_keyboard())
    await InlineFSM.delete_goal.set()
    await call.answer()


async def delete_goals_off(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(call.message.text, reply_markup=get_inline_keyboard())
    await InlineFSM.new_goal.set()
    await call.answer()


async def in_list(call: types.CallbackQuery, state: FSMContext):
    goals = await sqlite_db.sq_select_list(call)
    async with state.proxy() as data:
        data['list'] = call.data
    if goals is None:
        message_goal = """{}

{} """.format(call.data, 'Список пуст')
        await call.message.answer(message_goal, reply_markup=get_inline_keyboard())
    else:
        all_goals = ()
        for goal in goals:
            all_goals += goal
        message_goal = """{}
        
{}""".format(call.data, '\n'.join(all_goals))
        await call.message.answer(message_goal, reply_markup=get_inline_keyboard())
    await InlineFSM.new_goal_in_list.set()
    await call.answer()


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(new_list, text='new_list', state='*')
    dp.register_callback_query_handler(delete_lists, text='delete_list', state=InlineFSM.new_goal_in_list)
    dp.register_callback_query_handler(delete_goals_on, text='delete_goals_on', state=InlineFSM.new_goal_in_list)
    dp.register_callback_query_handler(delete_goals_off, text='delete_goals_off', state=InlineFSM.delete_goal)
    dp.register_callback_query_handler(in_list, state=InlineFSM.show_goals)
