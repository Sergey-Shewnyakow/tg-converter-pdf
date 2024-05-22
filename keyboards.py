from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard= [
    [KeyboardButton(text="Преобразовать в PDF 📝")],
    [KeyboardButton(text="Объединить PDF 📚")],
    [KeyboardButton(text="Смотреть/Разделить PDF ✂️")],
    [KeyboardButton(text="Сделать титульный лист 📝")]

],                   resize_keyboard= True, input_field_placeholder= "Выберите действие")

selection = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text = "<<", callback_data = 'back'), InlineKeyboardButton(text = ">>", callback_data= 'forward')],
    [InlineKeyboardButton(text = "Разделить", callback_data= 'divide')]
])