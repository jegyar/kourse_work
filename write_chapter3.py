# -*- coding: utf-8 -*-
"""
write_chapter3.py
Adds Chapter 3 (РАЗРАБОТКА СИСТЕМЫ) and Appendix A (listings)
to an existing docx, saves as Записка_ch3.docx.
СТП 01-2024 БГУИР formatting.
"""

import copy
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import docx.opc.constants

SRC  = r"c:\Users\Lenovo\Desktop\Korse_work\Записка.docx"
DST  = r"c:\Users\Lenovo\Desktop\Korse_work\Записка_ch3.docx"

IMG_PHYSICAL  = r"c:\Users\Lenovo\Desktop\Korse_work\course-work-4sem\materials\diagrams\physical.png"
IMG_CLASSES   = r"c:\Users\Lenovo\Desktop\Korse_work\course-work-4sem\materials\diagrams\classes.png"
IMG_ARCH      = r"c:\Users\Lenovo\Desktop\Korse_work\course-work-4sem\materials\diagrams\architecture.png"

# ── helpers ──────────────────────────────────────────────────────────────────

def set_para_fmt(para, first_line=True, space_before=0, space_after=0,
                 line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    pf = para.paragraph_format
    pf.alignment        = align
    pf.space_before     = Pt(space_before)
    pf.space_after      = Pt(space_after)
    pf.line_spacing     = Pt(14 * line_spacing)   # 14pt × 1.5 = 21pt
    if first_line:
        pf.first_line_indent = Cm(1.25)
    else:
        pf.first_line_indent = Cm(0)


def set_run_font(run, size=14, bold=False, italic=False,
                 name="Times New Roman", color=None):
    run.font.name  = name
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    # East-Asian font coverage
    rpr = run._r.get_or_add_rPr()
    for tag in (qn("w:rFonts"),):
        el = rpr.find(tag)
        if el is None:
            el = OxmlElement(tag)
            rpr.insert(0, el)
        el.set(qn("w:ascii"),      name)
        el.set(qn("w:hAnsi"),      name)
        el.set(qn("w:cs"),         name)


def add_body(doc, text, first_line=True):
    p = doc.add_paragraph()
    set_para_fmt(p, first_line=first_line)
    r = p.add_run(text)
    set_run_font(r)
    return p


def add_chapter_heading(doc, text):
    """Chapter heading: ALL CAPS, centered, bold, page break before."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment         = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before      = Pt(0)
    pf.space_after       = Pt(0)
    pf.first_line_indent = Cm(0)
    pf.line_spacing      = Pt(21)
    # page break
    r0 = p.add_run()
    r0.add_break(docx.oxml.OxmlElement('w:br') if False else __import__('docx').oxml.OxmlElement('w:br'))
    # easier: insert page break via XML
    pPr = p._p.get_or_add_pPr()
    pb  = OxmlElement('w:pageBreakBefore')
    pb.set(qn('w:val'), '1')
    pPr.append(pb)
    # remove the spurious run
    p._p.remove(r0._r)

    r = p.add_run(text.upper())
    set_run_font(r, bold=True)
    return p


def add_section_heading(doc, text):
    """Subsection heading: bold, left-aligned, 1.25 cm first-line."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment         = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before      = Pt(0)
    pf.space_after       = Pt(0)
    pf.first_line_indent = Cm(1.25)
    pf.line_spacing      = Pt(21)
    r = p.add_run(text)
    set_run_font(r, bold=True)
    return p


def add_figure_caption(doc, text):
    """Centered caption without period."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment         = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before      = Pt(0)
    pf.space_after       = Pt(0)
    pf.first_line_indent = Cm(0)
    pf.line_spacing      = Pt(21)
    r = p.add_run(text)
    set_run_font(r)
    return p


def add_table_caption(doc, text):
    """Left-aligned with indent, no period."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment         = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before      = Pt(0)
    pf.space_after       = Pt(0)
    pf.first_line_indent = Cm(1.25)
    pf.line_spacing      = Pt(21)
    r = p.add_run(text)
    set_run_font(r)
    return p


def add_image_centered(doc, path, width=Cm(13.5)):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment         = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before      = Pt(0)
    pf.space_after       = Pt(0)
    pf.first_line_indent = Cm(0)
    r = p.add_run()
    r.add_picture(path, width=width)
    return p


def add_table(doc, headers, rows, col_widths=None):
    """Add a styled table. headers = list[str], rows = list[list[str]]."""
    n_cols = len(headers)
    tbl = doc.add_table(rows=1 + len(rows), cols=n_cols)
    tbl.style = 'Table Grid'
    # header row
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        for para in hdr_cells[i].paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.space_after  = Pt(0)
            for run in para.runs:
                set_run_font(run, bold=True, size=12)
            if not para.runs:
                r = para.add_run(h)
                set_run_font(r, bold=True, size=12)
                para.runs[0].text = ''
                para.clear()
                r2 = para.add_run(h)
                set_run_font(r2, bold=True, size=12)
    # data rows
    for ri, row in enumerate(rows):
        cells = tbl.rows[ri + 1].cells
        for ci, val in enumerate(row):
            cells[ci].text = val
            for para in cells[ci].paragraphs:
                para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                para.paragraph_format.space_before = Pt(0)
                para.paragraph_format.space_after  = Pt(0)
                for run in para.runs:
                    set_run_font(run, size=12)
                if not para.runs:
                    r = para.add_run(val)
                    set_run_font(r, size=12)
    # column widths
    if col_widths:
        for row_obj in tbl.rows:
            for ci, w in enumerate(col_widths):
                row_obj.cells[ci].width = w
    return tbl


def add_listing_paragraph(doc, text):
    """Courier New 10pt, no indent, no spacing, exact indentation preserved."""
    for line in text.split('\n'):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment         = WD_ALIGN_PARAGRAPH.LEFT
        pf.space_before      = Pt(0)
        pf.space_after       = Pt(0)
        pf.first_line_indent = Cm(0)
        pf.line_spacing      = Pt(12)
        r = p.add_run(line if line else ' ')
        set_run_font(r, name='Courier New', size=10)


def add_listing_heading(doc, text):
    """Heading for a listing block inside the appendix."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment         = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before      = Pt(6)
    pf.space_after       = Pt(3)
    pf.first_line_indent = Cm(0)
    pf.line_spacing      = Pt(21)
    r = p.add_run(text)
    set_run_font(r, bold=True)
    return p


# ── page margins ─────────────────────────────────────────────────────────────

def set_margins(section):
    section.left_margin   = Cm(3)
    section.right_margin  = Cm(1.5)
    section.top_margin    = Cm(2)
    section.bottom_margin = Cm(2)


# ── main ─────────────────────────────────────────────────────────────────────

doc = Document(SRC)

# Make sure margins are set on all sections
for sec in doc.sections:
    set_margins(sec)

# ═══════════════════════════════════════════════════════════════════════════
# CHAPTER 3
# ═══════════════════════════════════════════════════════════════════════════

add_chapter_heading(doc, "3 РАЗРАБОТКА СИСТЕМЫ")

# ─── 3.1 Выбор средств реализации ──────────────────────────────────────────

add_section_heading(doc, "3.1 Выбор средств реализации")

add_body(doc, (
    "Выбор программных инструментов для реализации автоматизированной информационной системы "
    "управления интернет-магазином автозапчастей основывался на требованиях к надёжности хранения "
    "данных, производительности, простоте сопровождения кода и зрелости экосистемы."
))

add_body(doc, (
    "В качестве системы управления базами данных рассматривались три кандидата: PostgreSQL 15, "
    "MySQL 8 и SQLite 3. SQLite исключена на раннем этапе как не предназначенная для "
    "многопользовательской серверной нагрузки: она не поддерживает параллельные операции записи "
    "и лишена механизма управления привилегиями. MySQL обеспечивает приемлемый уровень "
    "параллелизма и широко применяется в веб-разработке, однако уступает PostgreSQL по полноте "
    "реализации стандарта SQL и набору встроенных типов данных. PostgreSQL предоставляет полную "
    "поддержку ACID-транзакций, ограничения CHECK с произвольными предикатами, тип SERIAL для "
    "автоинкрементных ключей, а также NUMERIC(12,2) для хранения денежных значений без потерь "
    "точности. Развитая система блокировок и MVCC-архитектура PostgreSQL позволяют обслуживать "
    "конкурентный доступ без деградации согласованности данных."
))

add_body(doc, (
    "Среди фреймворков для разработки HTTP-сервера сравнивались FastAPI 0.115, Flask 3 и "
    "Django 5. Django предлагает «батарейки в комплекте»: встроенную административную панель, "
    "собственный механизм миграций и ORM-слой, однако именно тесная интеграция с ORM создаёт "
    "ограничения при написании сложных SQL-запросов. Flask лёгок и не навязывает структуру "
    "проекта, но не имеет встроенной валидации данных и требует ручного подключения сторонних "
    "библиотек для документирования API. FastAPI сочетает высокую производительность благодаря "
    "асинхронному ASGI-исполнению, строгую валидацию входных данных посредством Pydantic и "
    "автоматическую генерацию интерактивной документации OpenAPI без написания "
    "дополнительного кода."
))

add_body(doc, (
    "Среди вспомогательных библиотек выбраны: psycopg2-binary для непосредственного "
    "взаимодействия с PostgreSQL через SQL-запросы, bcrypt для хэширования паролей по алгоритму "
    "«бикрипт» с адаптивным параметром стоимости, python-jose для формирования и верификации "
    "JWT-токенов, Jinja2 для серверной шаблонизации HTML-страниц, openpyxl для формирования "
    "отчётов в формате Excel, reportlab для генерации PDF-документов и python-docx для создания "
    "документов в формате Word. Перечисленные библиотеки представлены в таблице 3.1."
))

# Table 3.1
add_table_caption(doc, "Таблица 3.1 – Сравнение выбранных программных средств")
tbl31_headers = ["Компонент", "Альтернативы", "Выбранное решение", "Обоснование выбора"]
tbl31_rows = [
    ["СУБД",             "MySQL 8, SQLite 3",         "PostgreSQL 15",       "ACID, MVCC, CHECK, NUMERIC"],
    ["Веб-фреймворк",    "Flask 3, Django 5",          "FastAPI 0.115",       "ASGI, Pydantic, OpenAPI без ORM"],
    ["Драйвер БД",       "asyncpg, aiopg",             "psycopg2-binary 2.9", "Синхронный доступ, зрелый API"],
    ["Хэширование",      "passlib/argon2, hashlib",    "bcrypt",              "Адаптивная стоимость, широкая практика"],
    ["JWT",              "PyJWT, authlib",             "python-jose",         "RSA/HS256, совместимость с FastAPI"],
    ["Шаблоны",          "Mako, Chameleon",            "Jinja2",              "Интеграция с FastAPI, богатый синтаксис"],
    ["Excel-отчёты",     "xlrd, xlwt",                 "openpyxl",            "Чтение и запись xlsx, активная поддержка"],
    ["PDF-генерация",    "WeasyPrint, fpdf2",          "reportlab",           "Точное позиционирование, canvas API"],
    ["Word-документы",   "docx2txt",                  "python-docx",         "Создание и редактирование docx"],
]
add_table(doc, tbl31_headers, tbl31_rows,
          col_widths=[Cm(3), Cm(4), Cm(4), Cm(5.5)])

add_body(doc, (
    "Совокупность выбранных инструментов обеспечивает полный стек разработки: от хранения "
    "и обработки данных до формирования отчётов и обслуживания HTTP-запросов."
))

# ─── 3.2 Реализация базы данных ────────────────────────────────────────────

add_section_heading(doc, "3.2 Реализация базы данных")

add_body(doc, (
    "Физическая схема базы данных разработана с учётом требований к целостности, "
    "производительности и удобству сопровождения. Схема включает девять таблиц: "
    "«Role», «User», «Product», «Cart», «Order», «OrderItem», «DeliveryData», "
    "«Transaction» и «Review». Физическая схема приведена на рисунке 3.1."
))

add_image_centered(doc, IMG_PHYSICAL, width=Cm(14))
add_figure_caption(doc, "Рисунок 3.1 – Физическая схема базы данных")

add_body(doc, (
    "Для первичных ключей во всех таблицах применяется тип SERIAL, что обеспечивает "
    "автоматическую генерацию уникальных числовых идентификаторов средствами PostgreSQL "
    "без участия прикладного кода. Строковые атрибуты с ограниченной длиной объявлены "
    "как VARCHAR с конкретным предельным значением: VARCHAR(255) для адресов электронной "
    "почты и наименований, VARCHAR(100) для марок и моделей автомобилей. Хэш пароля "
    "сохраняется в поле VARCHAR(255), поскольку строка bcrypt не превышает 60 символов "
    "и указанный запас обеспечивает совместимость с иными алгоритмами хэширования в "
    "перспективе. Денежные суммы хранятся в NUMERIC(12,2), что гарантирует точность "
    "до двух десятичных знаков без ошибок округления, характерных для типа FLOAT. "
    "Флаг активности товара — BOOLEAN NOT NULL DEFAULT TRUE — позволяет выполнять "
    "«мягкое» удаление записей без физического их уничтожения. Временны́е метки "
    "создания записей имеют тип TIMESTAMP NOT NULL DEFAULT NOW()."
))

add_body(doc, (
    "Нормализация схемы достигнута до третьей нормальной формы. Первая нормальная "
    "форма соблюдается за счёт атомарности всех атрибутов: каждая ячейка содержит "
    "ровно одно неделимое значение, множественные значения не используются. Вторая "
    "нормальная форма выполнена, поскольку все составные ключи отсутствуют — "
    "первичный ключ в каждой таблице единственный суррогатный атрибут SERIAL, и "
    "все остальные атрибуты функционально зависят от него целиком. Третья нормальная "
    "форма соблюдена: транзитивные зависимости устранены выделением справочника ролей "
    "в отдельную таблицу «Role» и хранением адреса доставки в отдельной таблице "
    "«DeliveryData», связанной с заказом внешним ключом."
))

add_body(doc, (
    "Для ускорения наиболее частых операций чтения в схеме созданы семь индексов. "
    "Перечень индексов с указанием покрываемых запросов и частоты использования "
    "приведён в таблице 3.2."
))

add_table_caption(doc, "Таблица 3.2 – Индексы базы данных")
tbl32_headers = ["Индекс", "Таблица.Столбец", "Покрываемая операция", "Частота"]
tbl32_rows = [
    ["IX_User_Email",    '"User"(email)',           "Поиск пользователя при аутентификации",          "Каждый вход в систему"],
    ["IX_User_Role",     '"User"(role_id)',          "Фильтрация администраторов",                     "Редко"],
    ["IX_Product_Category", "Product(category)",    "Фильтрация каталога по категории",               "Очень часто"],
    ["IX_Product_Brand", "Product(brand)",           "Фильтрация каталога по марке",                   "Очень часто"],
    ["IX_Product_Active","Product(is_active)",       "Исключение неактивных товаров из каталога",      "Каждый запрос каталога"],
    ["IX_Order_User",    '"Order"(user_id)',          "История заказов конкретного покупателя",         "Часто"],
    ["IX_Order_Status",  '"Order"(status)',           "Выборка заказов по статусу в панели администратора", "Часто"],
]
add_table(doc, tbl32_headers, tbl32_rows,
          col_widths=[Cm(4), Cm(4), Cm(6.5), Cm(3)])

add_body(doc, (
    "Ссылочная целостность обеспечивается внешними ключами с правилом CASCADE для "
    "зависимых записей. Каскадное удаление настроено для связей «Заказ — OrderItem», "
    "«Заказ — DeliveryData» и «Заказ — Transaction»: при удалении заказа связанные "
    "строки удаляются автоматически. Ограничение RESTRICT установлено на внешнем ключе "
    "«User — Role», чтобы исключить удаление роли при наличии пользователей с ней."
))

add_body(doc, (
    "Ограничения CHECK обеспечивают согласованность данных на уровне СУБД независимо "
    "от прикладного кода. Поле price таблицы Product ограничено условием price >= 0. "
    "Поле stock_quantity ограничено условием stock_quantity >= 0, что исключает "
    "отрицательный остаток на складе. Поле discount_percent ограничено диапазоном "
    "от нуля до 100 включительно. Статус заказа ограничен перечислимым CHECK-значением "
    "среди допустимых строк: 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'. "
    "Ограничение UNIQUE установлено на столбец email таблицы «User» и на составную пару "
    "(user_id, product_id) таблицы Cart, что не допускает дублирования одного товара "
    "в корзине одного пользователя."
))

# ─── 3.3 Применение интеллектуальных инструментов ─────────────────────────

add_section_heading(doc, "3.3 Применение интеллектуальных инструментов")

add_body(doc, (
    "В ходе разработки системы для ускорения рутинных задач применялись средства "
    "генерации кода на базе больших языковых моделей: GitHub Copilot и ChatGPT. "
    "Данные инструменты использовались на конкретных этапах проектирования и кодирования, "
    "а не как замена самостоятельной архитектурной работы."
))

add_body(doc, (
    "На этапе проектирования схемы данных инструменты генерировали черновые DDL-скрипты "
    "по текстовому описанию сущностей и связей. Разработчик формулировал задачу в виде "
    "требований к таблицам и ограничениям, получал предложенный вариант SQL, проверял "
    "типы данных, правила CASCADE и наличие CHECK-ограничений, после чего вносил "
    "исправления. Аналогичный цикл применялся при составлении шаблонов маршрутизаторов "
    "FastAPI: модель запроса и ожидаемый ответ описывались в задаче, ИИ-инструмент "
    "формировал заготовку функции с аннотациями типов и кодами HTTP-статусов, "
    "разработчик добавлял логику обращения к сервисному слою и покрывал код тестами."
))

add_body(doc, (
    "При работе с шаблонами Jinja2 инструменты предлагали структуру блоков наследования "
    "и расположение макросов для форм, что сократило время первоначальной настройки "
    "фронтенда. SQL-запросы с множественными JOIN и динамическими WHERE-условиями "
    "генерировались как исходная точка, требуя ручной проверки индексируемости "
    "используемых столбцов и корректности параметризации."
))

add_body(doc, (
    "Общий рабочий процесс включал четыре шага: формулировка задачи разработчиком, "
    "генерация варианта инструментом, ревизия и тестирование, корректировка при "
    "выявлении ошибок. Примеры задач, результатов генерации и необходимых исправлений "
    "приведены в таблице 3.3."
))

add_table_caption(doc, "Таблица 3.3 – Примеры применения ИИ-инструментов в разработке")
tbl33_headers = ["Задача", "Инструмент", "Результат генерации", "Что потребовало корректировки"]
tbl33_rows = [
    [
        "DDL-скрипт таблицы «Order»",
        "ChatGPT",
        "Сгенерирован CREATE TABLE с атрибутами и FK",
        "Добавлен CHECK на status, скорректирован тип total_amount на NUMERIC(12,2)"
    ],
    [
        "Маршрутизатор FastAPI для регистрации",
        "GitHub Copilot",
        "Шаблон POST-эндпоинта с Pydantic-схемой",
        "Добавлена проверка уникальности email, обработка HTTPException 400"
    ],
    [
        "SQL-запрос с фильтрами каталога",
        "ChatGPT",
        "SELECT с динамическим WHERE через конкатенацию",
        "Заменена конкатенация на параметризованный список, добавлен ILIKE"
    ],
    [
        "Шаблон Jinja2 страницы товара",
        "GitHub Copilot",
        "Структура блоков base/content/scripts",
        "Скорректированы пути к статике, добавлены aria-атрибуты"
    ],
    [
        "Функция генерации PDF-накладной",
        "ChatGPT",
        "Заготовка reportlab canvas с таблицей",
        "Настроены шрифты с кириллицей, исправлены координаты позиционирования"
    ],
]
add_table(doc, tbl33_headers, tbl33_rows,
          col_widths=[Cm(3.8), Cm(2.8), Cm(5.4), Cm(5)])

add_body(doc, (
    "Применение интеллектуальных инструментов позволило сократить время написания "
    "шаблонного кода и ускорить формирование черновых вариантов SQL и DDL. Вместе "
    "с тем архитектурные решения — разбиение на слои, выбор стратегий индексирования, "
    "проектирование транзакционной логики — принимались разработчиком самостоятельно. "
    "Верификация корректности каждого фрагмента кода через ручное тестирование и "
    "анализ граничных случаев оставалась обязательным этапом независимо от источника "
    "первоначального варианта."
))

# ─── 3.4 Программная реализация системы ───────────────────────────────────

add_section_heading(doc, "3.4 Программная реализация системы")

add_body(doc, (
    "Система реализована по трёхуровневой архитектуре: уровень представления, уровень "
    "бизнес-логики и уровень доступа к данным. Каждый уровень оформлен отдельным "
    "пакетом внутри каталога app/."
))

add_body(doc, (
    "Пакет app/routers содержит модули FastAPI-маршрутизаторов, отвечающих за разбор "
    "HTTP-запросов, валидацию входных параметров через Pydantic-схемы и формирование "
    "ответа. Маршрутизаторы не реализуют бизнес-правил напрямую — они делегируют "
    "обработку соответствующим классам сервисного уровня. Пакет app/services содержит "
    "классы AuthService, ProductService, CartService, OrderService и AdminService. "
    "Каждый сервис получает соединение с базой данных через параметр конструктора и "
    "выполняет SQL-запросы посредством курсора psycopg2. Пакет app/utils объединяет "
    "функции обеспечения безопасности (модуль security.py) и генерации отчётов "
    "(модуль reports.py). Pydantic-схемы для запросов и ответов сосредоточены в "
    "пакете app/models. Управление соединениями с PostgreSQL вынесено в app/database.py."
))

add_body(doc, (
    "Диаграмма классов системы приведена на рисунке 3.2."
))

add_image_centered(doc, IMG_CLASSES, width=Cm(14))
add_figure_caption(doc, "Рисунок 3.2 – Диаграмма классов системы")

add_body(doc, (
    "Общая архитектура развёртывания системы с указанием направлений потоков данных "
    "между компонентами показана на рисунке 3.3."
))

add_image_centered(doc, IMG_ARCH, width=Cm(14))
add_figure_caption(doc, "Рисунок 3.3 – Архитектура системы")

add_body(doc, (
    "Аутентификация пользователя реализована следующим образом. Клиент отправляет "
    "POST-запрос с адресом электронной почты и паролем. Маршрутизатор передаёт "
    "данные в метод authenticate_user() класса AuthService. Сервис выполняет SQL-запрос "
    "SELECT с условием WHERE email = %s, используя параметризованный вызов psycopg2 "
    "для защиты от инъекций. Если запись найдена, функция verify_password() из "
    "модуля security.py сравнивает переданный пароль с хранимым хэшем посредством "
    "bcrypt.checkpw(). При успешной проверке функция create_access_token() формирует "
    "JWT-токен с временем жизни 60 минут, подписывает его секретным ключом по алгоритму "
    "HS256 и возвращает клиенту. Токен сохраняется в localStorage браузера и "
    "передаётся в заголовке Authorization при последующих запросах."
))

add_body(doc, (
    "Оформление заказа реализовано как атомарная транзакция PostgreSQL. Метод "
    "create_order() класса OrderService открывает транзакцию неявно через соединение "
    "psycopg2 и выполняет следующую последовательность операций: проверяет непустоту "
    "корзины пользователя; вставляет строку в таблицу «Order» и получает "
    "сгенерированный order_id через RETURNING; для каждой позиции корзины выполняет "
    "UPDATE Product SET stock_quantity = stock_quantity - %s WHERE product_id = %s "
    "AND stock_quantity >= %s и проверяет cursor.rowcount — если значение равно нулю, "
    "товар недоступен и транзакция откатывается; вставляет строку в OrderItem с "
    "зафиксированной ценой на момент заказа; вставляет запись о доставке в "
    "DeliveryData; вставляет запись об оплате в «Transaction»; удаляет позиции "
    "корзины командой DELETE FROM Cart WHERE user_id = %s. При успешном завершении "
    "всех операций выполняется conn.commit(). При любом исключении вызывается "
    "conn.rollback(), что гарантирует атомарность: частично оформленный заказ "
    "никогда не сохраняется в базе данных."
))

add_body(doc, (
    "Экспорт каталога товаров реализован в административном маршрутизаторе. "
    "Обработчик выполняет SQL-запрос SELECT всех полей таблицы Product, после чего "
    "в зависимости от выбранного формата: при выборе CSV формирует файл через "
    "csv.DictWriter с кодировкой utf-8-sig для совместимости с Microsoft Excel; "
    "при выборе JSON сериализует список словарей через json.dumps с параметрами "
    "ensure_ascii=False и indent=2; при выборе XML строит дерево элементов через "
    "xml.etree.ElementTree. Результат в каждом случае помещается в объект BytesIO "
    "и возвращается клиенту как потоковый ответ StreamingResponse с соответствующим "
    "заголовком Content-Type и Content-Disposition для инициирования загрузки файла."
))

add_body(doc, (
    "Генерация отчётов производится полностью в оперативной памяти без создания "
    "временных файлов на диске. Функция generate_order_invoice_pdf() из модуля "
    "utils/reports.py создаёт объект BytesIO, открывает на нём холст reportlab "
    "canvas формата A4 и размещает на нём реквизиты заказа, таблицу позиций и "
    "итоговую сумму с помощью методов позиционирования canvas. Функция "
    "generate_sales_excel() формирует рабочую книгу openpyxl, заполняет ячейки "
    "данными о продажах, применяет стили и сохраняет книгу в BytesIO. Функция "
    "generate_summary_word() создаёт документ python-docx, добавляет заголовки "
    "и таблицу итогов, после чего сохраняет документ в BytesIO. Все три функции "
    "возвращают объект BytesIO, содержимое которого передаётся маршрутизатором "
    "в тело HTTP-ответа без записи на диск."
))

# ═══════════════════════════════════════════════════════════════════════════
# APPENDIX A
# ═══════════════════════════════════════════════════════════════════════════

add_chapter_heading(doc, "ПРИЛОЖЕНИЕ А")

# Title line
p_title = doc.add_paragraph()
pf = p_title.paragraph_format
pf.alignment         = WD_ALIGN_PARAGRAPH.CENTER
pf.space_before      = Pt(0)
pf.space_after       = Pt(6)
pf.first_line_indent = Cm(0)
pf.line_spacing      = Pt(21)
r_title = p_title.add_run("Листинги программы")
set_run_font(r_title, bold=True)

# ── А.1 DDL ──────────────────────────────────────────────────────────────

add_listing_heading(doc, "А.1 DDL-скрипт создания базы данных (schema.sql, фрагмент)")

DDL_CODE = """\
-- Роли пользователей
CREATE TABLE IF NOT EXISTS "Role" (
    role_id     SERIAL PRIMARY KEY,
    role_name   VARCHAR(50) NOT NULL UNIQUE
);

-- Пользователи
CREATE TABLE IF NOT EXISTS "User" (
    user_id         SERIAL PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    role_id         INTEGER NOT NULL DEFAULT 2,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT FK_User_Role FOREIGN KEY (role_id)
        REFERENCES "Role"(role_id) ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS IX_User_Email ON "User"(email);
CREATE INDEX IF NOT EXISTS IX_User_Role  ON "User"(role_id);

-- Каталог товаров
CREATE TABLE IF NOT EXISTS Product (
    product_id      SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    description     TEXT NULL,
    brand           VARCHAR(100) NOT NULL,
    car_model       VARCHAR(100) NULL,
    category        VARCHAR(100) NOT NULL,
    price           NUMERIC(12,2) NOT NULL CHECK (price >= 0),
    stock_quantity  INTEGER NOT NULL DEFAULT 0
                        CHECK (stock_quantity >= 0),
    discount_percent INTEGER NOT NULL DEFAULT 0
                        CHECK (discount_percent BETWEEN 0 AND 100),
    image_url       VARCHAR(500) NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS IX_Product_Category ON Product(category);
CREATE INDEX IF NOT EXISTS IX_Product_Brand    ON Product(brand);
CREATE INDEX IF NOT EXISTS IX_Product_Active   ON Product(is_active);

-- Заказы
CREATE TABLE IF NOT EXISTS "Order" (
    order_id        SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    total_amount    NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0),
    status          VARCHAR(20) NOT NULL DEFAULT 'pending'
                        CHECK (status IN
                            ('pending','confirmed','shipped',
                             'delivered','cancelled')),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT FK_Order_User FOREIGN KEY (user_id)
        REFERENCES "User"(user_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS IX_Order_User   ON "Order"(user_id);
CREATE INDEX IF NOT EXISTS IX_Order_Status ON "Order"(status);

-- Позиции заказа
CREATE TABLE IF NOT EXISTS OrderItem (
    item_id     SERIAL PRIMARY KEY,
    order_id    INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    CONSTRAINT FK_OrderItem_Order   FOREIGN KEY (order_id)
        REFERENCES "Order"(order_id) ON DELETE CASCADE,
    CONSTRAINT FK_OrderItem_Product FOREIGN KEY (product_id)
        REFERENCES Product(product_id) ON DELETE RESTRICT
);

-- Данные доставки
CREATE TABLE IF NOT EXISTS DeliveryData (
    delivery_id SERIAL PRIMARY KEY,
    order_id    INTEGER NOT NULL UNIQUE,
    address     VARCHAR(500) NOT NULL,
    city        VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20)  NOT NULL,
    phone       VARCHAR(30)  NOT NULL,
    CONSTRAINT FK_Delivery_Order FOREIGN KEY (order_id)
        REFERENCES "Order"(order_id) ON DELETE CASCADE
);

-- Транзакции оплаты
CREATE TABLE IF NOT EXISTS "Transaction" (
    transaction_id  SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL,
    payment_method  VARCHAR(50) NOT NULL,
    amount          NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT FK_Transaction_Order FOREIGN KEY (order_id)
        REFERENCES "Order"(order_id) ON DELETE CASCADE
);

-- Корзина
CREATE TABLE IF NOT EXISTS Cart (
    cart_id     SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    CONSTRAINT UQ_Cart_User_Product UNIQUE (user_id, product_id),
    CONSTRAINT FK_Cart_User    FOREIGN KEY (user_id)
        REFERENCES "User"(user_id) ON DELETE CASCADE,
    CONSTRAINT FK_Cart_Product FOREIGN KEY (product_id)
        REFERENCES Product(product_id) ON DELETE CASCADE
);

-- Отзывы
CREATE TABLE IF NOT EXISTS Review (
    review_id   SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment     TEXT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT FK_Review_User    FOREIGN KEY (user_id)
        REFERENCES "User"(user_id) ON DELETE CASCADE,
    CONSTRAINT FK_Review_Product FOREIGN KEY (product_id)
        REFERENCES Product(product_id) ON DELETE CASCADE
);
"""
add_listing_paragraph(doc, DDL_CODE)

# ── А.2 create_order ─────────────────────────────────────────────────────

add_listing_heading(doc, "А.2 Сервис оформления заказа (order_service.py, метод create_order)")

ORDER_CODE = """\
def create_order(self, user_id, order_data):
    cart = self.cart_service.get_cart(user_id)
    if not cart.items:
        raise HTTPException(status_code=400, detail="Корзина пуста")
    try:
        # 1. Создание заказа
        self.cursor.execute(
            'INSERT INTO "Order" (user_id, total_amount) '
            'VALUES (%s, %s) RETURNING order_id',
            (user_id, cart.total_amount)
        )
        order_id = self.cursor.fetchone()[0]

        # 2. Для каждой позиции корзины: списание остатка, вставка OrderItem
        for item in cart.items:
            self.cursor.execute(
                "UPDATE Product "
                "SET stock_quantity = stock_quantity - %s "
                "WHERE product_id = %s AND stock_quantity >= %s",
                (item.quantity, item.product_id, item.quantity)
            )
            if self.cursor.rowcount == 0:
                raise Exception(
                    f"Товар {item.name} закончился или недоступен"
                )
            self.cursor.execute(
                "INSERT INTO OrderItem "
                "(order_id, product_id, quantity, unit_price) "
                "VALUES (%s, %s, %s, %s)",
                (order_id, item.product_id, item.quantity, item.price)
            )

        # 3. Данные доставки
        self.cursor.execute(
            "INSERT INTO DeliveryData "
            "(order_id, address, city, postal_code, phone) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                order_id,
                order_data.delivery.address,
                order_data.delivery.city,
                order_data.delivery.postal_code,
                order_data.delivery.phone,
            )
        )

        # 4. Запись об оплате
        self.cursor.execute(
            'INSERT INTO "Transaction" '
            '(order_id, payment_method, amount) '
            'VALUES (%s, %s, %s)',
            (order_id, order_data.payment_method, cart.total_amount)
        )

        # 5. Очистка корзины
        self.cursor.execute(
            "DELETE FROM Cart WHERE user_id = %s",
            (user_id,)
        )

        self.conn.commit()
        return self.get_order(user_id, order_id)

    except Exception as e:
        self.conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
"""
add_listing_paragraph(doc, ORDER_CODE)

# ── А.3 generate_order_invoice_pdf ──────────────────────────────────────

add_listing_heading(doc, "А.3 Генерация PDF-накладной (utils/reports.py)")

PDF_CODE = """\
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def generate_order_invoice_pdf(order: dict) -> BytesIO:
    \"\"\"Формирует PDF-накладную для заказа. Возвращает BytesIO.\"\"\"
    pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    # Заголовок
    c.setFont("DejaVu", 16)
    c.drawCentredString(width / 2, height - 50,
                        f"Накладная № {order['order_id']}")

    # Реквизиты заказа
    c.setFont("DejaVu", 11)
    y = height - 90
    c.drawString(50, y, f"Дата:   {order['created_at']}")
    y -= 18
    c.drawString(50, y, f"Статус: {order['status']}")
    y -= 18
    c.drawString(50, y,
                 f"Адрес доставки: {order['delivery']['city']}, "
                 f"{order['delivery']['address']}")
    y -= 30

    # Заголовок таблицы позиций
    c.setFont("DejaVu", 10)
    c.drawString(50,  y, "Наименование")
    c.drawString(310, y, "Кол-во")
    c.drawString(380, y, "Цена")
    c.drawString(460, y, "Сумма")
    y -= 5
    c.line(50, y, width - 50, y)
    y -= 15

    # Строки позиций
    for item in order.get("items", []):
        total = item["quantity"] * item["unit_price"]
        c.drawString(50,  y, str(item["name"])[:45])
        c.drawString(310, y, str(item["quantity"]))
        c.drawString(380, y, f"{item['unit_price']:.2f}")
        c.drawString(460, y, f"{total:.2f}")
        y -= 15
        if y < 80:          # новая страница при необходимости
            c.showPage()
            c.setFont("DejaVu", 10)
            y = height - 50

    # Итог
    y -= 5
    c.line(50, y, width - 50, y)
    y -= 18
    c.setFont("DejaVu", 12)
    c.drawString(380, y, "Итого:")
    c.drawString(460, y, f"{order['total_amount']:.2f} руб.")

    c.save()
    buf.seek(0)
    return buf
"""
add_listing_paragraph(doc, PDF_CODE)

# ── А.4 export_products ──────────────────────────────────────────────────

add_listing_heading(doc, "А.4 Экспорт каталога товаров (app/routers/admin.py, фрагмент)")

EXPORT_CODE = """\
import csv
import json
import xml.etree.ElementTree as ET
from io import BytesIO, StringIO
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from app.database import get_db_dependency

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/products/export")
def export_products(
    fmt: str = Query("json", regex="^(json|csv|xml)$"),
    conn=Depends(get_db_dependency),
):
    \"\"\"Экспортирует все товары в выбранном формате (JSON / CSV / XML).\"\"\"
    cursor = conn.cursor()
    cursor.execute(
        "SELECT product_id, name, brand, car_model, category, "
        "       price, stock_quantity, discount_percent, is_active "
        "FROM Product ORDER BY product_id"
    )
    columns = [desc[0] for desc in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    if fmt == "json":
        content = json.dumps(rows, ensure_ascii=False,
                             indent=2, default=str)
        media_type = "application/json"
        filename   = "products.json"
        buf = BytesIO(content.encode("utf-8"))

    elif fmt == "csv":
        si = StringIO()
        writer = csv.DictWriter(si, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
        buf = BytesIO(si.getvalue().encode("utf-8-sig"))
        media_type = "text/csv"
        filename   = "products.csv"

    else:  # xml
        root = ET.Element("products")
        for row in rows:
            prod = ET.SubElement(root, "product")
            for key, val in row.items():
                child = ET.SubElement(prod, key)
                child.text = str(val) if val is not None else ""
        buf = BytesIO(
            ET.tostring(root, encoding="utf-8", xml_declaration=True)
        )
        media_type = "application/xml"
        filename   = "products.xml"

    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type=media_type,
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        },
    )
"""
add_listing_paragraph(doc, EXPORT_CODE)

# ═══════════════════════════════════════════════════════════════════════════
# Save
# ═══════════════════════════════════════════════════════════════════════════

doc.save(DST)
print(f"Saved → {DST}")
