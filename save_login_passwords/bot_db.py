import sqlite3 as sq  # Импорт необходимых модулей и библиотек
from save_login_passwords.login_password_bot import dp, bot
from save_login_passwords.login_password_bot import start_buttons, button_fist_choice


def sql_start():
    global base, cur
    base = sq.connect('info.db')  # Подключаемся к БД или создаем БД (если ее нет)
    cur = base.cursor()  # Создаем курсор
    if base:  # Проверка подключения
        print('\nData base accounts connected!')
    base.execute('CREATE TABLE IF NOT EXISTS accounts(login PRIMARY KEY, password TEXT)')  # Создаем таблицу, в которую будем вносить данные
    base.commit()  # Сохранение изменений


async def sql_add_account(login, password):
    cur.execute('INSERT INTO accounts VALUES (?, ?)', (login, password))  # Запись данных в таблицу в поля login, password
    base.commit()


async def sql_read_info(message):
    try:
        acc_count = 0  # Создание переменной номера аккаунтов
        accounts = ''  # Создание переменной с информацией об аккаунтах
        for info in cur.execute('SELECT * FROM accounts').fetchall():  # Извлечение информации из БД
            acc_count += 1
            accounts += f'\nАккаунт {acc_count}\nЛогин: {info[0]}\nПароль: {info[1]}\n'
        await bot.send_message(message.from_user.id, accounts)
    except:
        await bot.send_message(message.from_user.id, 'Добавленных аккаунтов нет',
                               reply_markup=start_buttons)


async def delete_account_db(message, login):
    try:
        count = 0  # Создание переменной-счетчика
        for log in cur.execute('SELECT * FROM accounts').fetchall():  # Извлечение информации из БД
            if login == log[0]:  # Проверка наличия логина в базе данных
                sql_update_query = """DELETE from accounts where login = ?"""
                cur.execute(sql_update_query, (login,))  # Удаление логина из БД
                base.commit()  # Соранение изменений в БД
                await bot.send_message(message.from_user.id, "Аккаунт успешно удален", reply_markup=button_fist_choice)
                count += 1
        if count == 0:  # Обработка в случае, если логин не был найден
            await bot.send_message(message.from_user.id, 'Логин не найден', reply_markup=button_fist_choice)

    except sq.Error as error:  # Обработка возможной ошибки при работе с бд
        await bot.send_message(message.from_user.id, f"Ошибка при работе с SQLite, {error}",
                               reply_markup=button_fist_choice)


async def delete_all_accounts_db(message):  # Функция для удаления всех аккаунтов из БД
    try:
        sql_update_query = """DELETE from accounts"""
        cur.execute(sql_update_query)  # Удаляем аккаунты
        base.commit()  # Соранение изменений в БД
        await bot.send_message(message.from_user.id, "Аккаунты успешно удалены", reply_markup=button_fist_choice)

    except sq.Error as error:  # Обработка возможной ошибки при работе с бд
        await bot.send_message(message.from_user.id, f"Ошибка при работе с SQLite, {error}",
                               reply_markup=button_fist_choice)
