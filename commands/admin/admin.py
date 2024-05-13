from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db import BotDB
import main
from aiogram import types
import sqlite3
from xlsxwriter.workbook import Workbook

BotDB = BotDB("users.db")

ahelps = {
    "1": ("<b>/delevent [event_id] </b>- удалить мп\n<b>/createevent </b>- создать мп\n<b>/setname [uid] [name] "
          " </b>- смена имени пользователя\n<b>/setsurname [uid] [surname] </b>- изменить фамилию "
          "пользователю\n<b>/setadmin [uid] </b>- поставить на админа\n<b>/remadmin [uid] </b>- снять "
          "админку\n<b>/uid [uid] </b>- узнать информацию по юзер иду\n<b>/sid [sid] </b>- узнать информацию по "
          "статичному иду\n<b>/pm [uid] [message] </b>- личное сообщение пользователю\n<b>/unban [uid] </b>- "
          "разбан\n<b>/ban </b>- бан\n<b>/news </b>- рассылка всем пользователям\n<b>/hui </b>- кружок с "
          "сафиной\n<b>/snews </b>- новости для стафа\n<b>/spnews </b>- новости для промов\n<b>/scpnews </b>- "
          "новости для кураторов промов\n<b>/scpinew </b>- новости для кур пиаров\n<b>/spinew </b>- новости для "
          "пиаров\n<b>/setstuff [user_id] [0/1] </b>- добавить в стафф\n<b>/setcurprom [user_id] [0/1] </b>- "
          "добавить в кур промов\n<b>/setcurpiar [user_id] [0/1] </b>- добавить в кур пиаров\n<b>/setprom ["
          "user_id] [0/1] </b>- добавить в промов\n<b>/setpiar [user_id] [0/1] </b>- добавить в "
          "пиаров\n<b>/tech </b>- начало тех. Работ\n<b>/endtech </b>- конец работ\n<b>/dump </b>- запросить "
          "дамп базы данных\n<b>/winter </b>- сюрприз\n<b>/ahelp </b>-Список команда", 1),
    "2": ("<b>/spinews</b> - новости для пиаров\n/setpiar [user_id] [0/1] </b>- добавить в пиаров", 2),
    "3": (
    "<b>/spnews</b> - новости для промоутеров\n/setprom [user_id] [0/1] </b>- добавить в промоутеров(0 - Не промоутер, 1 - Промоутер)",
    3)
}


async def send_pm(chat_id, user_id, message):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1 and await BotDB.user_exists(
            user_id):
        await main.bot.send_message(chat_id, f"Успешно отправлен текст:\n{message}\n\nпользователю {user_id}")
        await main.bot.send_message(555066955,
                                    f"Успешно отправлен текст:\n{message}\n\nпользователю {user_id} by {chat_id}")
        await main.bot.send_message(user_id, message)
        if chat_id == 734059135:
            await main.bot.send_message(chat_id, "Пошел нахуй ебанько")
    elif int(await BotDB.is_admin(chat_id)) == 1 and not await BotDB.user_exists():
        await main.bot.send_message(chat_id, "нет такого пользователя ")
    elif not await BotDB.user_banned(chat_id) and int(
            await BotDB.is_cur_prom(chat_id)) == 1 and await BotDB.user_exists(
        user_id) and int(await BotDB.is_prom(user_id)):
        await main.bot.send_message(chat_id, f"Успешно отправлен текст:\n{message}\n\nпользователю {user_id}")
        await main.bot.send_message(555066955,
                                    f"Успешно отправлен текст:\n{message}\n\nпользователю {user_id} by {chat_id}")
        await main.bot.send_message(user_id, message)
        if chat_id == 734059135:
            await main.bot.send_message(chat_id, "Пошел нахуй ебанько")
    else:
        print("hui")


async def start_news(chat_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        await main.NewsSetProccess.message.set()
        await main.bot.send_message(chat_id,
                                    "Отправь мне любое сообщение а я перешлю его всем пользователям")

    else:
        print("HUI")


async def send_news(admin_id, admin_message_id, state):
    if not await BotDB.user_banned(admin_id) and int(await BotDB.is_admin(admin_id)) == 1:
        users = await BotDB.get_users()
        count = 0
        users = users.split(" ")
        for uid in users:
            try:
                await main.bot.copy_message(uid, admin_id, admin_message_id)
                count += 1
            except:
                pass
        await main.bot.send_message(admin_id, f"Рассылка успешна, ее получили {count} пользователей")
        if admin_id == 734059135:
            await main.bot.send_message(admin_id, "Пошел нахуй ебанько")
        await state.finish()
    else:
        print("hui")


async def get_user(message):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        user_id = message.text.split(" ")
        user_link = InlineKeyboardButton("user link", url=f"tg://user?id={user_id[1]}")
        kb = InlineKeyboardMarkup().add(user_link)
        await main.bot.send_message(message.from_user.id, "Ссылка на пользователя", reply_markup=kb)
    else:
        print("hui")


async def start_stuff_news(chat_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        await main.NewsStuffSetProccess.message.set()
        await main.bot.send_message(chat_id,
                                    "Отправь мне любое сообщение а я перешлю его всем сотрудникам")

    else:
        print("HUI")


async def send_stuff_news(admin_id, admin_message_id, state):
    if not await BotDB.user_banned(admin_id) and int(await BotDB.is_admin(admin_id)) == 1:
        users = await BotDB.get_stuff()
        count = 0
        users = users.split(" ")

        for uid in users:
            try:
                await main.bot.copy_message(uid, admin_id, admin_message_id)
                count += 1
            except:
                pass
        await main.bot.send_message(admin_id, f"Рассылка успешна, ее получили {count} сотрудников")
        if admin_id == 734059135:
            await main.bot.send_message(admin_id, "Пошел нахуй ебанько")
        await state.finish()
    else:
        print("hui")


async def start_scp_news(chat_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        await main.NewsCurPromSetProccess.message.set()
        await main.bot.send_message(chat_id,
                                    "Отправь мне любое сообщение а я перешлю его всем кураторам промов")

    else:
        print("HUI")


async def send_scp_news(admin_id, admin_message_id, state):
    if not await BotDB.user_banned(admin_id) and int(await BotDB.is_admin(admin_id)) == 1:
        users = await BotDB.get_cur_prom()
        count = 0
        users = users.split(" ")
        for uid in users:
            try:
                await main.bot.copy_message(uid, admin_id, admin_message_id)
                count += 1
            except:
                pass
        await main.bot.send_message(admin_id, f"Рассылка успешна, ее получили {count} кураторов промоуторов")
        if admin_id == 734059135:
            await main.bot.send_message(admin_id, "Пошел нахуй ебанько")
        await state.finish()
    else:
        print("hui")


async def start_scpi_news(chat_id):
    if not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1:
        await main.NewsCurPiarSetProccess.message.set()
        await main.bot.send_message(chat_id,
                                    "Отправь мне любое сообщение а я перешлю его всем кураторам пиаров")

    else:
        print("HUI")


async def send_scpi_news(admin_id, admin_message_id, state):
    if not await BotDB.user_banned(admin_id) and int(await BotDB.is_admin(admin_id)) == 1:
        users = await BotDB.get_cur_piar()
        count = 0
        users = users.split(" ")
        for uid in users:
            try:
                await main.bot.copy_message(uid, admin_id, admin_message_id)
                count += 1
            except:
                pass
        await main.bot.send_message(admin_id, f"Рассылка успешна, ее получили {count} кураторов пиаров")
        if admin_id == 734059135:
            await main.bot.send_message(admin_id, "Пошел нахуй ебанько")
        await state.finish()
    else:
        print("hui")


async def start_spi_news(chat_id):
    if (not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1) or (
            not await BotDB.user_banned(chat_id) and int(await BotDB.is_cur_piar(chat_id)) == 1):
        await main.NewsPiarSetProccess.message.set()
        await main.bot.send_message(chat_id,
                                    "Отправь мне любое сообщение а я перешлю его пиар отделу")

    else:
        print("HUI")


async def send_spi_news(admin_id, admin_message_id, state):
    if (not await BotDB.user_banned(admin_id) and int(await BotDB.is_admin(admin_id)) == 1) or (
            not await BotDB.user_banned(admin_id) and int(await BotDB.is_cur_piar(admin_id)) == 1):

        users = await BotDB.get_piar()
        count = 0
        users = users.split(" ")
        for uid in users:
            try:
                await main.bot.copy_message(uid, admin_id, admin_message_id)
                count += 1
            except:
                pass
        await main.bot.send_message(admin_id, f"Рассылка успешна, ее получили {count} пиаров")
        if admin_id == 734059135:
            await main.bot.send_message(admin_id, "Пошел нахуй ебанько")
        await state.finish()
    else:
        print("hui")


async def start_sp_news(chat_id):
    if (not await BotDB.user_banned(chat_id) and int(await BotDB.is_admin(chat_id)) == 1) or (
            not await BotDB.user_banned(chat_id) and int(await BotDB.is_cur_prom(chat_id)) == 1):
        await main.NewsPromSetProccess.message.set()
        await main.bot.send_message(chat_id,
                                    "Отправь мне любое сообщение а я перешлю его промоутерам")

    else:
        print("HUI")


async def send_sp_news(admin_id, admin_message_id, state):
    if (not await BotDB.user_banned(admin_id) and int(await BotDB.is_admin(admin_id)) == 1) or (
            not await BotDB.user_banned(admin_id) and int(await BotDB.is_cur_prom(admin_id)) == 1):

        users = await BotDB.get_prom()
        count = 0
        users = users.split(" ")
        for uid in users:
            try:
                await main.bot.copy_message(uid, admin_id, admin_message_id)
                count += 1
            except:
                pass
        await main.bot.send_message(admin_id, f"Рассылка успешна, ее получили {count} промоутеров")
        if admin_id == 734059135:
            await main.bot.send_message(admin_id, "Пошел нахуй ебанько")
        await state.finish()
    else:
        print("hui")


async def tech(message):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        users = await BotDB.get_users()
        count = 0
        users = users.split(" ")

        for uid in users:
            try:
                await main.bot.send_message(uid, "⚠️ПРОВОДЯТСЯ ТЕХ. РАБОТЫ⚠️\n🤖Бот не работает")
                count += 1
            except:
                pass
        await main.bot.send_message(message.from_user.id, f"Рассылка успешна, ее получили {count} пользователей")
        if message.from_user.id == 734059135:
            await main.bot.send_message(message.from_user.id, "Пошел нахуй ебанько")
    else:
        print("hui")


async def endtech(message):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        users = await BotDB.get_users()
        count = 0
        users = users.split(" ")
        for uid in users:
            try:
                await main.bot.send_message(uid, "✅ТЕХ. РАБОТЫ ЗАВЕРШЕНЫ️✅\n🤖Бот работает в штатном режиме")
                count += 1
            except:
                pass
        await main.bot.send_message(message.from_user.id, f"Рассылка успешна, ее получили {count} пользователей")
        if message.from_user.id == 734059135:
            await main.bot.send_message(message.from_user.id, "Пошел нахуй ебанько")
    else:
        print("hui")


async def ahelp(message):
    if not await BotDB.user_banned(message.from_user.id):
        group = int(await BotDB.get_group(message.from_user.id))
        if 0 < group <= 3:
            for answer, num in ahelps.values():
                if int(group) == int(num):
                    await main.bot.send_message(message.from_user.id, answer, parse_mode=types.ParseMode.HTML)
    else:
        print("a help hui")


async def dump(message):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        from xlsxwriter.workbook import Workbook
        workbook = Workbook("dump.xlsx")
        worksheet = workbook.add_worksheet()

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("select * from users")
        mysel = c.execute("select * from users ")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        workbook.close()
        await main.bot.send_document(message.from_user.id, document=open("dump.xlsx", "rb"), caption="Успешно")
        await main.bot.send_document(555066955, document=open("dump.xlsx", "rb"),
                                     caption=f"Запросил {message.from_user.id}")
    else:
        print("DUMP HUI")

async def dump_giveaway(message):
    if not await BotDB.user_banned(message.from_user.id) and int(await BotDB.is_admin(message.from_user.id)) == 1:
        from xlsxwriter.workbook import Workbook
        workbook = Workbook("dump.xlsx")
        worksheet = workbook.add_worksheet()

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("select * from giveaways")
        mysel = c.execute("select * from giveaways ")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        workbook.close()
        await main.bot.send_document(message.from_user.id, document=open("dump.xlsx", "rb"), caption="Успешно")
        await main.bot.send_document(555066955, document=open("dump.xlsx", "rb"),
                                     caption=f"Запросил {message.from_user.id}")
    else:
        print("DUMP HUI")