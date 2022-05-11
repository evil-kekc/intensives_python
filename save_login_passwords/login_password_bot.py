from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import save_login_passwords.bot_db
import os


bot = Bot(os.getenv('TOKEN'))  # Создание экземпляра бота и получение токена из venv
dp = Dispatcher(bot, storage=MemoryStorage())  # Создание экземпляра диспетчера
admin_id = int(os.getenv('admin_id'))  # Создание id пользователя


class FSMAdmin(StatesGroup):  # Класс, в котором создаем states, для работы с машиной состояний
    first_question = State()
    choice = State()
    login = State()
    password = State()
    get_info = State()
    get_url = State()
    save_url = State()
    delete_account = State()
    delete_all_accounts = State()
    delete_all_urls = State()
    delete_url = State()
    get_num_of_comments = State()
    start_spam = State()
    end = State()


async def start_mess(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:  # Проаерка id для доступа к сообщениям бота
        await FSMAdmin.choice.set()  # Перевод бота в следующее состояние
        await message.answer('Выберите действие',
                             reply_markup=start_buttons)  # Отправка сообщения боту
    else:  # Отправка сообщения, в случае если id не в admin_id
        await bot.send_message(message.from_user.id, 'Вы не имеете прав для работы с этим ботом',
                               reply_markup=types.ReplyKeyboardRemove())


async def choice(message: types.Message, state: FSMContext):  # Функция выбора дальнейших событий
    if message.text == 'Добавить аккаунт':
        await FSMAdmin.password.set()
        await message.answer('Введите логин', reply_markup=cancel_button)

    elif message.text == 'Получить информацию':
        await save_login_passwords.bot_db.sql_read_info(message)

    elif message.text == 'Удалить аккаунт':
        await bot.send_message(message.from_user.id, f"Введите логин аккаунта, который нужно удалить",
                               reply_markup=cancel_button)
        await FSMAdmin.delete_account.set()

    elif message.text == 'Удалить все аккаунты':
        await bot.send_message(message.from_user.id, f"Вы действительно хотите удалить все аккаунты?",
                               reply_markup=delete_choice_buttons)
        await FSMAdmin.delete_all_accounts.set()


async def delete_account(message: types.Message, state=FSMContext):  # Функция для удаления аккаунта по логину
    await save_login_passwords.bot_db.delete_account_db(message=message, login=message.text)
    await state.finish()


async def delete_all_accounts(message: types.Message, state=FSMContext):  # Функция для удаления всех аккаунтов
    await save_login_passwords.bot_db.delete_all_accounts_db(message=message)
    await state.finish()


async def cancel(message: types.Message, state=FSMContext):  # Функция отмены
    await message.reply('Ввод отменен', reply_markup=button_fist_choice)
    await state.finish()


async def get_login(message: types.Message, state: FSMContext):  # Функция получения и записи логина
    global login
    async with state.proxy() as data:  # Сохранение полученного сообщения в словарь
        data['login'] = message.text
    await FSMAdmin.end.set()  # Перевод бота в следующее состояние
    await message.reply('Введите пароль')


async def end_message(message: types.Message, state: FSMContext):  # Функция сохранения пароля
    global login, password, url
    async with state.proxy() as data:  # Сохранение полученного сообщения в словарь
        data['password'] = message.text
    try:  # Запись данных в БД
        data = await state.get_data()  # Получение данных из словаря
        login = data.get('login')
        password = data.get('password')
        await save_login_passwords.bot_db.sql_add_account(login, password)
        await bot.send_message(message.from_user.id, f'Ваши данные успешно сохранены', reply_markup=button_fist_choice)
        await state.finish()
    except:  # Сообщение об исключении (в случае, если аккаунт с таким логином уже есть)
        await bot.send_message(message.from_user.id, f'Такой аакаунт уже есть', reply_markup=button_fist_choice)
        await state.finish()


def register_handlers(dp: Dispatcher):  # Функция для регистрации хэндлерова
    dp.register_message_handler(choice, state=FSMAdmin.choice)

    dp.register_message_handler(cancel, state="*", commands=['отмена', 'cancel'])
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state="*")

    dp.register_message_handler(get_login, state=FSMAdmin.password)

    dp.register_message_handler(end_message, state=FSMAdmin.end)

    dp.register_message_handler(delete_account, state=FSMAdmin.delete_account)
    dp.register_message_handler(delete_all_accounts, Text(equals='да', ignore_case=True),
                                state=FSMAdmin.delete_all_accounts)

    dp.register_message_handler(start_mess)
    dp.register_message_handler(start_mess, commands='start')


"""
******************   BUTTONS   ******************
"""

end_buttons = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton('Добавить аккаунт'), KeyboardButton('Удалить аккаунт'))\
    .row(KeyboardButton('Удалить все аккаунты'))\
    .add(KeyboardButton('Получить информацию'))

button_fist_choice = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
    .row(KeyboardButton('Выбрать действие'))

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Отмена'))

start_buttons = end_buttons

delete_choice_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Да'))\
    .add(KeyboardButton('Отмена'))


if __name__ == '__main__':
    register_handlers(dp)
    save_login_passwords.bot_db.sql_start()
    print('bot polling started')
    executor.start_polling(dp)
