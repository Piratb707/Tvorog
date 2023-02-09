from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/help')
kb.insert(b1)

ikb = InlineKeyboardMarkup(row=2)
ib = InlineKeyboardMarkup()