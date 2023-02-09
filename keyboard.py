from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/help')
b2 = KeyboardButton('/desc')
b3 = KeyboardButton('/img')
kb.insert(b1).insert(b2).insert(b3)

ikb = InlineKeyboardMarkup(row=2)
ib = InlineKeyboardMarkup()