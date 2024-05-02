from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard= [
    [KeyboardButton(text="Преобразовать в PDF")],
    [KeyboardButton(text="Объединить PDF")],
    [KeyboardButton(text="Редоктировать PDF")]

],                   resize_keyboard= True, input_field_placeholder= "Выберите действие")
