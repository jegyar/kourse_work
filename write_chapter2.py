# -*- coding: utf-8 -*-
"""
Скрипт добавления Главы 2 «ПРОЕКТИРОВАНИЕ СИСТЕМЫ»
в пояснительную записку курсовой работы БГУИР.
"""

import sys
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ─────────────────────────── пути ───────────────────────────
INPUT_PATH  = r"c:\Users\Lenovo\Desktop\Korse_work\Записка.docx"
OUTPUT_PATH = r"c:\Users\Lenovo\Desktop\Korse_work\Записка_ch2.docx"

IMG_ER       = r"c:\Users\Lenovo\Desktop\Korse_work\course-work-4sem\materials\diagrams\er_chen.png"
IMG_LOGICAL  = r"c:\Users\Lenovo\Desktop\Korse_work\course-work-4sem\materials\diagrams\logical.png"
IMG_USECASE  = r"c:\Users\Lenovo\Desktop\Korse_work\course-work-4sem\materials\diagrams\usecase.png"
IMG_CONTEXT  = r"c:\Users\Lenovo\Desktop\Korse_work\course-work-4sem\materials\diagrams\context.png"
IMG_SEQUENCE = r"c:\Users\Lenovo\Desktop\Korse_work\course-work-4sem\materials\diagrams\sequence_deliver.png"
IMG_ALGO     = r"c:\Users\Lenovo\Desktop\Korse_work\course-work-4sem\materials\diagrams\algorithm_deliver.png"

# ─────────────────────── вспомогательные функции ────────────────────────────

def set_page_margins(doc):
    """Устанавливает поля страницы по СТП 01-2024."""
    for section in doc.sections:
        section.left_margin   = Cm(3)
        section.right_margin  = Cm(1.5)
        section.top_margin    = Cm(2)
        section.bottom_margin = Cm(2)


def _apply_run_font(run, bold=False, italic=False, size_pt=14):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size_pt)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    # CJK font fallback
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"),    "Times New Roman")
    rFonts.set(qn("w:hAnsi"),   "Times New Roman")
    rFonts.set(qn("w:cs"),      "Times New Roman")
    rPr.insert(0, rFonts)


def _fmt_para(para, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
              first_indent_cm=1.25, line_spacing_pt=21,
              space_before=0, space_after=0):
    fmt = para.paragraph_format
    fmt.alignment        = align
    fmt.first_line_indent = Cm(first_indent_cm) if first_indent_cm else None
    fmt.line_spacing     = Pt(line_spacing_pt)
    fmt.space_before     = Pt(space_before)
    fmt.space_after      = Pt(space_after)
    fmt.widow_control    = True


def add_page_break(doc):
    para = doc.add_paragraph()
    run  = para.add_run()
    run.add_break(docx_break_type())
    _fmt_para(para, first_indent_cm=0)


def docx_break_type():
    from docx.oxml.ns import qn as _qn
    from docx.oxml   import OxmlElement as _OE
    br = _OE("w:br")
    br.set(_qn("w:type"), "page")
    return br  # we handle it manually below


def add_page_break_v2(doc):
    """Добавляет разрыв страницы через атрибут параграфа."""
    para = doc.add_paragraph()
    pPr  = para._p.get_or_add_pPr()
    pb   = OxmlElement("w:pageBreakBefore")
    pb.set(qn("w:val"), "true")
    pPr.append(pb)
    _fmt_para(para, first_indent_cm=0, line_spacing_pt=14)


def heading_chapter(doc, text):
    """Заголовок главы: ПРОПИСНЫЕ, по центру, жирный, разрыв страницы перед."""
    # разрыв страницы
    para_br = doc.add_paragraph()
    run_br  = para_br.add_run()
    from docx.oxml import OxmlElement as OE
    br = OE("w:br")
    br.set(qn("w:type"), "page")
    run_br._r.append(br)
    _fmt_para(para_br, first_indent_cm=0, line_spacing_pt=14)

    para = doc.add_paragraph()
    run  = para.add_run(text.upper())
    _apply_run_font(run, bold=True)
    _fmt_para(para, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent_cm=0,
              line_spacing_pt=21, space_before=0, space_after=0)
    return para


def heading_section(doc, text):
    """Заголовок раздела: жирный, выравнивание по ширине, отступ 1.25."""
    para = doc.add_paragraph()
    run  = para.add_run(text)
    _apply_run_font(run, bold=True)
    _fmt_para(para, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_indent_cm=1.25,
              line_spacing_pt=21, space_before=0, space_after=0)
    return para


def body(doc, text, first_indent=1.25):
    """Обычный абзац тела текста."""
    para = doc.add_paragraph()
    run  = para.add_run(text)
    _apply_run_font(run)
    _fmt_para(para, first_indent_cm=first_indent, line_spacing_pt=21)
    return para


def add_figure(doc, img_path, caption_text):
    """Вставляет рисунок по центру, затем подпись по центру."""
    # рисунок
    if os.path.exists(img_path):
        para_img = doc.add_paragraph()
        para_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _fmt_para(para_img, align=WD_ALIGN_PARAGRAPH.CENTER,
                  first_indent_cm=0, line_spacing_pt=21,
                  space_before=6, space_after=0)
        run_img = para_img.add_run()
        run_img.add_picture(img_path, width=Cm(13.5))
    else:
        body(doc, f"[Рисунок недоступен: {os.path.basename(img_path)}]",
             first_indent=0)

    # подпись
    para_cap = doc.add_paragraph()
    run_cap  = para_cap.add_run(caption_text)
    _apply_run_font(run_cap)
    _fmt_para(para_cap, align=WD_ALIGN_PARAGRAPH.CENTER,
              first_indent_cm=0, line_spacing_pt=21,
              space_before=0, space_after=6)
    return para_cap


def add_table_caption(doc, caption_text):
    para = doc.add_paragraph()
    run  = para.add_run(caption_text)
    _apply_run_font(run)
    _fmt_para(para, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
              first_indent_cm=1.25, line_spacing_pt=21,
              space_before=6, space_after=0)
    return para


def make_table(doc, headers, rows, col_widths=None):
    """Создаёт простую таблицу с заголовком."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # заголовочная строка
    hdr_row = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(h)
        _apply_run_font(run, bold=True, size_pt=12)
        fmt = para.paragraph_format
        fmt.space_before = Pt(2)
        fmt.space_after  = Pt(2)
        fmt.line_spacing = Pt(18)
        fmt.first_line_indent = Pt(0)

    # строки данных
    for ri, row_data in enumerate(rows):
        row = table.rows[ri + 1]
        for ci, cell_text in enumerate(row_data):
            cell = row.cells[ci]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = para.add_run(str(cell_text))
            _apply_run_font(run, size_pt=12)
            fmt = para.paragraph_format
            fmt.space_before = Pt(2)
            fmt.space_after  = Pt(2)
            fmt.line_spacing = Pt(18)
            fmt.first_line_indent = Pt(0)

    # ширины столбцов
    if col_widths:
        for row in table.rows:
            for ci, w in enumerate(col_widths):
                row.cells[ci].width = Cm(w)

    return table


# ═══════════════════════════════════════════════════════════════
#   ОСНОВНОЙ КОД
# ═══════════════════════════════════════════════════════════════

doc = Document(INPUT_PATH)
set_page_margins(doc)

# ───────────────────────────────────────────────────────────────
# ГЛАВА 2
# ───────────────────────────────────────────────────────────────
heading_chapter(doc, "2 ПРОЕКТИРОВАНИЕ СИСТЕМЫ")

# ───────────────────────────────────────────────────────────────
# 2.1 Проектирование базы данных
# ───────────────────────────────────────────────────────────────
heading_section(doc, "2.1 Проектирование базы данных")

body(doc,
     "Проектирование базы данных выполнялось в три этапа: концептуальный, "
     "логический и физический. На каждом этапе степень детализации "
     "представления данных возрастала: от абстрактных сущностей предметной "
     "области до конкретных таблиц PostgreSQL с ограничениями целостности "
     "и индексами.")

body(doc,
     "Концептуальный уровень. Концептуальная модель строилась в нотации "
     "Питера Чена и охватывает восемь сущностей предметной области: "
     "«Роль», «Пользователь», «Товар», «Корзина», «Заказ», "
     "«Позиция заказа», «Транзакция» и «Данные доставки». "
     "Центральной сущностью является «Заказ»: с ней связаны все "
     "финансовые, логистические и товарные аспекты. ER-диаграмма в нотации "
     "Питера Чена приведена на рисунке 2.1.")

add_figure(doc, IMG_ER,
           "Рисунок 2.1 – ER-диаграмма предметной области в нотации Питера Чена")

body(doc,
     "Сущность «Роль» содержит два атрибута: идентификатор роли (role_id) "
     "и наименование роли (role_name). Наименование роли уникально в "
     "пределах системы. В системе предусмотрены две роли: покупатель "
     "и администратор.")

body(doc,
     "Сущность «Пользователь» описывает зарегистрированного пользователя "
     "системы. Атрибуты: уникальный идентификатор (user_id), адрес "
     "электронной почты (email), хеш пароля (password_hash), имя "
     "(first_name), фамилия (last_name), ссылка на роль (role_id), "
     "временная метка регистрации (created_at). Поле email является "
     "уникальным ключом-кандидатом.")

body(doc,
     "Сущность «Товар» хранит данные о позициях каталога. Атрибуты: "
     "идентификатор товара (product_id), наименование (name), описание "
     "(description), бренд (brand), модель автомобиля (car_model), "
     "категория (category), цена (price), остаток на складе "
     "(stock_quantity), URL изображения (image_url), признак активности "
     "(is_active), дата создания (created_at). Атрибуты price и "
     "stock_quantity ограничены снизу нулём.")

body(doc,
     "Сущность «Корзина» реализует связь «многие ко многим» между "
     "«Пользователем» и «Товаром». Атрибуты: идентификатор записи "
     "(cart_id), ссылки на пользователя и товар (user_id, product_id), "
     "количество единиц товара (quantity, не менее одной), временная "
     "метка добавления (added_at). Пара (user_id, product_id) уникальна: "
     "один пользователь не может добавить один и тот же товар в корзину "
     "дважды — вместо этого обновляется количество.")

body(doc,
     "Сущность «Заказ» фиксирует факт оформленного заказа. Атрибуты: "
     "идентификатор заказа (order_id), ссылка на покупателя (user_id), "
     "итоговая сумма (total_amount), процент скидки (discount_percent "
     "в диапазоне от 0 до 100), статус (status), валюта (currency), "
     "временные метки создания и последнего изменения (created_at, "
     "updated_at). Статус принимает одно из шести значений: «new», "
     "«confirmed», «processing», «shipped», «delivered», «cancelled».")

body(doc,
     "Сущность «Позиция заказа» детализирует состав заказа. Атрибуты: "
     "идентификатор позиции (order_item_id), ссылки на заказ и товар "
     "(order_id, product_id), количество единиц (quantity), цена единицы "
     "на момент оформления (unit_price). Хранение цены в позиции "
     "исключает влияние последующих изменений прайс-листа на уже "
     "созданные заказы.")

body(doc,
     "Сущность «Транзакция» отражает факт оплаты заказа. Атрибуты: "
     "идентификатор транзакции (transaction_id), ссылка на заказ "
     "(order_id), способ оплаты (payment_method), сумма платежа "
     "(amount), валюта (currency), статус платежа (status), временная "
     "метка оплаты (paid_at). Способ оплаты выбирается из перечня: "
     "«card», «cash», «online», «transfer». Статус платежа принимает "
     "значения «pending», «completed», «failed», «refunded».")

body(doc,
     "Сущность «Данные доставки» хранит адресную информацию и статус "
     "логистики. Атрибуты: идентификатор доставки (delivery_id), "
     "ссылка на заказ (order_id), адрес (address), город (city), "
     "почтовый индекс (postal_code), телефон получателя (phone), "
     "статус доставки (delivery_status), ожидаемая и фактическая даты "
     "доставки (estimated_date, delivered_at). Статус принимает значения "
     "«pending», «in_transit», «delivered», «returned».")

body(doc,
     "Связи концептуального уровня. Между «Ролью» и «Пользователем» "
     "установлена связь «один ко многим»: одна роль назначается "
     "произвольному числу пользователей, каждый пользователь имеет "
     "ровно одну роль. Между «Пользователем» и «Корзиной» — связь "
     "«один ко многим»: один пользователь может иметь несколько записей "
     "в корзине, соответствующих разным товарам. Между «Товаром» и "
     "«Корзиной» — симметричная связь «один ко многим» с обратной "
     "стороны: один товар может присутствовать в корзинах разных "
     "пользователей. Итоговая связь «Пользователь–Товар» через сущность "
     "«Корзина» является связью «многие ко многим».")

body(doc,
     "Между «Пользователем» и «Заказом» — связь «один ко многим»: "
     "один пользователь оформляет произвольное число заказов. Между "
     "«Заказом» и «Позицией заказа» — связь «один ко многим»: один "
     "заказ включает одну или несколько позиций. Между «Товаром» и "
     "«Позицией заказа» — связь «один ко многим»: один товар может "
     "входить в позиции разных заказов. Между «Заказом» и "
     "«Транзакцией», а также между «Заказом» и «Данными доставки» "
     "установлены связи «один к одному»: каждому заказу соответствует "
     "не более одной транзакции и не более одной записи о доставке.")

body(doc,
     "Логический уровень. На логическом уровне каждая сущность "
     "концептуальной модели преобразуется в реляционную таблицу, "
     "связи «один ко многим» реализуются внешними ключами, а связь "
     "«многие ко многим» между пользователями и товарами вынесена в "
     "отдельную таблицу Cart. Логическая схема базы данных приведена "
     "на рисунке 2.2.")

add_figure(doc, IMG_LOGICAL,
           "Рисунок 2.2 – Логическая схема базы данных")

body(doc,
     "Первичные ключи во всех таблицах реализованы как столбцы с типом "
     "SERIAL (автоинкремент PostgreSQL). Внешние ключи обеспечивают "
     "ссылочную целостность: удаление родительской записи, когда она "
     "имеет зависимые строки, блокируется или каскадируется согласно "
     "стратегии ON DELETE CASCADE, применённой в таблицах Cart, "
     "OrderItem, Transaction и DeliveryData. Это гарантирует, что при "
     "удалении заказа вместе с ним удаляются все связанные позиции, "
     "транзакция и данные доставки.")

body(doc,
     "Нормализация. База данных приведена к третьей нормальной форме "
     "(3НФ). Первая нормальная форма (1НФ) соблюдена: все атрибуты "
     "атомарны, повторяющихся групп нет. Вторая нормальная форма (2НФ) "
     "выполнена: каждый неключевой атрибут функционально зависит "
     "от всего первичного ключа, а не от его части — это существенно "
     "для таблицы Cart, где составной ключ-кандидат (user_id, product_id) "
     "полностью определяет quantity и added_at. Третья нормальная форма "
     "(3НФ) соблюдена: транзитивных зависимостей между неключевыми "
     "атрибутами нет. Например, данные доставки не хранятся непосредственно "
     "в таблице заказа, а вынесены в отдельную таблицу DeliveryData, "
     "что исключает транзитивную зависимость адресных полей от "
     "идентификатора пользователя через заказ.")

body(doc,
     "Ограничения целостности. Для обеспечения доменной и ссылочной "
     "целостности в схеме определены следующие ограничения. "
     "Ограничение CHECK (price >= 0) на таблице Product запрещает "
     "отрицательные цены. Ограничение CHECK (stock_quantity >= 0) "
     "исключает отрицательный складской остаток. В таблице Order "
     "ограничение CHECK гарантирует допустимость значения discount_percent "
     "в диапазоне от нуля до ста включительно, а ограничение CHECK на "
     "столбце status допускает только шесть фиксированных строковых "
     "значений. Ограничение UNIQUE на столбце email таблицы User "
     "исключает дублирование учётных записей. Составное ограничение "
     "UNIQUE (user_id, product_id) таблицы Cart не позволяет добавить "
     "один и тот же товар в корзину дважды.")

body(doc,
     "Индексирование. Для ускорения типичных запросов созданы "
     "некластеризованные индексы. На таблице User — индексы по полям "
     "email и role_id. На таблице Product — индексы по полям category, "
     "brand и is_active, что ускоряет фильтрацию каталога. "
     "На таблице Order — индексы по полям user_id и status, "
     "обеспечивающие быстрый поиск заказов конкретного пользователя "
     "и выборку заказов по статусу для административных отчётов.")

# Таблица атрибутов (сводная)
add_table_caption(doc, "Таблица 2.1 – Сводная характеристика таблиц базы данных")
tbl_headers = ["Таблица", "Первичный ключ", "Внешние ключи", "Ключевые ограничения"]
tbl_rows = [
    ["Role",         "role_id",         "—",                              "UNIQUE(role_name)"],
    ["User",         "user_id",         "role_id → Role",                 "UNIQUE(email)"],
    ["Product",      "product_id",      "—",                              "CHECK price≥0, stock≥0"],
    ["Cart",         "cart_id",         "user_id → User, product_id → Product (CASCADE)", "UNIQUE(user_id, product_id), CHECK qty>0"],
    ["Order",        "order_id",        "user_id → User",                 "CHECK status IN(...), discount 0-100"],
    ["OrderItem",    "order_item_id",   "order_id → Order (CASCADE), product_id → Product", "CHECK qty>0, unit_price≥0"],
    ["Transaction",  "transaction_id",  "order_id → Order (CASCADE)",     "CHECK amount≥0, status IN(...)"],
    ["DeliveryData", "delivery_id",     "order_id → Order (CASCADE)",     "CHECK delivery_status IN(...)"],
]
make_table(doc, tbl_headers, tbl_rows, col_widths=[3.5, 3.0, 5.0, 5.0])

# ───────────────────────────────────────────────────────────────
# 2.2 Проектирование системы
# ───────────────────────────────────────────────────────────────
heading_section(doc, "2.2 Проектирование системы")

body(doc,
     "Проектирование системы включает разработку диаграммы вариантов "
     "использования, определение архитектуры приложения, построение "
     "диаграмм последовательности для ключевых сценариев и схематическое "
     "описание алгоритмов критически важных операций.")

# — Use Case —
body(doc,
     "Диаграмма вариантов использования. В системе определены два "
     "актора: «Покупатель» и «Администратор». Диаграмма вариантов "
     "использования представлена на рисунке 2.3.")

add_figure(doc, IMG_USECASE,
           "Рисунок 2.3 – Диаграмма вариантов использования")

body(doc,
     "Актор «Покупатель» взаимодействует со следующими вариантами "
     "использования: регистрация в системе, вход в личный кабинет, "
     "просмотр каталога товаров, поиск и фильтрация товаров по бренду, "
     "категории и модели автомобиля, управление корзиной (добавление, "
     "изменение количества, удаление позиций), оформление заказа "
     "с указанием адреса доставки и способа оплаты, просмотр истории "
     "заказов, а также переключение языка интерфейса.")

body(doc,
     "Актор «Администратор» обладает расширенным набором прав. "
     "Ему доступны следующие варианты использования: управление "
     "товарами (создание, редактирование, деактивация), управление "
     "заказами (смена статусов на всех этапах жизненного цикла), "
     "управление учётными записями пользователей, экспорт и импорт "
     "каталога товаров, а также генерация отчётов в форматах PDF, "
     "Excel и Word.")

# — Architecture —
body(doc,
     "Архитектура системы. Система построена по трёхуровневой "
     "клиент-серверной архитектуре. Уровень представления, уровень "
     "бизнес-логики и уровень хранения данных разграничены функционально "
     "и технологически. Контекстная диаграмма архитектуры приведена "
     "на рисунке 2.4.")

add_figure(doc, IMG_CONTEXT,
           "Рисунок 2.4 – Контекстная диаграмма архитектуры системы")

body(doc,
     "Уровень представления формируется браузером пользователя. "
     "Пользовательский интерфейс генерируется на стороне сервера "
     "с применением шаблонизатора Jinja2: FastAPI передаёт данные "
     "в HTML-шаблоны и отдаёт готовую страницу клиенту. "
     "Клиентская часть не содержит отдельного фреймворка: "
     "интерактивность обеспечивается стандартными средствами HTML, "
     "CSS и минимальным JavaScript.")

body(doc,
     "Уровень бизнес-логики реализован на базе фреймворка FastAPI "
     "(Python 3.10). FastAPI обрабатывает HTTP-запросы, выполняет "
     "проверку входных данных через Pydantic-схемы, применяет "
     "бизнес-правила и формирует ответ. Аутентификация пользователей "
     "выполняется на основе JWT-токенов (библиотека python-jose): "
     "после успешного входа клиент получает токен, который передаётся "
     "при каждом последующем запросе. Пароли хранятся исключительно "
     "в виде хешей, полученных алгоритмом bcrypt.")

body(doc,
     "Уровень хранения данных представлен СУБД PostgreSQL. "
     "Взаимодействие сервера приложений с базой данных осуществляется "
     "посредством библиотеки psycopg2: все запросы формируются "
     "вручную в виде параметризованных SQL-выражений, что исключает "
     "уязвимость SQL-инъекций. Параметризованные запросы передают "
     "пользовательские данные отдельно от SQL-кода, и драйвер "
     "выполняет их экранирование автоматически.")

# — Sequence —
body(doc,
     "Диаграмма последовательности. Сценарий оформления заказа "
     "является наиболее сложным с точки зрения взаимодействия "
     "компонентов. Диаграмма последовательности для данного сценария "
     "приведена на рисунке 2.5.")

add_figure(doc, IMG_SEQUENCE,
           "Рисунок 2.5 – Диаграмма последовательности: оформление заказа")

body(doc,
     "Покупатель отправляет POST-запрос на оформление заказа через "
     "браузер. FastAPI извлекает идентификатор пользователя из "
     "JWT-токена и передаёт управление сервисному слою. Сервисный "
     "слой открывает соединение с PostgreSQL через psycopg2 и "
     "инициирует транзакцию. В рамках транзакции выполняется выборка "
     "позиций корзины пользователя, проверка наличия товаров на складе, "
     "вставка записи заказа, вставка позиций заказа с одновременным "
     "уменьшением складского остатка, вставка данных доставки и "
     "транзакции платежа, а также очистка корзины. При успешном "
     "завершении всех операций транзакция фиксируется (COMMIT). "
     "В случае любой ошибки выполняется откат (ROLLBACK), и клиент "
     "получает сообщение об ошибке.")

# — Algorithm —
body(doc,
     "Схема алгоритма. Алгоритм транзакционного оформления заказа "
     "детализирован на уровне отдельных SQL-операций и логических "
     "проверок. Схема алгоритма приведена на рисунке 2.6.")

add_figure(doc, IMG_ALGO,
           "Рисунок 2.6 – Схема алгоритма оформления заказа")

body(doc,
     "Алгоритм начинается с проверки корзины: если корзина пуста, "
     "выполнение прерывается с возвратом ошибки. При непустой корзине "
     "открывается транзакция PostgreSQL (BEGIN). Для каждого товара "
     "в корзине производится проверка складского остатка: если "
     "остаток меньше запрошенного количества, транзакция откатывается "
     "(ROLLBACK) и пользователь получает уведомление о недостаточном "
     "количестве товара. Если остатки достаточны, выполняется "
     "INSERT INTO Order с вычисленной итоговой суммой и скидкой. "
     "Затем в цикле по позициям корзины: для каждой позиции "
     "выполняется UPDATE Product SET stock_quantity = stock_quantity "
     "- quantity и INSERT INTO OrderItem со ссылкой на созданный заказ. "
     "После обработки всех позиций выполняются INSERT INTO DeliveryData "
     "с адресом доставки и INSERT INTO Transaction с параметрами платежа. "
     "Корзина очищается запросом DELETE FROM Cart WHERE user_id = %s. "
     "Транзакция фиксируется (COMMIT), и покупателю возвращается "
     "идентификатор нового заказа.")

body(doc,
     "Применение явных транзакций PostgreSQL гарантирует атомарность "
     "операции оформления заказа: либо все изменения фиксируются "
     "одновременно, либо ни одно из них не применяется. Такой подход "
     "предотвращает ситуации, при которых остатки были бы списаны, "
     "но запись заказа не создана, или наоборот.")

# ───────────────────────────────────────────────────────────────
# Сохранение
# ───────────────────────────────────────────────────────────────
doc.save(OUTPUT_PATH)
print(f"Документ сохранён: {OUTPUT_PATH}")
