from db import BotDB
import main
from aiogram import types

BotDB = BotDB("users.db")


async def check(chat_id, ticket_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        ticket_id = ticket_id.split()
        if len(ticket_id) == 2 and ticket_id[1].isdigit():
            ticket_id = int(ticket_id[1])
            if await BotDB.ticket_exists(ticket_id):
                user_id = int(await BotDB.get_uid_by_id(ticket_id))
                event_id = int(await BotDB.get_eid_by_id(ticket_id))
                fio = await BotDB.get_fio(user_id)
                event_name = await BotDB.get_event_name(event_id)
                await main.bot.send_message(chat_id,
                                            f"<b>{event_name}</b>\n\n🆔: {user_id}\n<b>👥:</b> {fio}\n<b>ID мероприятия:</b> {event_id}",
                                            parse_mode=types.ParseMode.HTML)
            else:
                await main.bot.send_message(chat_id, "Такого билета не существует либо ввели его не правильно")

        else:
            await main.bot.send_message(chat_id, "Вы не ввели номер билета")
    else:
        print("HUI")
