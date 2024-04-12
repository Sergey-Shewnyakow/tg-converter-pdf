from config import BOT_API_KEY
from config import CONVERTER_API_KEY
import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.filters import CommandStart
from keyboards import get_start_kb


bot = Bot(token=BOT_API_KEY)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в нашего бота! Выберите действие!',
                           reply_markup=get_start_kb())


@dp.message(lambda message: message.text in ['Преобразовать в pdf', 'Объединить pdf'])
async def convert_or_merge(message: types.Message):
    if message.text == "Преобразовать в pdf":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отправьте файл в формате docx, xlsx, txt и тд")
    elif message.text == "Объединить pdf":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отправьте несколько pdf файлов одним сообщением")



async def main():
    await dp.start_polling(bot)

asyncio.run(main())


