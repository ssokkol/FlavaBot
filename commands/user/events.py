import keyboards
from db import BotDB
import main
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BotDB = BotDB("users.db")


async def send_events(chat_id):
    events = await BotDB.get_events()
    events = events.split()
    keyboard = []
    for i in events:
        name = await BotDB.get_event_name(i)
        name = name[3:-4]
        keyboard.append([InlineKeyboardButton(name, callback_data=f"eventn{i}")])
    keyboard.append([InlineKeyboardButton("⏪Назад⏪", callback_data="back")])
    await main.bot.send_message(chat_id, "Доступные мероприятия на данный момент",
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))


async def event_info(chat_id, event_id):
    name = await BotDB.get_event_name(event_id)
    name = name[3:-4]
    soldout = int(await BotDB.get_soldout(event_id))
    desc = str(await BotDB.get_desc(event_id))
    date = await BotDB.get_event_date(event_id)
    url = await BotDB.get_event_img(event_id)
    time = await BotDB.get_event_time(event_id)
    buy = InlineKeyboardButton(text="💳Купить билет💳", url=f"https://flava.qtickets.ru/event/{event_id}")
    event_buy_kb = InlineKeyboardMarkup().add(buy).add(keyboards.backe)
    if soldout == 0:
        await main.bot.send_photo(chat_id, photo=url, caption=
        f"<b>{name}</b>\n\n<b>Описание:</b>\n{desc}\n\n<b>Дата:</b> {date}\n<b>Время начала меропрития:</b> {time}",
                                  reply_markup=event_buy_kb, parse_mode=types.ParseMode.HTML)
    elif soldout == 1:
        await main.bot.send_photo(chat_id, photo=url, caption=
        f"<b>{name}</b>\n\n<b>Описание:</b>\n{desc}\n\n<b>Дата:</b> {date}\n<b>Время начала меропрития:</b> {time}",
                                  reply_markup=keyboards.event_soldout_kb, parse_mode=types.ParseMode.HTML)
