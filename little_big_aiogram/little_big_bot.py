from aiogram import Bot, Dispatcher, types  # Импорт необходимых модулей
from aiogram.utils import executor
import logging
import os
import aiofiles


logging.basicConfig(level=logging.ERROR, filename="mylog.log",
                    format="%(asctime)s | %(levelname)s | %(funcName)s: %(lineno)d | %(message)s",
                    datefmt='%H:%M:%S')  # Добавили логгирование

number = 100  # Загаданное число
count_of_attempts = 1  # Количество попыток

bot = Bot(os.environ.get('TOKEN'))  # Создаем экземпляр бота и передаем токен из venv
dp = Dispatcher(bot)  # Создаем экземпляр диспетчера


users = dict()  # Создание словаря с никами пользователей, общающихся с ботом


@dp.message_handler(commands='start')  # Декоратор, "отлавливающий" только команду /start
async def start_message(message: types.Message):  # Функция, работающая после команды /start
    global count_of_attempts

    if str(message.from_user.id) not in users.keys():  # Проверка уже добавленных пользователей
        users[str(message.from_user.id)] = message.from_user.full_name  # Добавление пользователей в словарь

        async with aiofiles.open('users_data.txt', 'w+') as users_file:
            for ID, username in users.items():
                await users_file.write(f'ID: {ID} | Username: {username}')

    if count_of_attempts == 1:
        await bot.send_message(message.from_user.id, 'Привет, я загадал число, попробуй его угадать')
    else:
        await bot.send_message(message.from_user.id, 'Введите число')


@dp.message_handler()  # Декоратор, "отлавливающий все текстовые сообщения"
async def info(message: types.Message):
    global number, count_of_attempts

    try:
        if int(message.text) == number:
            await bot.send_message(message.from_user.id, f'Вы угадали!\nКоличество попыток: {count_of_attempts}')

        elif int(message.text) < number:
            await bot.send_message(message.from_user.id, 'Введенное число меньше загаданного\n')
            count_of_attempts += 1
            await start_message(message)

        elif int(message.text) > number:
            await bot.send_message(message.from_user.id, 'Введенное число больше загаданного\n')
            count_of_attempts += 1
            print(count_of_attempts)
            await start_message(message)
    except:
        await start_message(message)


if __name__ == '__main__':  # Проверка "прямого" запуска программы
    print('bot polling started')  # Сообщение о том, что бот был запущен
    executor.start_polling(dp)  # Запуск бота "polling-ом"
