from aiogram.fsm.state import StatesGroup, State
from api2pdf import Api2Pdf
from config import pdf_api
from config import BOT_API_KEY
import asyncio
from aiogram import Bot, types, Dispatcher, F
from aiogram.enums import ParseMode, ContentType

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

a2p_client = Api2Pdf(pdf_api)

bot = Bot(token= BOT_API_KEY)
dp = Dispatcher()


@dp.message(F.content_type == ContentType.DOCUMENT)
async def get_doc(message: types.Message):
    if message.document.mime_type != 'application/pdf':
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        print(file_info)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{BOT_API_KEY}/{file_path}"
        api_response = a2p_client.LibreOffice.any_to_pdf(
            file_url, inline=False,
            file_name='test.pdf')
        file_pdf = api_response.result.get('FileUrl')
        await bot.send_document(message.chat.id, file_pdf)
    else:
        pass

file_links = []
@dp.message(F.content_type == ContentType.DOCUMENT)
async def get_doc(message: types.Message):
    if message.document:
        document = message.document
        file_info = await bot.get_file(document.file_id)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{BOT_API_KEY}/{file_path}"
        file_links.append(file_url)
        # Проверяем, есть ли в списке достаточное количество файлов для объединения
        if len(file_links) >= 2:
            await merge_files(message)
async def merge_files(message: types.Message):
    if len(file_links) > 1:  # Проверяем, что у нас есть более одного файла для объединения
        links_to_pdfs = file_links
        merge_result = a2p_client.PdfSharp.merge(links_to_pdfs, inline=True, file_name='test.pdf')
        u_pdf = merge_result.result.get('FileUrl')
        await bot.send_document(message.chat.id, u_pdf)
    else:
        await bot.send_message(message.chat.id, "Недостаточно файлов для объединения")

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())