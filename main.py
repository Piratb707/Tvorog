from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove

from config import TOKEN
from Tex_Mes import *
from keyboard import *

bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print("Starting !")


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=START_MENU,
                           parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove())
    await message.delete()

@dp.message_handler(commands=['order'])
async def order_cmd(message: types.Message):
    await bot.send_message()

@dp.message_handler(commands=['comments'])
async def comments_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=COMMENTS,
                           parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove())
    await message.delete()

@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMAND, parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove())
    await message.delete()

@dp.message_handler(commands=['about'])
async def help_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=DESCRIPTION, parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove())
    await message.delete()

@dp.message_handler(commands=['menu'])
async def send_image(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=MENU_PROD,
                           parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove())
    await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)
