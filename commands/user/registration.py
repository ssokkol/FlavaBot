import db
import main
from keyboards import main_kb
from aiogram import *
from db import BotDB

BotDB = BotDB("users.db")


async def user_reg(chat_id ):
    if not await BotDB.user_banned(chat_id):
        if not await BotDB.user_exists(chat_id):
            await BotDB.add_user(chat_id)
            await main.bot.send_message(chat_id,
                                        "Привет! Отправь мне свое Имя и Фамилию через пробел.\nПример: Иван Иванов")
            await main.FioState.fio.set()
        else:
            await main.bot.send_message(chat_id, "Добро пожаловать в главное меню!", reply_markup=main_kb)
    else:
        reason = await BotDB.get_reason(chat_id)
        admin = await BotDB.get_admin(chat_id)
        await main.bot.send_message(chat_id,
                                    f"<b>Вы были заблокированы</b>\n<b>Причина:</b> {reason}\n<b>Администратор:</b> {admin}\n<b>Обжалование:</b> @theharlsquinn",
                                    parse_mode=types.ParseMode.HTML)


async def set_name(chat_id, message, state):
    if not await BotDB.user_banned(chat_id):
        msg = message
        msg_array = msg.split()
        if len(msg_array) != 2:
            await main.bot.send_message(chat_id, "Вам нужно указать Имя и Фамилию через пробел")
            await main.FioState.fio.set()
        else:
            await main.bot.send_message(chat_id,
                                        f"Привет {msg_array[0]}!\nЕсли допустил ошибку в имени или фамилии напиши /help")
            await BotDB.add_fio(chat_id, msg_array[0], msg_array[1])
            await main.bot.send_message(chat_id, "Добро пожаловать в главное меню!", reply_markup=main_kb)
            await state.finish()
    else:
        reason = await BotDB.get_reason(chat_id)
        admin = await BotDB.get_admin(chat_id)
        await main.bot.send_message(chat_id,
                                    f"Вы были заблокированы\nПричина: {reason}\nАдминистратор: {admin}\nОбжалование: @theharlsquinn")
