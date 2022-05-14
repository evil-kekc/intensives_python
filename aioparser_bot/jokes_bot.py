import logging
import os
import random
from aiogram import Bot, Dispatcher, types  # Импорт необходимых модулей
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import aioparser_bot.aioparser


logging.basicConfig(level=logging.ERROR, filename="jokes_bot.log",
                    format="%(asctime)s | %(levelname)s | %(funcName)s: %(lineno)d | %(message)s",
                    datefmt='%H:%M:%S')  # Добавили логгирование

bot = Bot(os.getenv('TOKEN'))  # Создаем экземпляр бота и передаем токен из venv
dp = Dispatcher(bot)  # Создаем экземпляр диспетчера

list_of_jokes = []  # Создаем список с анекдотами


@dp.message_handler(commands='start')  # Декоратор, "отлавливающий" только команду /start
async def start_message(message: types.Message):  # Функция, работающая после команды /start
    global list_of_jokes
    await bot.send_message(message.from_user.id, 'Привет, я бот, который может рассказать какой-нибудь анекдот',
                           reply_markup=user_kb)

    list_of_jokes = await aioparser_bot.aioparser.run_tasks()  # Выполняем парсинг анекдотов


@dp.callback_query_handler(lambda callback: callback.data == 'joke_button')  # Декоратор, "отлавливающий" нажатие inline-кноки
async def get_joke(callback_query: types.CallbackQuery):  # Функция, которая вызывает парсер
    global list_of_jokes
    if len(list_of_jokes) == 0:  # Проверка наличия анекдотов в списке
        await bot.send_message(callback_query.from_user.id, f'Обновите базу данных анекдотов',
                               reply_markup=update_base_kb)
    else:
        await bot.answer_callback_query(callback_query.id)  # Ответ на коллбэк
        msg = random.choice(list_of_jokes)  # Выбираем рандомный анекдот
        await bot.send_message(callback_query.from_user.id, f'<b>{msg}</b>', parse_mode=types.ParseMode.HTML,
                               reply_markup=user_kb)


@dp.callback_query_handler(text='update_base_button')  # Декоратор, "отлавливающий" шаблон сообщений
async def get_joke(callback_query: types.CallbackQuery):  # Функция, которая вызывает парсер
    global list_of_jokes
    try:  # Пробуем обновить базу данных аекдотов
        list_of_jokes = await aioparser_bot.aioparser.run_tasks()  # Парсим анекдоты
        await bot.answer_callback_query(callback_query.id, 'База данных успешно обновлена', show_alert=True)
        await bot.send_message(callback_query.from_user.id, 'Хочешь получить анекдот? Тогда жми кнопку ниже!',
                               reply_markup=user_kb)

    except Exception as e:  # Обработка возможных ошибок
        await bot.send_message(callback_query.from_user.id, f'{repr(e)}', parse_mode=types.ParseMode.HTML,
                               reply_markup=update_base_kb)


"""    ********************    BUTTONS    ********************    """


user_kb = InlineKeyboardMarkup(resize_keyboard=True)\
    .add(InlineKeyboardButton('Получить анекдот', callback_data='joke_button'))  # Добавление кнопок на клавиатуру

update_base_kb = InlineKeyboardMarkup(resize_keyboard=True)\
    .add(InlineKeyboardButton('Обновить базу анекдотов', callback_data='update_base_button'))  # Добавление кнопок на клавиатуру


if __name__ == '__main__':  # Проверка "прямого" запуска программы
    print('bot polling started')  # Сообщение о том, что бот был запущен
    executor.start_polling(dp)  # Запуск бота "polling-ом"
