import main
import keyboards
from db import BotDB
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
BotDB = BotDB("users.db")


async def send_giveaway(message):
    events = await BotDB.get_giveaways()
    events = events.split()
    keyboard = []
    for i in events:
        name = await BotDB.get_giveaway_name(i)
        name = name[3:-4]
        link = await BotDB.get_giveaway_link(i)
        keyboard.append([InlineKeyboardButton(name, url = link)])
    keyboard.append([InlineKeyboardButton(text="⏪Назад⏪", callback_data="back")])
    await main.bot.send_message(message.from_user.id,"Тут вы увидете все наши действующие розыгрыши:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
