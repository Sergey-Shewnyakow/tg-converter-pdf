from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup
from aiogram import types


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text="Преобразовать в pdf")],
        [types.KeyboardButton(text="Объединить pdf")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
        one_time_keyboard=True
    )
    return keyboard