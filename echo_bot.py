from aiogram import Bot, Dispatcher, types  # Импорт необходимых модулей
from aiogram.utils import executor
import logging
import os


logging.basicConfig(level=logging.DEBUG, filename="mylog.log",
                    format="%(asctime)s | %(levelname)s | %(funcName)s: %(lineno)d | %(message)s",
                    datefmt='%H:%M:%S')  # Добавили логгирование

bot = Bot(os.environ.get('TOKEN'))  # Создаем экземпляр бота и передаем токен из venv
dp = Dispatcher(bot)  # Создаем экземпляр диспетчера


@dp.message_handler(commands='start')  # Декоратор, "отлавливающий" только команду /start
async def start_message(message: types.Message):  # Функция, работающая после команды /start
    await bot.send_message(message.from_user.id, 'Привет, я бот, который в ответ отправит любое твое сообщение')


@dp.message_handler()  # Декоратор, "отлавливающий все текстовые сообщения"
async def start_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':  # Проверка "прямого" запуска программы
    print('bot polling started')  # Сообщение о том, что бот был запущен
    executor.start_polling(dp)  # Запуск бота "polling-ом"
