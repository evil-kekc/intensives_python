from aiogram import Bot, Dispatcher, types  # Импорт необходимых модулей
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import datetime
import os


bot = Bot(os.getenv('TOKEN'))  # Создаем экземпляр бота и передаем токен из venv
dp = Dispatcher(bot)  # Создаем экземпляр диспетчера


@dp.message_handler(commands='start')  # Декоратор, "отлавливающий" только команду /start
async def start_message(message: types.Message):  # Функция, работающая после команды /start
    await bot.send_message(message.from_user.id, 'Привет, я бот, который в ответ отправит любое твое сообщение',
                           reply_markup=user_kb)
    await bot.send_message(message.from_user.id, 'Можешь узнать дату',
                           reply_markup=user_inline_kb)  # Отправка сообщения пользователю с клавиатурой
    # (reply_markup - отправка клавиатуры)


@dp.message_handler(Text(equals='пожелание доброго утра', ignore_case=True))  # Хэндлер для реагирования на кнопку
async def good_morning(message: types.Message):
    await bot.send_message(message.from_user.id, 'Доброе утро!',
                           reply_markup=user_kb)


@dp.message_handler(Text(equals='пожелание доброй ночи', ignore_case=True))   # Хэндлер для реагирования на кнопку
async def good_morning(message: types.Message):
    await bot.send_message(message.from_user.id, 'Доброй ночи!',
                           reply_markup=user_kb)


@dp.callback_query_handler(text='button_date')  # # Хэндлер для реагирования на inline-кнопку
async def good_morning(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)  # Ответ на коллбеки, его желательно писать даже если не
    # передаем в него информацию

    now = datetime.datetime.now()  # Запись даты и времени на данный момент

    await bot.send_message(callback_query.from_user.id, f'{now.strftime("%d-%m-%Y %H:%M:%S")}')  # Форматирование
    # и отправка сообщения пользователю с датой и временем


@dp.message_handler()  # Декоратор, "отлавливающий все текстовые сообщения"
async def start_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


"""     ***********************  BUTTONS  ***********************   """

button_good_morning = KeyboardButton('Пожелание доброго утра')  # Создание кнопок
button_good_night = KeyboardButton('Пожелание доброй ночи')

user_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
    .add(button_good_morning).add(button_good_night)  # Добавление кнопок на клавиатуру


button_date = InlineKeyboardButton(text='Время и дата', callback_data='button_date')  # Создание кнопок
button_url = InlineKeyboardButton(text='Ссылка на гитхаб', url='https://github.com/evil-kekc/intensives_python')

user_inline_kb = InlineKeyboardMarkup(resize_keyboard=True).add(button_date).add(button_url)

if __name__ == '__main__':  # Проверка "прямого" запуска программы
    print('bot polling started')  # Сообщение о том, что бот был запущен
    executor.start_polling(dp)  # Запуск бота "polling-ом"
