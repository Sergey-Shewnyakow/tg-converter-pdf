# Telegram бот конвертер

Этот Telegram-бот предоставляет возможность конвертировать различные типы файлов в pdf, обединять файлы или удалять страницы

# Установка 
1. Склонируйте репозиторий себе на компьютер
2. Создайте файл .env
3. Укажите в нем токен на вашего бота (BOT_API_KEY = "token") и токе pdf ковертатора (pdf_api = "token")(https://portal.api2pdf.com/register)
# Использование
![image](https://github.com/Sergey-Shewnyakow/tg-converter-pdf/assets/55350656/584c2fde-6895-496d-a03c-e52f2334245c)


# Функционал 

- **Преобразование документов в PDF**: Если вы отправляете не PDF файл, бот автоматически конвертирует его в PDF, используя LibreOffice. Результаты отправляются обратно вам.

![image](https://github.com/Sergey-Shewnyakow/tg-converter-pdf/assets/55350656/79603900-d646-4a12-a3f7-0c85d959735b)


- **Объединение PDF файлов**: Можно отправить несколько PDF файлов одним сообщением. Бот объединяет их в один файл и отправляет вам обратно.

![image](https://github.com/Sergey-Shewnyakow/tg-converter-pdf/assets/55350656/e5504c0e-fcc9-4375-a3c4-48155fa6c6d0)


- **Просмотр и разделение PDF файлов**: Бот позволяет просматривать PDF файлы по страницам, а также разделять их на части. После отправки PDF файла вам предоставляется возможность указать диапазон страниц для разделения.

![image](https://github.com/Sergey-Shewnyakow/tg-converter-pdf/assets/55350656/32485816-c2dd-4989-af5d-68d5b1e14289)


- **Навигация по страницам**: В режиме просмотра PDF файлов, вы можете переходить на следующую или предыдущую страницу.

![image](https://github.com/Sergey-Shewnyakow/tg-converter-pdf/assets/55350656/48ebdf6a-4199-4464-8272-ddb0d3154e37)


- **Ввод диапазона страниц**: При запросе на разделение PDF файла, бот ожидает, что вы укажете диапазон страниц в формате "начальная_страница-конечная_страница".

![image](https://github.com/Sergey-Shewnyakow/tg-converter-pdf/assets/55350656/b94e15e7-e144-4c6e-bd31-83dbf107f53d)

- **Создание титульного листа**: Бот позволяет создать титульные листы для работ по стандартам ГУАПа.

![image](https://github.com/Sergey-Shewnyakow/tg-converter-pdf/assets/55350656/dcd3ef26-30bd-4c62-8634-8fccab6a851b)

![image](https://github.com/Sergey-Shewnyakow/tg-converter-pdf/assets/55350656/d70f79d2-89d1-43e6-969f-7f1d277c9f54)


