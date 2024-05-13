import keyboards
from db import BotDB
import main
from aiogram import types

BotDB = BotDB("users.db")


async def send_user_tickets(chat_id):
    if not await BotDB.user_banned(chat_id):
        ticket_info = await BotDB.get_user_tickets(chat_id)
        tickets = []
        for i in ticket_info:
            event_id = int(await BotDB.get_eid_by_id(i))
            name = await BotDB.get_event_name(event_id)
            tickets.append(f"<b>Мероприятие:</b> {name}\n<b>Номер билета:</b> {i}\n\n")
        tickets = "".join(tickets)
        await main.bot.send_message(chat_id, f"<b>Ваши билеты:</b>\n\n{tickets}", reply_markup=keyboards.backp_kb,
                                    parse_mode=types.ParseMode.HTML)
    else:
        reason = await BotDB.get_reason(chat_id)
        admin = await BotDB.get_admin(chat_id)
        await main.bot.send_message(chat_id,
                                    f"Вы были заблокированы\nПричина: {reason}\nАдминистратор: {admin}\nОбжалование: @theharlsquinn")
