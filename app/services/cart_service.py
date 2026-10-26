import psycopg2.extensions
from fastapi import HTTPException, status
from app.models.cart import CartItemCreate, CartItemUpdate, CartItemResponse, CartSummary

class CartService:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_cart(self, user_id: int) -> CartSummary:
        """Получить корзину пользователя."""
        self.cursor.execute(
            """
            SELECT c.cart_id, c.product_id, p.name, p.price, c.quantity, p.image_url, c.added_at
            FROM Cart c
            JOIN Product p ON c.product_id = p.product_id
            WHERE c.user_id = %s
            ORDER BY c.added_at DESC
            """,
            (user_id,)
        )
        rows = self.cursor.fetchall()

        items = []
        total = 0.0
        for row in rows:
            items.append(CartItemResponse(
                cart_id=row[0],
                product_id=row[1],
                name=row[2],
                price=float(row[3]),
                quantity=row[4],
                image_url=row[5],
                added_at=row[6]
            ))
            total += float(row[3]) * row[4]

        return CartSummary(items=items, total_amount=total)

    def add_to_cart(self, user_id: int, item: CartItemCreate) -> CartItemResponse:
        """Добавить товар в корзину."""
        # Проверить остатки товара
        self.cursor.execute("SELECT stock_quantity, is_active FROM Product WHERE product_id = %s", (item.product_id,))
        prod = self.cursor.fetchone()

        if not prod or not prod[1]:
            raise HTTPException(status_code=400, detail="Товар недоступен")

        # Проверить, есть ли уже этот товар в корзине
        self.cursor.execute("SELECT cart_id, quantity FROM Cart WHERE user_id = %s AND product_id = %s", (user_id, item.product_id))
        existing = self.cursor.fetchone()

        if existing:
            new_qty = existing[1] + item.quantity
            if new_qty > prod[0]:
                raise HTTPException(status_code=400, detail="Недостаточно товара на складе")

            self.cursor.execute("UPDATE Cart SET quantity = %s WHERE cart_id = %s", (new_qty, existing[0]))
        else:
            if item.quantity > prod[0]:
                raise HTTPException(status_code=400, detail="Недостаточно товара на складе")

            self.cursor.execute(
                "INSERT INTO Cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                (user_id, item.product_id, item.quantity)
            )

        self.conn.commit()
        return self.get_cart(user_id).items[0]

    def update_quantity(self, user_id: int, cart_id: int, item: CartItemUpdate) -> CartSummary:
        """Обновить количество товара в корзине."""
        if item.quantity <= 0:
            return self.remove_from_cart(user_id, cart_id)

        self.cursor.execute(
            """
            SELECT c.product_id, p.stock_quantity 
            FROM Cart c JOIN Product p ON c.product_id = p.product_id
            WHERE c.cart_id = %s AND c.user_id = %s
            """,
            (cart_id, user_id)
        )
        prod = self.cursor.fetchone()

        if not prod:
            raise HTTPException(status_code=404, detail="Товар в корзине не найден")

        if item.quantity > prod[1]:
            raise HTTPException(status_code=400, detail="Недостаточно товара на складе")

        self.cursor.execute("UPDATE Cart SET quantity = %s WHERE cart_id = %s", (item.quantity, cart_id))
        self.conn.commit()

        return self.get_cart(user_id)

    def remove_from_cart(self, user_id: int, cart_id: int) -> CartSummary:
        """Удалить товар из корзины."""
        self.cursor.execute("DELETE FROM Cart WHERE cart_id = %s AND user_id = %s", (cart_id, user_id))
        self.conn.commit()
        return self.get_cart(user_id)
