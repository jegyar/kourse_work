# -*- coding: utf-8 -*-
"""
Скрипт создания отдельного Word-документа:
- Титульный лист
- Задание по курсовому проекту
- Содержание (часть содержания с готовыми разделами)

Тема: Автоматизированная информационная система управления интернет-магазина автозапчастей
Описание: Автоматизация процессов товарного учета автозапчастей, обработки клиентских заказов,
контроля движения складских запасов и формирования отчетов по продажам интернет-магазина.
"""
import os
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    """Установить внутренние отступы ячейки."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def clear_cell_borders(cell):
    """Удалить границы ячейки."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        r'<w:tcBorders {} >'
        r'  <w:top w:val="none"/>'
        r'  <w:left w:val="none"/>'
        r'  <w:bottom w:val="none"/>'
        r'  <w:right w:val="none"/>'
        r'</w:tcBorders>'.format(nsdecls('w'))
    )
    tcPr.append(tcBorders)

def add_bottom_border_to_cell(cell):
    """Добавить нижнюю черту (для подписи/подчеркивания)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        r'<w:tcBorders {} >'
        r'  <w:top w:val="none"/>'
        r'  <w:left w:val="none"/>'
        r'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        r'  <w:right w:val="none"/>'
        r'</w:tcBorders>'.format(nsdecls('w'))
    )
    tcPr.append(tcBorders)

def create_front_matter_document():
    doc = docx.Document()

    # Параметры страницы (А4, СТП БГУИР: левое 30 мм, правое 15 мм, верхнее 20 мм, нижнее 20 мм)
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(1.5)

    # Базовый шрифт документа
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(14)
    normal_font.color.rgb = RGBColor(0, 0, 0)

    # =========================================================================
    # СТРАНИЦА 1: ТИТУЛЬНЫЙ ЛИСТ
    # =========================================================================
    def title_para(text, align=WD_ALIGN_PARAGRAPH.CENTER, size=12, bold=False, before=0, after=0, spacing=1.0):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = spacing
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.bold = bold
        return p

    title_para("Министерство образования Республики Беларусь", size=12, before=0, after=2)
    title_para("Учреждение образования", size=12, before=0, after=2)
    title_para("БЕЛОРУССКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ", size=13, bold=True, before=0, after=2)
    title_para("ИНФОРМАТИКИ И РАДИОЭЛЕКТРОНИКИ", size=13, bold=True, before=0, after=14)

    # Блок факультета и кафедры
    t_info = doc.add_table(rows=3, cols=2)
    t_info.alignment = WD_TABLE_ALIGNMENT.LEFT
    col_w = [Cm(3.2), Cm(13.3)]
    info_rows = [
        ("Факультет", "информационных технологий и управления"),
        ("Кафедра", "информационных технологий автоматизированных систем"),
        ("Дисциплина", "системы управления базами данных")
    ]
    for r_i, (lbl, val) in enumerate(info_rows):
        row = t_info.rows[r_i]
        for c_i, text in enumerate((lbl, val)):
            cell = row.cells[c_i]
            cell.width = col_w[c_i]
            clear_cell_borders(cell)
            set_cell_margins(cell, top=20, bottom=20, left=0, right=0)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)

    # Центральный блок темы
    title_para("ПОЯСНИТЕЛЬНАЯ ЗАПИСКА", size=15, bold=True, before=60, after=4)
    title_para("к курсовому проекту", size=14, before=0, after=4)
    title_para("на тему", size=14, before=0, after=12)

    title_para(
        "АВТОМАТИЗИРОВАННАЯ ИНФОРМАЦИОННАЯ СИСТЕМА УПРАВЛЕНИЯ\n"
        "ИНТЕРНЕТ-МАГАЗИНА АВТОЗАПЧАСТЕЙ",
        size=15, bold=True, before=0, after=16, spacing=1.15
    )

    title_para("БГУИР  КР 6-05-0612-03 440 ПЗ", size=13, bold=True, before=0, after=70)

    # Блок подписей студента и руководителя
    t_sign = doc.add_table(rows=2, cols=3)
    t_sign.alignment = WD_TABLE_ALIGNMENT.RIGHT
    col_w_sign = [Cm(5.0), Cm(5.5), Cm(6.0)]
    sign_rows = [
        ("Студент гр. 440", "", "М. А. Иосько"),
        ("Руководитель", "", "А. И. Лаппо")
    ]
    for r_i, (col1, col2, col3) in enumerate(sign_rows):
        row = t_sign.rows[r_i]
        for c_i, text in enumerate((col1, col2, col3)):
            cell = row.cells[c_i]
            cell.width = col_w_sign[c_i]
            clear_cell_borders(cell)
            if c_i == 1:
                add_bottom_border_to_cell(cell)
            set_cell_margins(cell, top=40, bottom=40, left=40, right=40)
            p = cell.paragraphs[0]
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            if c_i == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            elif c_i == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            run = p.add_run(text if text else "")
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13)

    # Минск 2026
    title_para("Минск 2026", size=13, before=60, after=0)

    # =========================================================================
    # СТРАНИЦА 2-3: ЗАДАНИЕ ПО КУРСОВОМУ ПРОЕКТИРОВАНИЮ
    # =========================================================================
    doc.add_page_break()

    def task_head(text, align=WD_ALIGN_PARAGRAPH.CENTER, size=11, bold=False, before=0, after=2):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.bold = bold
        return p

    task_head("Учреждение образования", size=11, before=0, after=1)
    task_head("«Белорусский государственный университет информатики и радиоэлектроники»", size=12, bold=True, before=0, after=1)
    task_head("Факультет информационных технологий и управления", size=11, before=0, after=1)
    task_head("Кафедра информационных технологий автоматизированных систем", size=11, before=0, after=10)

    # Гриф УТВЕРЖДАЮ (справа)
    t_utv = doc.add_table(rows=4, cols=2)
    t_utv.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_utv_w = [Cm(8.5), Cm(8.0)]
    utv_data = [
        ("", "УТВЕРЖДАЮ"),
        ("", "Заведующий кафедрой ИТАС"),
        ("", "_________  ____________________"),
        ("", "«___» ______________ 2026 г.")
    ]
    for r_i, (left_t, right_t) in enumerate(utv_data):
        row = t_utv.rows[r_i]
        for c_i, val in enumerate((left_t, right_t)):
            cell = row.cells[c_i]
            cell.width = t_utv_w[c_i]
            clear_cell_borders(cell)
            set_cell_margins(cell, top=10, bottom=10, left=0, right=0)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            if r_i == 0 and c_i == 1:
                run.bold = True

    task_head("ЗАДАНИЕ", size=14, bold=True, before=12, after=2)
    task_head("по курсовому проектированию", size=12, bold=True, before=0, after=2)
    task_head("Студенту: Иосько Михаилу Алексеевичу", size=12, before=0, after=10)

    def task_item(num_text, content_text, underline_content=False, before=4, after=3):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = 1.1
        
        r_num = p.add_run(num_text + " ")
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(12)
        r_num.bold = True

        r_cnt = p.add_run(content_text)
        r_cnt.font.name = 'Times New Roman'
        r_cnt.font.size = Pt(12)
        if underline_content:
            r_cnt.underline = True
        return p

    def task_subitem(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(0.75)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        run.underline = True
        return p

    task_item(
        "1. Тема проекта:",
        "Автоматизированная информационная система управления интернет-магазина автозапчастей",
        underline_content=True
    )

    task_item(
        "2. Срок сдачи студентом законченного проекта:",
        "1 декабря 2026 г.",
        underline_content=True
    )

    task_item(
        "3. Исходные данные к проекту:",
        "Автоматизация процессов товарного учета автозапчастей, обработки клиентских заказов, контроля движения складских запасов и формирования отчетов по продажам интернет-магазина. Реализация базы данных в реляционной СУБД PostgreSQL в третьей нормальной форме без использования объектно-реляционного отображения (ORM) на базе прямых параметризованных SQL-запросов. Клиентская витрина с каталогом и фильтрацией, корзина покупателя, транзакционная обработка заказов со списанием остатков, пакетный обмен данными в форматах JSON, XML, CSV и генерация отчетов в форматах PDF, Excel, Word.",
        underline_content=True
    )

    task_item(
        "4. Содержание расчетно-пояснительной записки (перечень подлежащих разработке вопросов):",
        ""
    )
    task_subitem("Введение")
    task_subitem("1 Обзор исследуемой области (предметная область, анализ аналогов, постановка задачи)")
    task_subitem("2 Проектирование системы (инфологическое, логическое и архитектурное проектирование)")
    task_subitem("3 Разработка системы (выбор средств реализации, разработка базы данных и программных модулей)")
    task_subitem("4 Руководство пользователя и администратора")
    task_subitem("Заключение")
    task_subitem("Список использованных источников")
    task_subitem("Приложения")

    task_item(
        "5. Перечень графического материала (с точным обозначением обязательных чертежей и схем):",
        ""
    )
    task_subitem("1) ER-диаграмма сущностей базы данных в нотации Питера Чена;")
    task_subitem("2) Логическая схема базы данных;")
    task_subitem("3) Диаграмма вариантов использования (Use Case);")
    task_subitem("4) Диаграмма классов;")
    task_subitem("5) Схема алгоритма транзакционного оформления заказа со списанием остатков;")
    task_subitem("6) Архитектура развертывания программной системы;")
    task_subitem("7) Физическая схема базы данных (формат А3).")

    task_item(
        "6. Консультант по проекту (с обозначением разделов проекта):",
        "Трофимович А. Ф.",
        underline_content=True
    )

    task_item(
        "7. Дата выдачи задания:",
        "11 сентября 2026 г.",
        underline_content=True
    )

    task_item(
        "8. Календарный график работы над проектом на весь период проектирования:",
        ""
    )
    task_subitem("– раздел 1 к 24.09 – 30%;")
    task_subitem("– раздел 2 к 22.10 – 60%;")
    task_subitem("– раздел 3 к 19.11 – 90%;")
    task_subitem("– оформление пояснительной записки и графического материала к 11.12 – 100%.")

    # Подписи руководителя и студента в задании
    p_task_sign = doc.add_paragraph()
    p_task_sign.paragraph_format.space_before = Pt(14)
    p_task_sign.paragraph_format.space_after = Pt(4)
    p_task_sign.paragraph_format.line_spacing = 1.05

    t_tsign = doc.add_table(rows=2, cols=3)
    t_tsign.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_tsign = [Cm(6.0), Cm(5.0), Cm(5.5)]
    tsign_data = [
        ("Руководитель проекта", "", "Лаппо А. И."),
        ("Задание принял к исполнению", "", "Иосько М. А.")
    ]
    for r_i, (col1, col2, col3) in enumerate(tsign_data):
        row = t_tsign.rows[r_i]
        for c_i, text in enumerate((col1, col2, col3)):
            cell = row.cells[c_i]
            cell.width = col_w_tsign[c_i]
            clear_cell_borders(cell)
            if c_i == 1:
                add_bottom_border_to_cell(cell)
            set_cell_margins(cell, top=30, bottom=30, left=20, right=20)
            p = cell.paragraphs[0]
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            if c_i == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            elif c_i == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            run = p.add_run(text if text else "")
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.5)

    # =========================================================================
    # СТРАНИЦА 4: СОДЕРЖАНИЕ (СТП 01-2024 БГУИР)
    # =========================================================================
    doc.add_page_break()

    p_toc_head = doc.add_paragraph()
    p_toc_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_head.paragraph_format.first_line_indent = Cm(0)
    p_toc_head.paragraph_format.space_before = Pt(10)
    p_toc_head.paragraph_format.space_after = Pt(14)
    p_toc_head.paragraph_format.line_spacing = 1.15
    r_toc_h = p_toc_head.add_run("СОДЕРЖАНИЕ")
    r_toc_h.font.name = 'Times New Roman'
    r_toc_h.font.size = Pt(14)
    r_toc_h.bold = True

    # Функция добавления строки содержания с табом и точечным заполнением
    def add_toc_line(title_text, page_str, level=1, bold=False, note_badge=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(2) if level == 1 else Pt(1)
        p.paragraph_format.space_after = Pt(2) if level == 1 else Pt(1)
        p.paragraph_format.line_spacing = 1.15

        # Уровни отступа
        if level == 1:
            p.paragraph_format.first_line_indent = Cm(0)
        elif level == 2:
            p.paragraph_format.first_line_indent = Cm(0.75)
        else:
            p.paragraph_format.first_line_indent = Cm(1.25)

        # Правый таб-стоп на 16.5 см с заполнителем точками
        tab_stops = p.paragraph_format.tab_stops
        tab_stops.add_tab_stop(Cm(16.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

        run_title = p.add_run(title_text)
        run_title.font.name = 'Times New Roman'
        run_title.font.size = Pt(13) if level == 1 else Pt(12.5)
        run_title.bold = bold

        if note_badge:
            run_badge = p.add_run(f"  [{note_badge}]")
            run_badge.font.name = 'Times New Roman'
            run_badge.font.size = Pt(10.5)
            run_badge.font.italic = True
            run_badge.font.color.rgb = RGBColor(0, 110, 50)  # Зеленый акцент

        run_tab = p.add_run("\t")
        run_page = p.add_run(page_str)
        run_page.font.name = 'Times New Roman'
        run_page.font.size = Pt(13) if level == 1 else Pt(12.5)
        run_page.bold = bold
        return p

    # Строки содержания
    toc_structure = [
        ("ВВЕДЕНИЕ", "4", 1, True, "выполнено"),
        ("1 ОБЗОР ИССЛЕДУЕМОЙ ОБЛАСТИ", "5", 1, True, "выполнено"),
        ("1.1 Описание предметной области", "5", 2, False, "выполнено"),
        ("1.2 Обзор аналогов", "6", 2, False, "выполнено"),
        ("1.3 Постановка задачи", "8", 2, False, "выполнено"),
        ("2 ПРОЕКТИРОВАНИЕ СИСТЕМЫ", "10", 1, True, None),
        ("2.1 Инфологическое и логическое проектирование базы данных", "10", 2, False, None),
        ("2.2 Архитектурное проектирование системы", "14", 2, False, None),
        ("3 РАЗРАБОТКА СИСТЕМЫ", "18", 1, True, None),
        ("3.1 Выбор и обоснование средств реализации", "18", 2, False, None),
        ("3.2 Реализация базы данных", "20", 2, False, None),
        ("3.3 Программная реализация модулей системы", "24", 2, False, None),
        ("4 РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ И АДМИНИСТРАТОРА", "29", 1, True, None),
        ("4.1 Руководство пользователя", "29", 2, False, None),
        ("4.2 Руководство администратора", "32", 2, False, None),
        ("ЗАКЛЮЧЕНИЕ", "35", 1, True, None),
        ("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", "37", 1, True, None),
        ("ПРИЛОЖЕНИЕ А Скрипты генерации схемы базы данных", "39", 1, True, None),
        ("ПРИЛОЖЕНИЕ Б Графический материал курсового проекта", "43", 1, True, None),
    ]

    for title_text, page_str, level, bold, badge in toc_structure:
        add_toc_line(title_text, page_str, level=level, bold=bold, note_badge=badge)

    # Примечание о статусе выполнения под содержанием
    p_note = doc.add_paragraph()
    p_note.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_note.paragraph_format.first_line_indent = Cm(0)
    p_note.paragraph_format.space_before = Pt(20)
    p_note.paragraph_format.space_after = Pt(0)
    p_note.paragraph_format.line_spacing = 1.15
    r_n = p_note.add_run(
        "Примечание: отметкой [выполнено] выделена часть пояснительной записки (Введение и Глава 1 с подразделами 1.1–1.3), "
        "сформированная в соответствии со стандартом СТП 01-2024 в отдельном файле."
    )
    r_n.font.name = 'Times New Roman'
    r_n.font.size = Pt(11)
    r_n.font.italic = True
    r_n.font.color.rgb = RGBColor(90, 90, 90)

    # Сохранение файлов
    out_dir_main = os.path.join(os.getcwd(), 'front_matter')
    os.makedirs(out_dir_main, exist_ok=True)
    out_path = os.path.join(out_dir_main, 'Титульный_лист_Задание_Содержание.docx')
    doc.save(out_path)
    print(f"Документ успешно создан: {out_path}")
    print(f"Размер: {os.path.getsize(out_path)} байт")

    # Также сохраняем копию в папку chapter_1 для удобства доступа
    ch1_copy = os.path.join(os.getcwd(), 'chapter_1', 'Титульный_лист_Задание_Содержание.docx')
    try:
        doc.save(ch1_copy)
        print(f"Копия сохранена: {ch1_copy}")
    except PermissionError:
        print(f"Файл {ch1_copy} занят.")

if __name__ == '__main__':
    create_front_matter_document()
