import urllib

from aiogram import Bot, types, Dispatcher, F, Router
from aiogram.enums import ParseMode, ContentType
from aiogram import Dispatcher, Bot, types
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from main import bot, a2p_client, bot_token
import keyboards as kb


router = Router()


class ConversionState(StatesGroup):
    waiting_for_conversion = State()
    waiting_for_merge = State()
    waiting_for_edit = State()

@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в нашего бота! Выберите действие!',
                           reply_markup=kb.main)

@router.message(lambda message: message.text in ['Преобразовать в PDF 📝', 'Объединить PDF 📚', "Редоктировать PDF ✏️"])
async def convert_or_merge(message: types.Message, state: FSMContext):
    if message.text == "Преобразовать в PDF 📝":
        await state.set_state(ConversionState.waiting_for_conversion)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отправьте файл в формате docx, xlsx, txt и тд")
    elif message.text == "Объединить PDF 📚":
        await state.set_state(ConversionState.waiting_for_merge)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отправьте несколько pdf файлов одним сообщением")
    elif message.text == "Редоктировать PDF ✏️":
        await state.set_state(ConversionState.waiting_for_edit)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Отправьте PDF файл")

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



async def edit_doc(message: types.Message):
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    print(file_info)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
    url = file_url
    start = 0
    end = 2
    response = a2p_client.PdfSharp.extract_pages(url, start, end)
    u_pdf = response.result.get('FileUrl')
    await bot.send_document(message.chat.id, u_pdf)