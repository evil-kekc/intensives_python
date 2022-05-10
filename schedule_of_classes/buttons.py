from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton


user_kb = ReplyKeyboardMarkup(resize_keyboard=True)\
    .row(KeyboardButton('Пн'), KeyboardButton('Вт'), KeyboardButton('Ср'), KeyboardButton('Чт'),
         KeyboardButton('Пт'), KeyboardButton('Сб'),)\
    .row(KeyboardButton('Сегодня'), KeyboardButton('Завтра'))  # Добавление кнопок на клавиатуру
