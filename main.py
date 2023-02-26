import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from config import *
from Tex_Mes import *


# Подключение к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы для пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, name TEXT, phone TEXT)''')

# Создание таблицы для заказов
cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                  (id INTEGER PRIMARY KEY, user_id INTEGER, status TEXT, item TEXT)''')

# Закрытие соединения с базой данных
conn.close()


# Создание клавиатуры для отмены операции
cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True
)

button1 = KeyboardButton("Создать заказ 🍽")
button2 = KeyboardButton("Отследить заказ 🕵🏻‍♂️")
button3 = KeyboardButton("Актуальное меню 👨‍🍳")
button4 = KeyboardButton("О нас ❓")
button5 = KeyboardButton("Отзывы ✍🏻")
button6 = KeyboardButton("Специальное меню 🍲")
button7 = KeyboardButton("Cвязаться с менеджером 🤙")

# Создание клавиатуры главного меню
main_menu_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True
).row(button1, button2, button3).row(button4, button5, button6).row(button7)

# Создание состояний для оформления заказа
class OrderForm(StatesGroup):
    item = State()
    phone = State()

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Добро пожаловать! Чтобы создать заказ, нажмите кнопку \"Создать заказ\".\nЧтобы отследить заказ, нажмите кнопку \"Отследить заказ\".", reply_markup=main_menu_keyboard)
    await message.delete()

# Обработчик кнопки "Создать заказ"
@dp.message_handler(Text(equals="Создать заказ 🍽"))
async def process_order_command(message: types.Message):
    await message.reply("Какой продукт Вас инетресует ?\nМожно своими словами или посмотреть в актуальном меню", reply_markup=cancel_keyboard)
    await OrderForm.item.set()
    await message.delete()

# Обработчик текстового сообщения с названием товара
@dp.message_handler(state=OrderForm.item)
async def process_order_item(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.reply("Оформление заказа отменено.", reply_markup=main_menu_keyboard)
        await message.delete()
        return

    async with state.proxy() as data:
        data['item'] = message.text
        await message.reply(f"Введите свой номер телефона для связи в формате +71234567890", reply_markup=cancel_keyboard)
        await OrderForm.next()

# Обработчик текстового сообщения с номером телефона
@dp.message_handler(state=OrderForm.phone)
async def process_order_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
        await message.reply("Спасибо за заказ! Мы свяжемся с вами в ближайшее время.", reply_markup=main_menu_keyboard)

        # Добавление заказа в базу данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, status, item) VALUES (?, ?, ?)", (message.from_user.id, "Новый заказ", data['item']))
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Отправка уведомления администратору о новом заказе
        await bot.send_message(chat_id=CHAT_ID, text=f"Поступил новый заказ №{order_id}\n\nТовар: {data['item']}\nНомер телефона: {data['phone']}")

    # Возвращение в главное меню
    await state.finish()
    await message.reply("Выберите действие:", reply_markup=main_menu_keyboard)

# Обработчик кнопки "Актуальное меню"
@dp.message_handler(Text(equals="Актуальное меню 👨‍🍳"))
async def process_actual_menu(message: types.Message):
    # Получение актуального меню
    await message.reply(MENU_PROD, parse_mode="HTML")
    await message.delete()

@dp.message_handler(Text(equals="Отзывы ✍🏻"))
async def process_comments(message: types.Message):
    # Получение отзывов
    await message.reply(COMMENTS, parse_mode="HTML")
    await message.delete()

@dp.message_handler(Text(equals="О нас ❓"))
async def process_about_autors(message: types.Message):
    # Получение информации о нас
    await message.reply(DESCRIPTION, parse_mode="HTML")
    await message.delete()

@dp.message_handler(Text(equals="Специальное меню 🍲"))
async def process_cpecial_menu(message: types.Message):
    # Получение специального меню
    await message.reply(SPECIAL_MENU, parse_mode="HTML")
    await message.delete()

@dp.message_handler(Text(equals="Cвязаться с менеджером 🤙"))
async def process_cpecial_menu(message: types.Message):
    # Получение специального меню
    await message.reply(CALL_SOUL, parse_mode="HTML")
    await message.delete()

# Обработчик кнопки "Отследить заказ"
@dp.message_handler(Text(equals="Отследить заказ 🕵🏻‍♂️"))
async def process_track_command(message: types.Message):
    # Получение списка заказов пользователя из базы данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id=?", (message.from_user.id,))
    orders = cursor.fetchall()
    conn.close()

    if not orders:
        await message.reply("У вас нет активных заказов.", reply_markup=main_menu_keyboard)
    else:
        # Отправка списка заказов пользователю
        text = "Ваши заказы:\n\n"
        for order in orders:
            text += f"Заказ №{order[0]}\nТовар: {order[3]}\nСтатус: {order[2]}\n\n"
        await message.reply(text, parse_mode=ParseMode.HTML, reply_markup=main_menu_keyboard)
    await message.delete()


# Обработчик текстовых сообщений, не являющихся командами
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply("Я не понимаю, что вы хотите сделать. Выберите действие из меню.", reply_markup=main_menu_keyboard)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

