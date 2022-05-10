from aiogram import Bot, Dispatcher, types  # Импорт необходимых модулей
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from schedule_of_classes import config
from schedule_of_classes.buttons import user_kb
import datetime
import logging
import os

logging.basicConfig(level=logging.ERROR, filename="scheduler_bot.log.log",
                    format="%(asctime)s | %(levelname)s | %(funcName)s: %(lineno)d | %(message)s",
                    datefmt='%H:%M:%S')  # Добавили логгирование

bot = Bot(os.getenv('TOKEN'))  # Создаем экземпляр бота и передаем токен из venv
dp = Dispatcher(bot)  # Создаем экземпляр диспетчера


@dp.message_handler(commands='start')  # Декоратор, "отлавливающий" только команду /start
async def start_message(message: types.Message):  # Функция, работающая после команды /start
    await bot.send_message(message.from_user.id, 'Привет, я бот, который может подсказать расписание занятий',
                           reply_markup=user_kb)


@dp.message_handler(
    Text(equals=config.schedule.keys(), ignore_case=True))  # Декоратор, "отлавливающий" ключи словаря schedule
async def start_message(message: types.Message):  # Функция, работающая после команды /start
    msg = config.schedule[message.text]  # Формирование текста сообщения
    await bot.send_message(message.from_user.id, f'<b>{msg}</b>', parse_mode=types.ParseMode.HTML)


@dp.message_handler(Text(equals='сегодня', ignore_case=True))  # Декоратор, "отлавливающий" только текст 'сегодня'
async def start_message(message: types.Message):  # Функция, работающая после команды /start
    msg = config.schedule[  # Обращение к словарю schedule по ключу
        list(config.schedule.keys())  # Преобразование ключей в список для возможности обращения к значениям по индексам
        [datetime.datetime.now().weekday()]  # Получение индекса дня недели, который равен индексу ключа из списка
    ]
    await bot.send_message(message.from_user.id, f'<b>{msg}</b>', parse_mode=types.ParseMode.HTML)  # Отправка сообщения


@dp.message_handler(Text(equals='завтра', ignore_case=True))  # Декоратор, "отлавливающий" только команду /start
async def start_message(message: types.Message):  # Функция, работающая после команды /start
    msg = config.schedule[  # Обращение к словарю schedule по ключу
        list(config.schedule.keys())  # Преобразование ключей в список для возможности обращения к значениям по индексам
        [datetime.datetime.now().weekday() + 1]  # Получение индекса дня недели + 1 день
    ]
    await bot.send_message(message.from_user.id, f'<b>{msg}</b>', parse_mode=types.ParseMode.HTML)


if __name__ == '__main__':  # Проверка "прямого" запуска программы
    print('bot polling started')  # Сообщение о том, что бот был запущен
    executor.start_polling(dp)  # Запуск бота "polling-ом"
