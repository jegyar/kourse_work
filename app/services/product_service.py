import psycopg2.extensions
from typing import Optional
from fastapi import HTTPException, status
from app.models.product import ProductResponse, PaginatedProducts


class ProductService:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_products(
        self,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        car_model: Optional[str] = None,
        sort_by: str = "product_id",
        sort_desc: bool = False
    ) -> PaginatedProducts:
        """Получение списка товаров с фильтрацией, поиском и пагинацией."""

        # Разрешенные столбцы для сортировки (защита от SQL-инъекций)
        allowed_sort_cols = ["product_id", "name", "price", "created_at"]
        if sort_by not in allowed_sort_cols:
            sort_by = "product_id"

        order = "DESC" if sort_desc else "ASC"

        # Построение WHERE clause
        where_clauses = ["is_active = TRUE"]
        params = []

        if search:
            words = [w.strip() for w in search.split() if w.strip()]
            for word in words:
                where_clauses.append("(name ILIKE %s OR brand ILIKE %s OR car_model ILIKE %s)")
                search_term = f"%{word}%"
                params.extend([search_term, search_term, search_term])

        if category:
            where_clauses.append("category = %s")
            params.append(category)

        if brand:
            where_clauses.append("brand = %s")
            params.append(brand)

        if car_model:
            where_clauses.append("car_model ILIKE %s")
            params.append(f"%{car_model}%")

        where_sql = " AND ".join(where_clauses)

        # Получение общего количества для пагинации
        count_sql = f"SELECT COUNT(*) FROM Product WHERE {where_sql}"
        self.cursor.execute(count_sql, params)
        total_count = self.cursor.fetchone()[0]

        # Получение данных (PostgreSQL использует LIMIT/OFFSET)
        sql = f"""
            SELECT product_id, name, description, brand, car_model, 
                   category, price, stock_quantity, image_url, is_active, created_at
            FROM Product
            WHERE {where_sql}
            ORDER BY {sort_by} {order}
            LIMIT %s OFFSET %s
        """

        # Добавляем параметры пагинации в конец
        query_params = params + [limit, skip]

        self.cursor.execute(sql, query_params)
        rows = self.cursor.fetchall()

        items = []
        for row in rows:
            items.append(
                ProductResponse(
                    product_id=row[0],
                    name=row[1],
                    description=row[2],
                    brand=row[3],
                    car_model=row[4],
                    category=row[5],
                    price=float(row[6]),
                    stock_quantity=row[7],
                    image_url=row[8],
                    is_active=row[9],
                    created_at=row[10]
                )
            )

        page = (skip // limit) + 1 if limit > 0 else 1

        return PaginatedProducts(
            items=items,
            total=total_count,
            page=page,
            size=limit
        )

    def get_product(self, product_id: int) -> ProductResponse:
        """Получение товара по ID."""
        self.cursor.execute(
            """
            SELECT product_id, name, description, brand, car_model, 
                   category, price, stock_quantity, image_url, is_active, created_at
            FROM Product
            WHERE product_id = %s AND is_active = TRUE
            """,
            (product_id,)
        )
        row = self.cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )

        return ProductResponse(
            product_id=row[0],
            name=row[1],
            description=row[2],
            brand=row[3],
            car_model=row[4],
            category=row[5],
            price=float(row[6]),
            stock_quantity=row[7],
            image_url=row[8],
            is_active=row[9],
            created_at=row[10]
        )

    def get_categories(self) -> list[str]:
        """Получение списка всех уникальных категорий."""
        self.cursor.execute("SELECT DISTINCT category FROM Product WHERE is_active = TRUE ORDER BY category")
        return [row[0] for row in self.cursor.fetchall()]

    def get_brands(self) -> list[str]:
        """Получение списка всех уникальных брендов."""
        self.cursor.execute("SELECT DISTINCT brand FROM Product WHERE is_active = TRUE ORDER BY brand")
        return [row[0] for row in self.cursor.fetchall()]
