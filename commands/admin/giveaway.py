import main
import keyboards
from db import BotDB
from aiogram import types

BotDB = BotDB("users.db")


async def delete_giveaways(message):
    text = str(message.text)
    text = text.split(" ")
    if len(text) == 2 and not await BotDB.user_banned(message.from_user.id) and int(
            await BotDB.is_admin(message.from_user.id)) == 1 and text[1].isdigit():
        if not await BotDB.giveaway_exist(int(text[1])):
            await main.bot.send_message(message.from_user.id, "Такого розыгрыша не существует")
        else:
            await BotDB.delete_giveaway(int(text[1]))
            await main.bot.send_message(message.from_user.id, "Успешно")
    else:
        print("Error delete_giveaways")


async def start_add_giveaways(message):
    if not await BotDB.user_banned(message.from_user.id) and int(
            await BotDB.is_admin(message.from_user.id)) == 1:
        await main.AddGiveaway.name.set()
        await main.bot.send_message(message.from_user.id, "Отправь мне название розыгрыша")


async def set_name(message, state):
    await state.update_data(name=message.text)
    await main.bot.send_message(message.from_user.id, "Отправь ссылку на розыгрыш")
    await main.AddGiveaway.link.set()


async def set_url(message, state):
    await state.update_data(url=message.text)
    data = await state.get_data()
    name = str(data["name"])
    link = str(message.text)
    await BotDB.add_giveaway(name, link)
    await main.bot.send_message(message.from_user.id, "Успешно")
    await state.finish()
