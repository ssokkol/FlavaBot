import main
import keyboards
from db import BotDB
from aiogram import types

BotDB = BotDB("users.db")

questions = {
    "1": ("Где пройдет вечеринка?",
          "Мы будем ждать тебя в клубе SMENA по адресу Товарищеский пер., 4, стр. 5, в нескольких минутах ходьбы от "
          "метро Марксистская.",
          1),
    "2": ("Когда и во сколько начнется мероприятие?",
          "Новогодняя вечеринка состоится 22 декабря в 23:00 и продолжится до самого утра - 5:00.", 2),
    "3": ("Можно ли пригласить с собой друга?", "Даже нужно, ведь так веселее!", 3),
    "4": ("Будут ли на вечеринке напитки?",
          "В распоряжении гостей будет бар с разнообразными коктейлями, среди которых каждый гость точно сможет найти "
          "что-то свое.",
          4),
    "5": ("Есть ли дресс-код?",
          "Новый год - яркий и фееричный, но одновременно с этим и уютный праздник, поэтому выбирай стиль, "
          "который откликается именно тебе - строгого дресс-кода у нас нет. ",
          5),
    "6": ("Какая будет программа?",
          "На вечеринке ты сможешь насладиться праздничной атмосферой, сделать кадры к себе в Сторис и Телеграм в "
          "яркой и трендовой фотозоне, потанцевать под зажигательные DJ-сеты и не только…Полностью раскрывать секреты "
          "мы не будем, но поверь, что тебя ждет лучший финал 2023!",
          6),
    "7": ("Возможен ли возврат билета?", "Да, при затруднениях с процессом возврата билета пиши в поддержку.", 7)
}


async def send_faq(chat_id):
    if not await BotDB.user_banned(chat_id):
        await main.bot.send_message(chat_id,
                                    "Тут ты сможешь узнать немного о нас или, если у тебя есть вопросы, то задай их "
                                    "поддержке, там тебе помогут",
                                    reply_markup=keyboards.faq_kb)
    else:
        reason = await BotDB.get_reason(chat_id)
        admin = await BotDB.get_admin(chat_id)
        await main.bot.send_message(chat_id,
                                    f"Вы были заблокированы\nПричина: {reason}\nАдминистратор: {admin}\nОбжалование: @theharlsquinn")


async def send_support(chat_id):
    if not await BotDB.user_banned(chat_id):
        await main.bot.send_message(chat_id,
                                    f"Контакты нашей команды:",
                                    reply_markup=keyboards.backfaq_kb)
    else:
        reason = await BotDB.get_reason(chat_id)
        admin = await BotDB.get_admin(chat_id)
        await main.bot.send_message(chat_id,
                                    f"Вы были заблокированы\nПричина: {reason}\nАдминистратор: {admin}\nОбжалование: @theharlsquinn")


async def send_question(number, chat_id):
    if not await BotDB.user_banned(chat_id):
        for question, answer, num in questions.values():
            if int(number) == int(num):
                await main.bot.send_message(chat_id, f"<b>{question}</b>\n\n{answer}", parse_mode=types.ParseMode.HTML,
                                            reply_markup=keyboards.backf_kb)
    else:
        print("HUI")
