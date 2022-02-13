from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from data_base import sqlite_db


def start_inline_keyboard():
    button = InlineKeyboardButton(text='Новый список', callback_data='new_list')
    inline_keyboard = InlineKeyboardMarkup().add(button)
    return inline_keyboard


def get_reply_keyboard():
    buttons = [
        KeyboardButton('Все списки'),
        KeyboardButton('Новый список'),
        KeyboardButton('Помощь')
    ]
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(buttons[0], buttons[1]).add(buttons[2])
    return reply_keyboard


def get_inline_keyboard():
    buttons = [
        InlineKeyboardButton(text='Удалить список', callback_data='delete_list'),
        InlineKeyboardButton(text='Удалить задачи OFF', callback_data='delete_goals_on'),
    ]
    inline_keyboard = InlineKeyboardMarkup(row_width=3).add(*buttons)
    return inline_keyboard


def get_delete_keyboard():
    buttons = [
        InlineKeyboardButton(text='Удалить список', callback_data='delete_list'),
        InlineKeyboardButton(text='Удалить задачи ON', callback_data='delete_goals_off'),
    ]
    inline_keyboard = InlineKeyboardMarkup(row_width=3).add(*buttons)
    return inline_keyboard


def get_inline_show_keyboard():
    lists = sqlite_db.sq_select_all_lists()
    all_lists = ()
    for list_name in lists:
        all_lists += list_name
    buttons = [InlineKeyboardButton(text=list_name, callback_data='{}'.format(list_name)) for list_name in all_lists]
    lists_name_keyboard = InlineKeyboardMarkup().add(*buttons)
    return lists_name_keyboard
