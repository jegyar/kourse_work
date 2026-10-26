from fastapi import APIRouter, Depends, Query, Response, UploadFile, File, HTTPException
import psycopg2.extensions
from typing import Optional
import csv
import json
import io
import xml.etree.ElementTree as ET

from app.database import get_db_dependency
from app.models.user import UserResponse
from app.models.product import ProductCreate, ProductResponse
from app.utils.security import get_current_admin_user

router = APIRouter(
    prefix="/admin_api",
    tags=["Admin"]
)

# ==================== PRODUCTS ====================

@router.get("/products")
def admin_get_products(
    search: Optional[str] = None,
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    cursor = conn.cursor()
    if search:
        cursor.execute(
            "SELECT * FROM Product WHERE name ILIKE %s OR brand ILIKE %s ORDER BY product_id DESC",
            (f"%{search}%", f"%{search}%")
        )
    else:
        cursor.execute("SELECT * FROM Product ORDER BY product_id DESC")

    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


@router.post("/products")
def admin_create_product(
    product: ProductCreate,
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Product (name, description, brand, car_model, category, price, stock_quantity, image_url, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING product_id""",
        (product.name, product.description, product.brand, product.car_model,
         product.category, product.price, product.stock_quantity, product.image_url, product.is_active)
    )
    pid = cursor.fetchone()[0]
    conn.commit()
    return {"product_id": pid, "message": "Товар создан"}


@router.put("/products/{product_id}")
def admin_update_product(
    product_id: int,
    product: ProductCreate,
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE Product SET name=%s, description=%s, brand=%s, car_model=%s, category=%s,
           price=%s, stock_quantity=%s, image_url=%s, is_active=%s WHERE product_id=%s""",
        (product.name, product.description, product.brand, product.car_model,
         product.category, product.price, product.stock_quantity, product.image_url,
         product.is_active, product_id)
    )
    conn.commit()
    return {"message": "Товар обновлен"}


@router.delete("/products/{product_id}")
def admin_delete_product(
    product_id: int,
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    cursor = conn.cursor()
    cursor.execute("UPDATE Product SET is_active = FALSE WHERE product_id = %s", (product_id,))
    conn.commit()
    return {"message": "Товар деактивирован"}


# ==================== ORDERS ====================

@router.get("/orders")
def admin_get_orders(
    status: Optional[str] = None,
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    cursor = conn.cursor()
    if status:
        cursor.execute(
            """SELECT o.*, u.email, u.first_name, u.last_name
            FROM "Order" o JOIN "User" u ON o.user_id = u.user_id
            WHERE o.status = %s ORDER BY o.created_at DESC""", (status,)
        )
    else:
        cursor.execute(
            """SELECT o.*, u.email, u.first_name, u.last_name
            FROM "Order" o JOIN "User" u ON o.user_id = u.user_id
            ORDER BY o.created_at DESC"""
        )
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


@router.patch("/orders/{order_id}/status")
def admin_update_order_status(
    order_id: int,
    status: str = Query(...),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    allowed = ['new', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
    if status not in allowed:
        raise HTTPException(status_code=400, detail=f"Статус должен быть одним из: {', '.join(allowed)}")

    cursor = conn.cursor()
    cursor.execute('UPDATE "Order" SET status = %s, updated_at = NOW() WHERE order_id = %s', (status, order_id))

    # Если заказ отменяется — возвращаем товар на склад
    if status == 'cancelled':
        cursor.execute("SELECT product_id, quantity FROM OrderItem WHERE order_id = %s", (order_id,))
        for row in cursor.fetchall():
            cursor.execute(
                "UPDATE Product SET stock_quantity = stock_quantity + %s WHERE product_id = %s",
                (row[0], row[1])
            )

    conn.commit()
    return {"message": f"Статус заказа #{order_id} изменен на '{status}'"}


# ==================== USERS ====================

@router.get("/users")
def admin_get_users(
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    cursor = conn.cursor()
    cursor.execute(
        """SELECT u.user_id, u.email, u.first_name, u.last_name, r.role_name, u.created_at
        FROM "User" u JOIN "Role" r ON u.role_id = r.role_id
        ORDER BY u.created_at DESC"""
    )
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


@router.patch("/users/{user_id}/role")
def admin_change_role(
    user_id: int,
    role_id: int = Query(...),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    cursor = conn.cursor()
    cursor.execute('UPDATE "User" SET role_id = %s WHERE user_id = %s', (role_id, user_id))
    conn.commit()
    return {"message": "Роль пользователя обновлена"}


@router.delete("/users/{user_id}")
def admin_delete_user(
    user_id: int,
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    admin: UserResponse = Depends(get_current_admin_user)
):
    if admin.user_id == user_id:
        raise HTTPException(status_code=400, detail="Нельзя удалить самого себя")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cart WHERE user_id = %s", (user_id,))
    cursor.execute('DELETE FROM "User" WHERE user_id = %s', (user_id,))
    conn.commit()
    return {"message": "Пользователь удален"}


# ==================== DASHBOARD STATS ====================

@router.get("/stats")
def admin_stats(
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Product WHERE is_active = TRUE")
    products = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM "User"')
    users = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM "Order"')
    orders = cursor.fetchone()[0]

    cursor.execute('SELECT COALESCE(SUM(total_amount), 0) FROM "Order" WHERE status != \'cancelled\'')
    revenue = float(cursor.fetchone()[0])

    cursor.execute(
        """SELECT o.order_id, o.total_amount, o.status, o.created_at, u.email
        FROM "Order" o JOIN "User" u ON o.user_id = u.user_id
        ORDER BY o.created_at DESC
        LIMIT 5"""
    )
    cols = [desc[0] for desc in cursor.description]
    recent_orders = [dict(zip(cols, row)) for row in cursor.fetchall()]

    return {
        "products": products,
        "users": users,
        "orders": orders,
        "revenue": revenue,
        "recent_orders": recent_orders
    }

# ==================== IMPORT / EXPORT ====================

@router.get("/export/products")
def export_products(
    format: str = Query("csv", pattern="^(csv|json|xml)$"),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name, description, brand, car_model, category, price, stock_quantity, image_url, is_active FROM Product")
    cols = [desc[0] for desc in cursor.description]
    products = [dict(zip(cols, row)) for row in cursor.fetchall()]

    if format == 'json':
        data = json.dumps(products, ensure_ascii=False, indent=2, default=str)
        return Response(content=data, media_type="application/json", headers={"Content-Disposition": "attachment; filename=products.json"})

    elif format == 'csv':
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=cols)
        writer.writeheader()
        for p in products:
            writer.writerow(p)
        return Response(content=output.getvalue().encode("utf-8-sig"), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=products.csv"})

    elif format == 'xml':
        root = ET.Element("Products")
        for p in products:
            prod_el = ET.SubElement(root, "Product")
            for k, v in p.items():
                child = ET.SubElement(prod_el, k)
                child.text = str(v) if v is not None else ""
        xml_data = ET.tostring(root, encoding="utf-8", method="xml")
        return Response(content=xml_data, media_type="application/xml", headers={"Content-Disposition": "attachment; filename=products.xml"})


@router.get("/export/sales/excel")
def export_sales_excel(
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    from app.utils.reports import generate_sales_excel
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.product_id, p.name, p.category, 
               COALESCE(SUM(oi.quantity), 0) as total_quantity,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) as total_revenue
        FROM Product p
        LEFT JOIN OrderItem oi ON p.product_id = oi.product_id
        LEFT JOIN "Order" o ON oi.order_id = o.order_id AND o.status != 'cancelled'
        GROUP BY p.product_id, p.name, p.category
        ORDER BY total_revenue DESC
    """)
    cols = [desc[0] for desc in cursor.description]
    data = [dict(zip(cols, row)) for row in cursor.fetchall()]
    
    stream = generate_sales_excel(data)
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=sales_report.xlsx"}
    )


@router.get("/export/sales/word")
def export_sales_word(
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    from app.utils.reports import generate_summary_word
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM "Order"')
    orders_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM "Order" WHERE status = \'delivered\'')
    delivered_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COALESCE(SUM(total_amount), 0) FROM "Order" WHERE status != \'cancelled\'')
    total_revenue = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM Product WHERE is_active = TRUE')
    products_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM "User" WHERE role_id = 2')
    users_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT p.name, COALESCE(SUM(oi.quantity), 0) as quantity, COALESCE(SUM(oi.quantity * oi.unit_price), 0) as revenue
        FROM Product p
        JOIN OrderItem oi ON p.product_id = oi.product_id
        JOIN "Order" o ON oi.order_id = o.order_id AND o.status != 'cancelled'
        GROUP BY p.product_id, p.name
        ORDER BY quantity DESC LIMIT 5
    """)
    top_products = [{"name": row[0], "quantity": row[1], "revenue": row[2]} for row in cursor.fetchall()]
    
    stats = {
        "orders_count": orders_count,
        "delivered_count": delivered_count,
        "total_revenue": total_revenue,
        "products_count": products_count,
        "users_count": users_count,
        "top_products": top_products
    }
    
    stream = generate_summary_word(stats)
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=sales_summary.docx"}
    )


@router.get("/orders/{order_id}/pdf")
def export_order_pdf(
    order_id: int,
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    from app.utils.reports import generate_order_invoice_pdf
    cursor = conn.cursor()
    
    cursor.execute('SELECT o.*, u.email as user_email FROM "Order" o JOIN "User" u ON o.user_id = u.user_id WHERE o.order_id = %s', (order_id,))
    order_row = cursor.fetchone()
    if not order_row:
        raise HTTPException(status_code=404, detail="Заказ не найден")
        
    cols = [desc[0] for desc in cursor.description]
    order_data = dict(zip(cols, order_row))
    
    cursor.execute('SELECT address, city, postal_code, phone FROM DeliveryData WHERE order_id = %s', (order_id,))
    delivery_row = cursor.fetchone()
    delivery_data = dict(zip([desc[0] for desc in cursor.description], delivery_row)) if delivery_row else None
    
    cursor.execute("""
        SELECT p.name, oi.quantity, oi.unit_price 
        FROM OrderItem oi JOIN Product p ON oi.product_id = p.product_id 
        WHERE oi.order_id = %s
    """, (order_id,))
    items = [{"name": r[0], "quantity": r[1], "unit_price": r[2]} for r in cursor.fetchall()]
    
    stream = generate_order_invoice_pdf(order_data, items, delivery_data)
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        stream,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=invoice_{order_id}.pdf"}
    )
    
@router.post("/import/products")
async def import_products(
    file: UploadFile = File(...),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency),
    _: UserResponse = Depends(get_current_admin_user)
):
    content = await file.read()
    filename = file.filename.lower()

    products_to_insert = []

    try:
        if filename.endswith('.json'):
            data = json.loads(content.decode('utf-8'))
            if not isinstance(data, list):
                raise ValueError("JSON должен содержать массив объектов")
            products_to_insert = data

        elif filename.endswith('.csv'):
            text = content.decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(text))
            products_to_insert = [row for row in reader]

        elif filename.endswith('.xml'):
            root = ET.fromstring(content)
            for prod_el in root.findall('Product'):
                prod_data = {}
                for child in prod_el:
                    prod_data[child.tag] = child.text
                products_to_insert.append(prod_data)
        else:
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат. Используйте CSV, JSON или XML.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка чтения файла: {str(e)}")

    cursor = conn.cursor()
    success_count = 0

    for p in products_to_insert:
        try:
            name = p.get('name')
            if not name:
                continue

            desc = p.get('description', '')
            brand = p.get('brand', '')
            car_model = p.get('car_model', '')
            category = p.get('category', '')
            price = float(p.get('price', 0))
            stock = int(p.get('stock_quantity', 0))
            img = p.get('image_url', '')
            is_active_raw = p.get('is_active', 1)
            is_active = is_active_raw in (1, '1', 'True', 'true', True)

            cursor.execute(
                """INSERT INTO Product (name, description, brand, car_model, category, price, stock_quantity, image_url, is_active)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (name, desc, brand, car_model, category, price, stock, img, is_active)
            )
            success_count += 1
        except Exception:
            continue

    conn.commit()
    return {"message": f"Успешно импортировано {success_count} товаров"}
