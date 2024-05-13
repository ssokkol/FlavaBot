import datetime

import keyboards
from db import BotDB
import main
from aiogram import types

BotDB = BotDB("users.db")


async def create_mp(chat_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        await main.EventSetProccess.name.set()
        await main.bot.send_message(chat_id,
                                    "Добро пожаловать в создание мероприятия!\nВведи его название(БЕЗ ЭМОДЗИ И ЗНАКОВ ПРЕПИНАНИЯ):")
    else:
        print("HUI")


async def set_description(chat_id, name, state):
    await main.bot.send_message(chat_id, "Введи описание мероприятия")
    await state.update_data(name=name)
    await main.EventSetProccess.next()


async def set_mp_name(chat_id, name, state):
    await main.bot.send_message(chat_id, "Так и запишу!\nВведи ID мероприятия с qtickets.com")
    await state.update_data(description=name)
    await main.EventSetProccess.next()


async def set_cost(chat_id, count, state):
    if not count.isdigit():
        await main.bot.send_message(chat_id, "Не число, попробуй еще раз!")
        await main.EventSetProccess.q_id.set()
    else:
        await main.bot.send_message(chat_id, "Введи дату(ДД ММ ГГГГ)")
        await state.update_data(q_id=int(count))
        await main.EventSetProccess.next()


async def is_valid_date(date_string):
    try:
        date = datetime.datetime.strptime(date_string, "%d %m %Y")
        return True
    except ValueError:
        return False


async def set_date(chat_id, date, state):
    array = date.split()
    if len(array) == 3:
        date_str = array[0] + " " + array[1] + " " + array[2]
        if await is_valid_date(date_str):
            today = datetime.datetime.now()
            date_str = datetime.datetime.strptime(date_str, "%d %m %Y")
            if today < date_str:
                day = str(int(array[0]))
                month = str(int(array[1]))
                if 0 <= int(array[0]) <= 9:
                    day = "0" + str(int(array[0]))
                if 0 <= int(array[1]) <= 9:
                    month = "0" + str(int(array[1]))
                date = day + " " + month + " " + array[2]
                await main.bot.send_message(chat_id, "Введи время(ЧЧ ММ)")
                await state.update_data(date=date)
                await main.EventSetProccess.next()
            else:
                await main.bot.send_message(chat_id, "Дата не может раньше текущей")
                await main.EventSetProccess.date.set()
        else:
            await main.bot.send_message(chat_id, "Попробуйте еще раз")
            await main.EventSetProccess.date.set()

    else:
        await main.bot.send_message(chat_id, "Попробуй еще раз!")
        await main.EventSetProccess.date.set()


async def set_time(chat_id, time, state):
    array = time.split()
    if len(array) == 2:
        if int(array[0]) <= 23 and int(array[1]) <= 59:
            await main.bot.send_message(chat_id, "Отправь ссылку на картинку для мероприятия")
            await state.update_data(time=time)
            await main.EventSetProccess.img.set()
        else:
            await main.bot.send_message(chat_id, "Попробуй еще раз!")
            await main.EventSetProccess.time.set()
    else:
        await main.bot.send_message(chat_id, "Попробуй еще раз!")
        await main.EventSetProccess.time.set()


async def set_url(chat_id, url, state):
    await state.update_data(img=url)
    data = await state.get_data()
    eventname = str(data["name"])
    desc = str(data["description"])
    q_id = int(data["q_id"])
    date = str(data["date"]).split()
    time = str(data["time"]).split()
    img = str(data["img"])
    await BotDB.add_event(eventname, desc, img, q_id, date[0], date[1], date[2], time[0], time[1])
    await main.bot.send_message(chat_id,
                                f"Успешно создано мероприятие \"{eventname}\"\n\nОписание:\n{desc}\n\nID: {q_id}\n\nДата и время(закрытия продаж): {date[0]}.{date[1]}.{date[2]} {time[0]}:{time[1]}")
    await state.finish()


async def get_by_id(chat_id, event_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        event_id = event_id.split()
        if len(event_id) != 2:
            await main.bot.send_message(chat_id, "Использование /getevent <id>")
        else:
            event_id = int(event_id[1])
            name = await BotDB.get_event_name(event_id)
            tickets = await BotDB.get_event_tickets(event_id)
            soldout = int(await BotDB.get_soldout(event_id))
            date = await BotDB.get_event_date(event_id)
            url = await BotDB.get_event_img(event_id)
            time = await BotDB.get_event_time(event_id)
            await main.bot.send_photo(chat_id, photo=url, caption=
            f"<b>{name}</b>\n\n<b>Доступно билетов:</b> {tickets}\n<b>Дата:</b> {date}\n<b>Время:</b> {time}",
                                      parse_mode=types.ParseMode.HTML)
    else:
        print("HUI")


async def delete_event(chat_id, event_id):
    event_id = event_id.split()
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1 and len(
            event_id) == 2 and await BotDB.event_exists(
            int(event_id[1])):
        event_id = int(event_id[1])
        await BotDB.delevent(event_id)
        await main.bot.send_message(chat_id, "Успешно!")

    else:
        print("HUI")


async def set_soldout(chat_id, g_id, new_num):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        if not await BotDB.event_exists(g_id):
            await main.bot.send_message(chat_id, "Нет такого мероприятия ебанько")
        elif await BotDB.event_exists(g_id):
            if new_num == 1:
                await BotDB.change_soldout(g_id, new_num)
                await main.bot.send_message(chat_id, "Установлено значение 1 - все билеты проданы")
            elif new_num == 0:
                await BotDB.change_soldout(g_id, new_num)
                await main.bot.send_message(chat_id, "Установлено значение 0 - билеты еще есть")
            else:
                await main.bot.send_message(chat_id, "Ты просто ебанько нет слов блядь")
    else:
        print(chat_id)
