from config import BOT_API_KEY
from config import CONVERTER_API_KEY
import asyncio
from aiogram import Bot, types, Dispatcher
from aiogram.enums import ParseMode


dp = Dispatcher()


@dp.message()
async def start_cmd(message: types.Message) -> None:
    await message.answer('Привет!')


async def main() -> None:
    bot = Bot(BOT_API_KEY, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
