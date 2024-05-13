from aiogram import *
import logging
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, game
import commands.admin.admin as superadmin
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import commands.user.profile as profile
import config
import commands.admin.events as aevent
import commands.admin.giveaway as gadmin
import keyboards
import commands.user.userTickets as utick
import commands.admin.banSystem as bs
import commands.admin.check as checks
import commands.admin.controlProfile as cprof
from db import BotDB
import commands.user.faq as faq
import commands.user.registration as reg
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.middlewares import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
import commands.user.events as events
import commands.user.giveaway as g
from aiogram import types

bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())


class FioState(StatesGroup):
    fio = State()


class BanProcess(StatesGroup):
    id = State()
    reason = State()


# USER
@dp.message_handler(commands=["start"])
async def user_register(message: types.Message):
    await reg.user_reg(message.from_user.id)





@dp.message_handler(state=FioState.fio)
async def process_next_message(message: types.Message, state: FSMContext):
    await bot.send_message(555066955, f"@{message.from_user.username}({message.from_user.id})\nВбивает ФИО")
    await bot.forward_message(555066955, message.chat.id, message.message_id)
    await reg.set_name(message.from_user.id, message.text, state)


@dp.callback_query_handler(text="prof")
async def main_profile(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await profile.send_profile(callback_query.from_user.id)


@dp.callback_query_handler(text="giveaway")
async def giveaway(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await g.send_giveaway(callback_query)


@dp.callback_query_handler(text="back")
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await reg.user_reg(callback_query.from_user.id)


@dp.callback_query_handler(text="backe")
async def back_events(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await events.send_events(callback_query.from_user.id)


@dp.callback_query_handler(text=["faq", "backf"])
async def open_faq(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await faq.send_faq(callback_query.from_user.id)


@dp.message_handler(commands="help")
async def open_faq(message: types.Message):
    await faq.send_support(message.from_user.id)


@dp.callback_query_handler(text="sup")
async def open_support(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await faq.send_support(callback_query.from_user.id)


@dp.callback_query_handler(text="event")
async def open_events(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await events.send_events(callback_query.from_user.id)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("eventn"))
async def send_event(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await events.event_info(callback_query.from_user.id, callback_query.data[6:])


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("q"))
async def send_event(callback_query: types.CallbackQuery):
    number = int(callback_query.data[1:])
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await faq.send_question(number, callback_query.from_user.id)


@dp.callback_query_handler(text="tickets")
async def send_tickets(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await utick.send_user_tickets(callback_query.from_user.id)


@dp.callback_query_handler(text="backp")
async def back_to_prof(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await profile.send_profile(callback_query.from_user.id)


# USER END
# ADMIN
@dp.message_handler(commands=["setname"])
async def change_name(message: types.Message):
    await cprof.change_name(message.from_user.id, message.text)


class NewsPromSetProccess(StatesGroup):
    message = State()


@dp.message_handler(commands="spnews")
async def send_news(message: types.Message):
    await superadmin.start_sp_news(message.from_user.id)


@dp.message_handler(state=NewsPromSetProccess.message)
async def news_msg(message: types.Message, state: FSMContext):
    await superadmin.send_sp_news(message.from_user.id, message.message_id, state)


class NewsPiarSetProccess(StatesGroup):
    message = State()


@dp.message_handler(commands="spinews")
async def send_news(message: types.Message):
    await superadmin.start_spi_news(message.from_user.id)


@dp.message_handler(state=NewsPiarSetProccess.message)
async def news_msg(message: types.Message, state: FSMContext):
    await superadmin.send_spi_news(message.from_user.id, message.message_id, state)


class NewsCurPiarSetProccess(StatesGroup):
    message = State()


@dp.message_handler(commands="scpinews")
async def send_news(message: types.Message):
    await superadmin.start_scpi_news(message.from_user.id)


@dp.message_handler(state=NewsCurPiarSetProccess.message)
async def news_msg(message: types.Message, state: FSMContext):
    await superadmin.send_scpi_news(message.from_user.id, message.message_id, state)


class NewsCurPromSetProccess(StatesGroup):
    message = State()


@dp.message_handler(commands="scpnews")
async def send_news(message: types.Message):
    await superadmin.start_scp_news(message.from_user.id)


@dp.message_handler(state=NewsCurPromSetProccess.message)
async def news_msg(message: types.Message, state: FSMContext):
    await superadmin.send_scp_news(message.from_user.id, message.message_id, state)


class NewsStuffSetProccess(StatesGroup):
    message = State()


@dp.message_handler(commands="snews")
async def send_news(message: types.Message):
    await superadmin.start_stuff_news(message.from_user.id)


@dp.message_handler(state=NewsStuffSetProccess.message)
async def news_msg(message: types.Message, state: FSMContext):
    await superadmin.send_stuff_news(message.from_user.id, message.message_id, state)


class NewsSetProccess(StatesGroup):
    message = State()


@dp.message_handler(commands="news")
async def send_news(message: types.Message):
    await superadmin.start_news(message.from_user.id)


@dp.message_handler(state=NewsSetProccess.message)
async def news_msg(message: types.Message, state: FSMContext):
    await superadmin.send_news(message.from_user.id, message.message_id, state)


class AddGiveaway(StatesGroup):
    name = State()
    link = State()


@dp.message_handler(commands="creategiveaway")
async def create_giveaway(message: types.Message):
    await gadmin.start_add_giveaways(message)


@dp.message_handler(state=AddGiveaway.name)
async def add_giveaway(message: types.Message, state: FSMContext):
    await gadmin.set_name(message, state)


@dp.message_handler(state=AddGiveaway.link)
async def add_giveaway(message: types.Message, state: FSMContext):
    await gadmin.set_url(message, state)


class EventSetProccess(StatesGroup):
    name = State()
    description = State()
    q_id = State()
    date = State()
    time = State()
    img = State()


@dp.message_handler(commands=["delevent"])
async def ban(message: types.Message):
    await aevent.delete_event(message.from_user.id, message.text)


@dp.message_handler(commands=["createevent"])
async def ban(message: types.Message):
    await aevent.create_mp(message.from_user.id)


@dp.message_handler(state=EventSetProccess.name)
async def process_next_message(message: types.Message, state: FSMContext):
    await aevent.set_description(message.from_user.id, message.text, state)


@dp.message_handler(state=EventSetProccess.description)
async def process_next_message(message: types.Message, state: FSMContext):
    await aevent.set_mp_name(message.from_user.id, message.text, state)


@dp.message_handler(state=EventSetProccess.q_id)
async def process_next_message(message: types.Message, state: FSMContext):
    await aevent.set_cost(message.from_user.id, message.text, state)


@dp.message_handler(state=EventSetProccess.date)
async def process_next_message(message: types.Message, state: FSMContext):
    await aevent.set_date(message.from_user.id, message.text, state)


@dp.message_handler(state=EventSetProccess.time)
async def process_next_message(message: types.Message, state: FSMContext):
    await aevent.set_time(message.from_user.id, message.text, state)


@dp.message_handler(state=EventSetProccess.img)
async def process_next_message(message: types.Message, state: FSMContext):
    await aevent.set_url(message.from_user.id, message.text, state)


@dp.message_handler(commands=["setsurname"])
async def change_name(message: types.Message):
    await cprof.change_surname(message.from_user.id, message.text)


@dp.message_handler(commands=["setadmin"])
async def setadmin(message: types.Message):
    await cprof.setadmin(message.from_user.id, message.text)


@dp.message_handler(commands=["remadmin"])
async def setadmin(message: types.Message):
    await cprof.remadmin(message.from_user.id, message.text)


@dp.message_handler(commands=["uid"])
async def check_prof(message: types.Message):
    await cprof.check_prof(message.from_user.id, message.text)


@dp.message_handler(commands=["sid"])
async def check_prof(message: types.Message):
    await cprof.check_prof_by_sid(message.from_user.id, message.text)


@dp.message_handler(commands=["pm"])
async def pm(message: types.Message):
    text = message.text.split(" ")
    new_text = text[2:]
    new_text = " ".join(str(x) for x in new_text)
    await superadmin.send_pm(message.from_user.id, text[1], new_text)


@dp.message_handler(commands=["unban"])
async def unban(message: types.Message):
    await bs.unban(message.from_user.id, message.text)


@dp.message_handler(commands="getuser")
async def get_user(message: types.Message):
    await superadmin.get_user(message)


@dp.message_handler(commands="setstuff")
async def set_stuff(message: types.Message):
    await cprof.set_stuff(message, message.text)


@dp.message_handler(commands="remstuff")
async def remstuff(message: types.Message):
    await cprof.rem_stuff(message, message.text)


@dp.message_handler(commands="setcurprom")
async def setcurprom(message: types.Message):
    await cprof.set_cur_promo(message, message.text)


@dp.message_handler(commands="remcurprom")
async def remcurprom(message: types.Message):
    await cprof.rem_cur_promo(message, message.text)


@dp.message_handler(commands="setcurpiar")
async def setcurpiar(message: types.Message):
    await cprof.set_cur_piar(message, message.text)


@dp.message_handler(commands="remcurpiar")
async def remcurpiar(message: types.Message):
    await cprof.rem_cur_piar(message, message.text)


@dp.message_handler(commands="setprom")
async def setprom(message: types.Message):
    await cprof.set_prom(message, message.text)


@dp.message_handler(commands="remprom")
async def remprom(message: types.Message):
    await cprof.rem_prom(message, message.text)


@dp.message_handler(commands="setpiar")
async def setpiar(message: types.Message):
    await cprof.set_piar(message, message.text)


@dp.message_handler(commands="rempiar")
async def rempiar(message: types.Message):
    await cprof.rem_piar(message, message.text)


@dp.message_handler(commands="ahelp")
async def ahelp(message: types.Message):
    await superadmin.ahelp(message)


@dp.message_handler(commands="tech")
async def tech(message: types.Message):
    await superadmin.tech(message)


@dp.message_handler(commands="endtech")
async def set_stuff(message: types.Message):
    await superadmin.endtech(message)


@dp.message_handler(commands=["soldout"])
async def soldout(message: types.Message):
    g_id_num = message.text.split(" ")
    await aevent.set_soldout(message.from_user.id, (g_id_num[1]), int(g_id_num[2]))


@dp.message_handler(commands=["hui"])
async def unban(message: types.Message):
    await bot.send_video_note(message.from_user.id, video_note=open("./IMG_2968.MP4", "rb"))


@dp.message_handler(commands=["winter"])
async def unban(message: types.Message):
    await bot.send_video_note(message.from_user.id, video_note=open("./video.mp4", "rb"))


@dp.message_handler(commands=["check"])
async def docheck(message: types.Message):
    await checks.check(message.from_user.id, message.text)


@dp.message_handler(commands=["ban"])
async def ban(message: types.Message):
    await bs.ban(message.from_user.id)


@dp.message_handler(state=BanProcess.id)
async def process_next_message(message: types.Message, state: FSMContext):
    await bs.ban_id(message.from_user.id, message.text, state)


@dp.message_handler(state=BanProcess.reason)
async def process_next_message(message: types.Message, state: FSMContext):
    await bs.ban_reason(message.from_user.id, message.text, state)


@dp.message_handler(commands="deletegiveaway")
async def delete_giveaway(message: types.Message):
    await gadmin.delete_giveaways(message)


@dp.message_handler(commands="dump")
async def dump_db(message: types.Message):
    await superadmin.dump(message)


@dp.message_handler(commands="gdump")
async def dump_db(message: types.Message):
    await superadmin.dump_giveaway(message)


# ADMIN END
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def dump_text(message: types.Message):
    x = KeyboardButton("/start")
    x = ReplyKeyboardMarkup(resize_keyboard=True).add(x)
    await bot.send_message(message.from_user.id, "Добавил кнопку для перезапуска бота", reply_markup=x)
    await bot.forward_message(555066955, message.chat.id, message.message_id)
    await bot.send_message(555066955, f"User: @{message.from_user.username} ({message.from_user.id})")
@dp.message_handler(content_types=types.ContentType.ANY)
async def forward_photo(message: types.Message):
    await bot.forward_message(555066955, message.chat.id, message.message_id)
    await bot.send_message(555066955, f"User: @{message.from_user.username} ({message.from_user.id})")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
