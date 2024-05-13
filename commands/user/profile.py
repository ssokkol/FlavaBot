from aiogram import *
import main
import cleaner
import keyboards

from db import BotDB

BotDB = BotDB("users.db")


async def send_profile(chat_id):
    if not await BotDB.user_banned(chat_id):
        fio = await BotDB.get_fio(chat_id)
        id = await BotDB.get_id(chat_id)
        await main.bot.send_message(chat_id, f"<b>🆔:</b> {id}\n<b>👥:</b> {fio}",
                                    parse_mode=types.ParseMode.HTML, reply_markup=keyboards.prof_kb)
    else:
        reason = await BotDB.get_reason(chat_id)
        admin = await BotDB.get_admin(chat_id)
        await main.bot.send_message(chat_id,
                                    f"Вы были заблокированы\nПричина: {reason}\nАдминистратор: {admin}\nОбжалование: @theharlsquinn")
