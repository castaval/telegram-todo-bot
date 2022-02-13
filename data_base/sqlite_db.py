import sqlite3 as sq
from aiogram import types
from handlers.clb import in_list


def sql_start():
    global base, cur
    base = sq.connect('thoughts.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')


async def sq_select_list(call: types.CallbackQuery):
    number_goals = cur.execute('SELECT count(goal) FROM "{}"'.format(call.data)).fetchone()[0]
    if number_goals > 0:
        return cur.execute('SELECT goal FROM "{}"'.format(call.data)).fetchall()
    else:
        return None


def sq_select_all_lists():
    return cur.execute('SELECT tbl_name from sqlite_master WHERE rootpage !=9').fetchall()


async def sql_add_list(list_name):
    base.execute('CREATE TABLE IF NOT EXISTS "{}" (ID INTEGER PRIMARY KEY AUTOINCREMENT, goal TEXT)'.format(list_name))
    base.commit()


async def sql_add_goal(state, goal):
    async with state.proxy() as data:
        cur.execute('INSERT INTO "{}"(goal) VALUES (?)'.format(list(data.values())[0]), (goal,))
        base.commit()


async def sql_delete_list(state):
    async with state.proxy() as data:
        list_name = list(data.values())[0]
        cur.execute('DROP TABLE IF EXISTS "{}"'.format(list(data.values())[0]))
        base.commit()
    return list_name


async def sql_delete_goal(state, id):
    async with state.proxy() as data:
        cur.execute('DELETE FROM "{}" WHERE ID = "{}"'.format(list(data.values())[0], id))
        base.commit()


async def sql_goals_read():
    list_name = cur.execute('SELECT tbl_name FROM sqlite_master WHERE sql != "CREATE TABLE sqlite_sequence(name,seq)" '
                            'ORDER BY rootpage DESC LIMIT 1').fetchone()[0]
    number_goals = cur.execute('SELECT count(goal) FROM "{}"'.format(list_name)).fetchone()[0]
    if number_goals > 0:
        return cur.execute('SELECT goal FROM "{}"'.format(list_name)).fetchall()
    else:
        return None

