from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from config import *
from Tex_Mes import *
from keyboard import *

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot,
                storage=storage)

class OrderStatesGroup(StatesGroup):

    product = State() # Состояние для выбора продукта
    phone = State()  # Номер телефона для связи
    adress = State()  # Адрес доставки либо самовывоз


async def on_startup(_):
    print("Starting !")

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text=START_MENU,
                           reply_markup=ReplyKeyboardRemove(),
                           parse_mode='HTML')
    await message.delete()

# !!! ФУНКЦИЯ ПРИЁМА ЗАКАЗА !!!
# Начало функции order_cmd -> load_product -> load_adress | Finish
# Функция принимает дданные от пользователя и передает в машину состояний
@dp.message_handler(commands=['order'])
async def order_cmd(message: types.Message) -> None:
    await message.reply("Напишите что вы хотите заказать в свободной форме "
                        "\n<b>Например:</b> \n10 блинчиков с творогом,"
                        "\n2 сырника и 900 г творога 4%. ",
                        parse_mode='HTML')
    await OrderStatesGroup.product.set()  # Установка состояния выбора продукта

@dp.message_handler(state=OrderStatesGroup.product)
async def load_product(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['product'] = message.text

    await message.reply('Укажите ваш номер телефона для связи.')
    await OrderStatesGroup.next()
@dp.message_handler(state=OrderStatesGroup.phone)
async def load_pnumber(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['phone'] = message.text

    await message.reply('Укажите адрес доставки или напишите слово самовывоз для замовывоза')
    await OrderStatesGroup.next()
@dp.message_handler(state=OrderStatesGroup.adress)
async def load_adress(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['adress'] = message.text
        await bot.send_message(text=f"Ваш заказ: {data['product']}\nАдрес доставки: {data['adress']}\nТелефон для связи: {data['phone']}",
                               chat_id=message.from_user.id)
        await bot.send_message(text=f"Новый заказ!\nЗаказ: {data['product']}\nАдрес доставки: {data['adress']}\nТелефон для связи: {data['phone']}",
                                chat_id=CHAT_ID)
    await message.reply(f"Спасибо за заказ!C вами свяжутся для подтверждения заказа.")
    await state.finish()

# !!! КОНЕЦ ФУНКЦИИ ПРИЕМА ЗАКАЗА !!!

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
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
