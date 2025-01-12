from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

faq = InlineKeyboardButton(text="📝FAQ", callback_data="faq")
event = InlineKeyboardButton(text="‼️Мероприятия‼️", callback_data="event")
prof = InlineKeyboardButton(text="👥Профиль", callback_data="prof")
giveaway = InlineKeyboardButton(text="🎁Розыгрыши", callback_data="giveaway")
main_kb = InlineKeyboardMarkup().add(prof, event).add(giveaway,faq)

back = InlineKeyboardButton(text="⏪Назад⏪", callback_data="back")
backf = InlineKeyboardButton(text="⏪Назад⏪", callback_data="backf")
backe = InlineKeyboardButton(text="⏪Назад⏪", callback_data="backe")
backp = InlineKeyboardButton(text="⏪Назад⏪", callback_data="backp")
prof_kb = InlineKeyboardMarkup().add(back)
bazhen = InlineKeyboardButton(text="❓По всем вопросам❓", url="tg://user?id=734059135")
tech = InlineKeyboardButton(text="👨‍💻В ОЧЕНЬ редких случаях👨‍💻", url="tg://user?id=555066955")

backp = InlineKeyboardButton(text="⏪Назад⏪", callback_data="backp")
backfaq_kb = InlineKeyboardMarkup().add(bazhen).add(tech).add(backf)
back_kb = InlineKeyboardMarkup().add(back)
backf_kb = InlineKeyboardMarkup().add(backf)
backp_kb = InlineKeyboardMarkup().add(backp)

support = InlineKeyboardButton(text="👨‍💻Поддержка", callback_data="sup")
q1 = InlineKeyboardButton("Где пройдет вечеринка?", callback_data="q1")
q2 = InlineKeyboardButton("Когда и во сколько начнется мероприятие?", callback_data="q2")
q3 = InlineKeyboardButton("Можно ли пригласить с собой друга?", callback_data="q3")
q4 = InlineKeyboardButton("Будут ли на вечеринке напитки?", callback_data="q4")
q5 = InlineKeyboardButton("Есть ли дресс-код?", callback_data="q5")
q6 = InlineKeyboardButton("Какая будет программа?", callback_data="q6")
q7 = InlineKeyboardButton("Возможен ли возврат билета?", callback_data="q7")
faq_kb = InlineKeyboardMarkup().add(q1).add(q2).add(q3).add(q4).add(q5).add(q6).add(q7).add(support).add(back)
backe_kb = InlineKeyboardMarkup().add(backe)
soldout = InlineKeyboardButton(text="⛔БИЛЕТОВ НЕТ⛔", callback_data="soldout")
event_soldout_kb = InlineKeyboardMarkup().add(soldout).add(backe)
