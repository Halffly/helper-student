from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu():
    keyboards = [
        [
            KeyboardButton(text='Математика'),
            KeyboardButton(text='Что умеет бот?')
        ],
        [
            KeyboardButton(text="Где то ошибка"),
            KeyboardButton(text="Контакты админа")
        ]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboards)

    return markup
