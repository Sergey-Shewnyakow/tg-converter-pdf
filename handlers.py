import re
from aiogram import Bot, types, Dispatcher, F, Router
from aiogram.enums import ParseMode, ContentType
from aiogram import Dispatcher, Bot, types
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from main import bot, a2p_client, bot_token
import keyboards as kb
import fitz
import aiohttp
import PyPDF2

from io import BytesIO


router = Router()
page = 0
class ConversionState(StatesGroup):
    waiting_for_conversion = State()
    waiting_for_merge = State()
    waiting_for_edit = State()
    waiting_for_editer = State()

@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в нашего бота! Выберите действие!',
                           reply_markup=kb.main)

@router.message(lambda message: message.text in ['Преобразовать в PDF 📝', 'Объединить PDF 📚', "Смотреть/Разделить PDF ✂️"])
async def convert_or_merge(message: types.Message, state: FSMContext):
    if message.text == "Преобразовать в PDF 📝":
        await state.set_state(ConversionState.waiting_for_conversion)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отправьте файл для конвертации")
    elif message.text == "Объединить PDF 📚":
        await state.set_state(ConversionState.waiting_for_merge)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отправьте несколько pdf файлов одним сообщением")
    elif message.text == "Смотреть/Разделить PDF ✂️":
        await state.set_state(ConversionState.waiting_for_edit)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Укажите диапазон страниц, после отправьте файл")

    print(await state.get_state())


@router.message(F.content_type == ContentType.DOCUMENT)
async def process_document(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print(current_state)

    if current_state == 'ConversionState:waiting_for_conversion':
        await convert_to_pdf(message)
        await state.clear()

    elif current_state == 'ConversionState:waiting_for_merge':
        await merge_documents(message)
        await state.clear()

    elif current_state == 'ConversionState:waiting_for_edit' :
        await edit_doc(message)
        await state.clear()

    # elif current_state == 'ConversionState:waiting_for_editor' :
    #     await edit_doc(message, 0, 2)
    #     await state.clear()

    elif current_state == None :
        await message.answer("Сначала выберите действие!")
async def convert_to_pdf(message: types.Message):
    if message.document.mime_type != 'application/pdf':
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        print(file_info)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        api_response = a2p_client.LibreOffice.any_to_pdf(
            file_url, inline=False,
            file_name='test.pdf')
        file_pdf = api_response.result.get('FileUrl')
        await bot.send_document(message.chat.id, file_pdf)
    else:
        pass

file_links = []

async def merge_documents(message: types.Message):
    if message.document:
        document = message.document
        file_info = await bot.get_file(document.file_id)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        file_links.append(file_url)
        if len(file_links) >= 2:
            await merge_files(message)
async def merge_files(message: types.Message):
    if len(file_links) > 1:
        links_to_pdfs = file_links
        merge_result = a2p_client.PdfSharp.merge(links_to_pdfs, inline=True, file_name='test.pdf')
        u_pdf = merge_result.result.get('FileUrl')
        await bot.send_document(message.chat.id, u_pdf)
        file_links.clear()
    else:
        await bot.send_message(message.chat.id, "Недостаточно файлов")

# async def editors_doc(message: types.Message, start, end):
#     file_id = message.document.file_id
#     file_info = await bot.get_file(file_id)
#     print(file_info)
#     file_path = file_info.file_path
#     file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
#     url = file_url
#     response = a2p_client.PdfSharp.extract_pages(url, start, end)
#     u_pdf = response.result.get('FileUrl')
#     await bot.send_document(message.chat.id, u_pdf)


async def download_pdf_from_url(pdf_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(pdf_url) as response:
            if response.status == 200:
                return await response.read()
            else:
                return None

async def get_pdf_data_from_message(message):
    if message.document.mime_type == 'application/pdf':
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        pdf_data = await bot.download_file(file_info.file_path)
        with open("Temp/temp_file.pdf", "wb") as file:
            file.write(pdf_data.read())
        return pdf_data
    else:
        return None

total_pages = 0
async def pdf_page_to_image(pdf_data, num):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    global total_pages
    total_pages = pdf_document.page_count
    page = pdf_document.load_page(num)
    image = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).tobytes("png")
    pdf_document.close()

    return image

async def edit_doc(message: types.Message):
    pdf_data = await get_pdf_data_from_message(message)
    page = 0
    if pdf_data:
        image_data = await pdf_page_to_image(pdf_data, page)
        with open("Temp/image.png", "wb") as file:
            file.write(image_data)
        await bot.send_photo(chat_id=message.chat.id, photo=types.FSInputFile(path="Temp/image.png"), reply_markup=kb.selection, caption= 'Если хотите сохранить определенный страницы напишите в формате (1-2)')



@router.callback_query(F.data == 'back')
async def back_line(callback:CallbackQuery):
    global page
    page -= 1
    if page < 0:
        await callback.answer("1")
        page += 1
    else:
        await callback.answer(f"{page + 1}")
        with open("Temp/temp_file.pdf", "rb") as file:
            pdf_data = file.read()
            file_info = await pdf_page_to_image(pdf_data, page)
        with open("Temp/temp_photo.png", "wb") as files:
            files.write(file_info)
        await callback.bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=types.InputMediaPhoto(media= types.FSInputFile(path ='Temp/temp_photo.png')),reply_markup= kb.selection
        )
@router.callback_query(F.data == 'forward')
async def forward_line(callback:CallbackQuery):
    global page
    page += 1
    if total_pages == page:
        page -= 1
    await callback.answer(f"{page + 1}")
    with open("Temp/temp_file.pdf", "rb") as file:
        pdf_data = file.read()
        file_info = await pdf_page_to_image(pdf_data, page)
    with open("Temp/temp_photo.png", "wb") as files:
        files.write(file_info)
    await callback.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=types.InputMediaPhoto(media= types.FSInputFile(path ='Temp/temp_photo.png')),reply_markup= kb.selection
    )

@router.callback_query(F.data == 'divide')
async def divide_line(callback:CallbackQuery):
    await callback.answer(f"Разделить pdf")
    await callback.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=types.InputMediaPhoto(media= types.FSInputFile(path ='Temp/temp_photo.png'), caption= "Введите диапозон")
    )

@router.message()
async def handle_message(message: types.Message,  state: FSMContext):
    text = message.text.strip()
    match = re.match(r'^(\d+)-(\d+)$', text)
    if match:
        start_page = int(match.group(1))
        end_page = int(match.group(2))
        await bot.send_message(message.chat.id, f"{start_page} , {end_page}")
        await split_pdf(start_page, end_page, message)
    else:
        await message.reply("Пожалуйста, введите диапазон в формате 'начальная_страница-конечная_страница', например '1-4'.")


async def split_pdf(start_page, end_page, message):
    with open("Temp/temp_file.pdf", 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()
        for page_number in range(start_page - 1, min(end_page, len(pdf_reader.pages))):
            pdf_writer.add_page(pdf_reader.pages[page_number])
        with open("Temp/divide.pdf", "wb") as output_file:
            pdf_writer.write(output_file)

        await bot.send_document(message.chat.id, types.FSInputFile("Temp/divide.pdf"))
