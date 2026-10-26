import io
from datetime import datetime
import openpyxl
from docx import Document
from docx.shared import Inches, Pt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Регистрация шрифта для поддержки русского языка в PDF
try:
    # Пытаемся найти Arial в Windows
    font_path = 'C:\\Windows\\Fonts\\arial.ttf'
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        PDF_FONT = 'Arial'
    else:
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        PDF_FONT = 'Arial'
except Exception as e:
    print("Warning: Could not load Cyrillic font:", e)
    PDF_FONT = 'Helvetica'

def generate_sales_excel(data: list[dict]) -> io.BytesIO:
    """Генерация Excel-отчета по продажам."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Продажи"
    
    # Заголовки
    headers = ["ID товара", "Название", "Категория", "Продано (шт)", "Выручка (руб)"]
    ws.append(headers)
    
    for row in data:
        ws.append([
            row['product_id'],
            row['name'],
            row['category'],
            row['total_quantity'],
            float(row['total_revenue'])
        ])
    
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return stream

def generate_summary_word(stats: dict) -> io.BytesIO:
    """Генерация Word-отчета для руководителя."""
    doc = Document()
    
    # Заголовок
    heading = doc.add_heading('Аналитический отчет по продажам', 0)
    heading.alignment = 1 # Center
    
    doc.add_paragraph(f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    
    doc.add_heading('Общие показатели', level=1)
    
    doc.add_paragraph(f"Всего заказов: {stats['orders_count']}")
    doc.add_paragraph(f"Завершенных заказов (доставлено): {stats['delivered_count']}")
    doc.add_paragraph(f"Общая выручка: {float(stats['total_revenue']):,.2f} руб.")
    doc.add_paragraph(f"Активных товаров в каталоге: {stats['products_count']}")
    doc.add_paragraph(f"Зарегистрированных клиентов: {stats['users_count']}")
    
    doc.add_heading('Топ 5 популярных товаров', level=1)
    
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Название'
    hdr_cells[1].text = 'Продано шт.'
    hdr_cells[2].text = 'Выручка'
    
    for item in stats['top_products']:
        row_cells = table.add_row().cells
        row_cells[0].text = str(item['name'])
        row_cells[1].text = str(item['quantity'])
        row_cells[2].text = f"{float(item['revenue']):.2f}"
        
    stream = io.BytesIO()
    doc.save(stream)
    stream.seek(0)
    return stream

def generate_order_invoice_pdf(order_data: dict, items: list[dict], delivery: dict) -> io.BytesIO:
    """Генерация PDF-накладной для заказа."""
    stream = io.BytesIO()
    c = canvas.Canvas(stream, pagesize=A4)
    width, height = A4
    
    # Используем шрифт с поддержкой кириллицы, если удалось загрузить
    c.setFont(PDF_FONT, 16)
    c.drawString(50, height - 50, f"Товарная накладная № {order_data['order_id']}")
    
    c.setFont(PDF_FONT, 12)
    c.drawString(50, height - 80, f"Дата заказа: {order_data['created_at']}")
    c.drawString(50, height - 100, f"Статус: {order_data['status']}")
    
    c.drawString(50, height - 140, "Данные клиента и доставки:")
    c.setFont(PDF_FONT, 10)
    
    c.drawString(50, height - 160, f"Email: {order_data['user_email']}")
    if delivery:
        c.drawString(50, height - 175, f"Адрес: {delivery['address']}, г. {delivery['city']}, {delivery['postal_code']}")
        c.drawString(50, height - 190, f"Телефон: {delivery['phone']}")
    
    # Таблица товаров (упрощенная отрисовка)
    y = height - 230
    c.setFont(PDF_FONT, 12)
    c.drawString(50, y, "Список товаров:")
    
    y -= 20
    c.setFont(PDF_FONT, 10)
    c.drawString(50, y, "Название")
    c.drawString(350, y, "Кол-во")
    c.drawString(420, y, "Цена")
    c.drawString(500, y, "Сумма")
    
    c.line(50, y - 5, 550, y - 5)
    
    y -= 20
    for item in items:
        # Обрезаем длинные названия
        name = item['name'][:40] + "..." if len(item['name']) > 40 else item['name']
        c.drawString(50, y, name)
        c.drawString(350, y, str(item['quantity']))
        c.drawString(420, y, f"{item['unit_price']:.2f}")
        c.drawString(500, y, f"{item['quantity'] * item['unit_price']:.2f}")
        y -= 20
        
        if y < 100:  # Новая страница если не влезает
            c.showPage()
            c.setFont(PDF_FONT, 10)
            y = height - 50
    
    c.line(50, y, 550, y)
    y -= 20
    c.setFont(PDF_FONT, 12)
    c.drawString(400, y, f"Итого: {order_data['total_amount']:.2f} {order_data['currency']}")
    
    c.save()
    stream.seek(0)
    return stream
