from api2pdf import Api2Pdf
import asyncio
import logging
import os
from dotenv import load_dotenv
from handlers import *

load_dotenv()

a2p_client = Api2Pdf(os.getenv("pdf_api"))
bot_token = os.getenv("BOT_API_KEY")
bot = Bot(token= os.getenv("BOT_API_KEY"))
dp = Dispatcher()


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')