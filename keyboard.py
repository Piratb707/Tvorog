from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text="Назад")

ikb.add(ib1)
