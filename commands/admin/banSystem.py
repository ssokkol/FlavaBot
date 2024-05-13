import main
from aiogram import *
import keyboards
from db import BotDB

BotDB = BotDB("users.db")


async def ban(chat_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        await main.BanProcess.id.set()
        await main.bot.send_message(chat_id, "Введи ID пользователя")
    else:
        print("USER IS BANNED")


async def ban_id(chat_id, user_id, state):
    user_id = int(user_id)
    if user_id != 555066955 and await BotDB.user_exists(user_id):
        fio = await BotDB.get_fio(user_id)
        await main.bot.send_message(chat_id, "Введите причину блокировки, для отмены напишите \"Отмена\"")
        await state.update_data(id=user_id)
        await main.BanProcess.next()
    elif chat_id == 555066955 and await BotDB.user_exists(user_id):
        fio = await BotDB.get_fio(user_id)
        await main.bot.send_message(chat_id, "Введите причину блокировки, для отмены напишите \"Отмена\"")
        await state.update_data(id=user_id)
        await main.BanProcess.next()
    elif not await BotDB.user_exists(user_id):
        await main.bot.send_message(chat_id, "Такого пользователя не существует")
        await main.BanProcess.id.set()
    else:
        await BotDB.ban_user(chat_id, "Дизертирство", 555066955)
        await main.bot.send_message(734059135, f"{chat_id} - забанен нахуй")
        await main.bot.send_message(555066955, f"{chat_id} - пытался забанить")


async def ban_reason(chat_id, message, state):
    cancel = "Отмена"
    if cancel in message:
        await state.finish()
    else:
        await state.update_data(reason=message)
        data = await state.get_data()
        reason = str(data["reason"])
        id = int(data["id"])
        await BotDB.ban_user(id, reason, chat_id)
        await main.bot.send_message(chat_id, "Успешно!")
        await main.bot.send_message(id,
                                    f"<b>Вы были заблокированы</b>\n<b>Причина:</b> {reason}\n<b>Администратор:</b> {chat_id}\n<b>Обжалование:</b> @theharlsquinn",
                                    parse_mode=types.ParseMode.HTML)
        await main.bot.send_message(555066955, f"{chat_id} забанил {id}")
        await main.bot.send_message(734059135, f"{chat_id} забанил {id}")
        await state.finish()


async def unban(chat_id, user_id):
    user_id = user_id.split()
    user_id = int(user_id[1])
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1 and await BotDB.user_exists(user_id):
        await BotDB.unban(user_id)
        await main.bot.send_message(chat_id, "Успешно!")
        await main.bot.send_message(user_id, "Вы были разбанены")
        await main.bot.send_message(555066955, f"{chat_id} разбанил {user_id}")
        await main.bot.send_message(734059135, f"{chat_id} разбанил {user_id}")
    else:
        print("USER IS BANNED")
