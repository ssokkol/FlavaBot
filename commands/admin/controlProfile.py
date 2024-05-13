import main
from aiogram import *
import keyboards
from db import BotDB

BotDB = BotDB("users.db")


async def change_name(chat_id, new_name):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:

        new_name = new_name.split()
        if len(new_name) != 3 or not new_name[1].isdigit():
            await main.bot.send_message(chat_id, "Использование /setname <id> <new_name>")
        elif new_name[1].isdigit() and await BotDB.user_exists(int(new_name[1])):
            await BotDB.change_name(int(new_name[1]), str(new_name[2]))
            await main.bot.send_message(chat_id, "Успешно!")
        else:
            await main.bot.send_message(chat_id, f"Не нашел пользователя с данным ID `<i>{new_name[1]}</i>`",
                                        parse_mode=types.ParseMode.HTML)

    else:
        print("USER IS BANNED")


async def change_surname(chat_id, new_name):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:

        new_name = new_name.split()
        if len(new_name) != 3 or not new_name[1].isdigit():
            await main.bot.send_message(chat_id, "Использование /setsurname <id> <new_surname>")
        elif new_name[1].isdigit() and await BotDB.user_exists(int(new_name[1])):
            await BotDB.change_surname(int(new_name[1]), str(new_name[2]))
            await main.bot.send_message(chat_id, "Успешно!")
        else:
            await main.bot.send_message(chat_id, f"Не нашел пользователя с данным ID `<i>{new_name[1]}</i>`",
                                        parse_mode=types.ParseMode.HTML)

    else:
        print("USER IS BANNED")


async def setadmin(chat_id, msg):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        msg = msg.split()
        if not await BotDB.user_exists(int(msg[1])):
            await main.bot.send_message(chat_id, f"Не нашел пользователя с данным ID `<i>{msg[1]}</i>`",
                                        parse_mode=types.ParseMode.HTML)
        else:
            await BotDB.change_admin_status(int(msg[1]), 1)
            await main.bot.send_message(chat_id, "Успешно!")
    else:
        print("USER IS BANNED")


async def remadmin(chat_id, msg):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        msg = msg.split()
        if int(msg[1]) != 555066955 and int(msg[1]) != 734059135:
            if not await BotDB.user_exists(int(msg[1])):
                await main.bot.send_message(chat_id, f"Не нашел пользователя с данным ID `<i>{msg[1]}</i>`",
                                            parse_mode=types.ParseMode.HTML)
            else:
                await BotDB.change_admin_status(int(msg[1]), 0)
                await main.bot.send_message(chat_id, "Успешно!")
        elif chat_id == 555066955:
            if not await BotDB.user_exists(int(msg[1])):
                await main.bot.send_message(chat_id, f"Не нашел пользователя с данным ID `<i>{msg[1]}</i>`",
                                            parse_mode=types.ParseMode.HTML)
            else:
                await BotDB.change_admin_status(int(msg[1]), 0)
                await main.bot.send_message(chat_id, "Успешно!")
        else:
            await BotDB.ban_user(chat_id, "Дизертирство", 555066955)
            await main.bot.send_message(734059135, f"{chat_id} - забанен нахуй")
            await main.bot.send_message(555066955, f"{chat_id} - пытался забрать админку")

    else:
        print("USER IS BANNED")


async def check_prof(chat_id, user_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        user_id = user_id.split()
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(int(user_id[1])):
                user_id = int(user_id[1])
                if not await BotDB.user_banned(user_id):
                    fio = await BotDB.get_fio(user_id)
                    id = await BotDB.get_id(user_id)
                    await main.bot.send_message(chat_id, f"<b>🆔:</b> {id}\n<b>👥:</b> {fio}\n",
                                                parse_mode=types.ParseMode.HTML)
                else:
                    reason = await BotDB.get_reason(user_id)
                    admin = await BotDB.get_admin(user_id)
                    fio = await BotDB.get_fio(user_id)
                    id = await BotDB.get_id(user_id)
                    await main.bot.send_message(chat_id, f"<b>🆔:</b> {id}\n<b>👥:</b> {fio}\n",
                                                parse_mode=types.ParseMode.HTML)
                    await main.bot.send_message(chat_id,
                                                f"Пользователь был заблокирован\nПричина: {reason}\nАдминистратор: {admin}\nПодробная информация: @theharlsquinn")
            else:
                await main.bot.send_message(chat_id, "Такого пользователя не существует!")
        else:
            await main.bot.send_message(chat_id, "Ты не ввел ID пользователя")
    else:
        print("HUI")


async def set_stuff(message, user_id):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):
                if 0 <= int(user_id[2]) <= 1:
                    await BotDB.set_stuff(user_id[1], 1)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь {user_id[1]} добавлен в стафф")
            else:
                await main.bot.send_message(message.from_user.id, "Такого пользователя не существует!")
        else:
            print("HUI")
    else:
        print("HUI")

async def rem_stuff(message, user_id):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):
                if 0 <= int(user_id[2]) <= 1:
                    await BotDB.set_stuff(user_id[1], 0)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь {user_id[1]} убран из стафа")
            else:
                await main.bot.send_message(message.from_user.id, "Такого пользователя не существует!")
        else:
            print("HUI")
    else:
        print("HUI")

async def set_cur_promo(message, user_id):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):
                    await BotDB.set_cur_prom(user_id[1],1)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь добавлен в кураторов промоутеров")
            else:
                await main.bot.send_message(message.from_user.id, "Такого пользователя не существует!")
        else:
            print("HUI")
    else:
        print("HUI")

async def rem_cur_promo(message, user_id):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):
                    await BotDB.set_cur_prom(user_id[1],0)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь убран из кураторов промоутеров")
            else:
                await main.bot.send_message(message.from_user.id, "Такого пользователя не существует!")
        else:
            print("HUI")
    else:
        print("HUI")
async def set_cur_piar(message, user_id):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):

                    await BotDB.set_cur_piar(user_id[1], 1)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь {user_id[1]} добавлен в кураторов пиаров")


        else:
            print("HUI")
    else:
        print("HUI")

async def rem_cur_piar(message, user_id):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):

                    await BotDB.set_cur_piar(user_id[1], 0)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь {user_id[1]} убран из кураторов пиаров")


        else:
            print("HUI")
    else:
        print("HUI")
async def set_piar(message, user_id):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):

                    await BotDB.set_is_piar(user_id[1],1)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь {user_id[1]} добавлен в пиаров")


        else:
            print("HUI")
    else:
        print("HUI")

async def rem_piar(message, user_id):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):

                    await BotDB.set_is_piar(user_id[1],0)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь {user_id[1]} убран из пиаров")


        else:
            print("HUI")
    else:
        print("HUI")
async def set_prom(message, user_id):
    if (not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1) or (
            not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_cur_prom(message.from_user.id)) == 1):
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):
                    await BotDB.set_is_prom(user_id[1], 1)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь {user_id[1]} добавлен в промоутеров")


            else:
                await main.bot.send_message(message.from_user.id, "Такого пользователя не существует!")
        else:
            print("HUI")
    else:
        print("HUI")

async def rem_prom(message, user_id):
    if (not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1) or (
            not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_cur_prom(message.from_user.id)) == 1):
        user_id = user_id.split(" ")
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.user_exists(user_id[1]):
                    await BotDB.set_is_prom(user_id[1], 0)
                    await main.bot.send_message(message.from_user.id,
                                                f"Пользователь {user_id[1]} убран из промоутеров")


            else:
                await main.bot.send_message(message.from_user.id, "Такого пользователя не существует!")
        else:
            print("HUI")
    else:
        print("HUI")
        
async def check_prof_by_sid(chat_id, user_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        user_id = user_id.split()
        if len(user_id) == 2 and user_id[1].isdigit():
            if await BotDB.sid_exists(int(user_id[1])):
                user_id = await BotDB.get_sid(int(user_id[1]))
                if not await BotDB.user_banned(user_id):
                    fio = await BotDB.get_fio(user_id)
                    id = await BotDB.get_id(user_id)
                    await main.bot.send_message(chat_id, f"<b>🆔:</b> {id}\n<b>👥:</b> {fio}",
                                                parse_mode=types.ParseMode.HTML)
                else:
                    reason = await BotDB.get_reason(user_id)
                    admin = await BotDB.get_admin(user_id)
                    fio = await BotDB.get_fio(user_id)
                    id = await BotDB.get_id(user_id)
                    await main.bot.send_message(chat_id, f"<b>🆔:</b> {id}\n<b>👥:</b> {fio}",
                                                parse_mode=types.ParseMode.HTML)
                    await main.bot.send_message(chat_id,
                                                f"Пользователь был заблокирован\nПричина: {reason}\nАдминистратор: {admin}\nПодробная информация: @theharlsquinn")
            else:
                await main.bot.send_message(chat_id, "Такого пользователя не существует!")
        else:
            await main.bot.send_message(chat_id, "Ты не ввел ID пользователя")
    else:
        print("HUI")
