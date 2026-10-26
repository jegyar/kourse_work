import psycopg2.extensions
from fastapi import HTTPException, status
from app.models.order import OrderCreate, OrderResponse, OrderItemResponse
from app.services.cart_service import CartService

class OrderService:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.cart_service = CartService(conn)

    def create_order(self, user_id: int, order_data: OrderCreate) -> OrderResponse:
        """Оформление заказа из корзины."""
        # Получаем корзину
        cart = self.cart_service.get_cart(user_id)
        if not cart.items:
            raise HTTPException(status_code=400, detail="Корзина пуста")

        try:
            # 1. Создаем заказ и получаем его ID через RETURNING
            self.cursor.execute(
                'INSERT INTO "Order" (user_id, total_amount) VALUES (%s, %s) RETURNING order_id',
                (user_id, cart.total_amount)
            )
            order_id = self.cursor.fetchone()[0]

            # 2. Добавляем товары, списываем остатки
            for item in cart.items:
                # Списание остатков
                self.cursor.execute(
                    "UPDATE Product SET stock_quantity = stock_quantity - %s WHERE product_id = %s AND stock_quantity >= %s",
                    (item.quantity, item.product_id, item.quantity)
                )
                if self.cursor.rowcount == 0:
                    raise Exception(f"Товар {item.name} закончился или недоступен в нужном количестве")

                # Добавление позиции заказа
                self.cursor.execute(
                    "INSERT INTO OrderItem (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                    (order_id, item.product_id, item.quantity, item.price)
                )

            # 3. Данные доставки
            self.cursor.execute(
                """
                INSERT INTO DeliveryData (order_id, address, city, postal_code, phone)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (order_id, order_data.delivery.address, order_data.delivery.city,
                 order_data.delivery.postal_code, order_data.delivery.phone)
            )

            # 4. Транзакция
            self.cursor.execute(
                'INSERT INTO "Transaction" (order_id, payment_method, amount) VALUES (%s, %s, %s)',
                (order_id, order_data.payment_method, cart.total_amount)
            )

            # 5. Очистка корзины
            self.cursor.execute("DELETE FROM Cart WHERE user_id = %s", (user_id,))

            self.conn.commit()
            return self.get_order(user_id, order_id)

        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def get_orders(self, user_id: int) -> list[OrderResponse]:
        """Получить все заказы пользователя."""
        self.cursor.execute(
            """
            SELECT order_id, total_amount, discount_percent, status, currency, created_at
            FROM "Order"
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )
        orders = []
        for row in self.cursor.fetchall():
            orders.append(OrderResponse(
                order_id=row[0],
                total_amount=float(row[1]),
                discount_percent=float(row[2]),
                status=row[3],
                currency=row[4],
                created_at=row[5]
            ))
        return orders

    def get_order(self, user_id: int, order_id: int) -> OrderResponse:
        """Получить детали конкретного заказа."""
        self.cursor.execute(
            'SELECT order_id, total_amount, discount_percent, status, currency, created_at FROM "Order" WHERE order_id = %s AND user_id = %s',
            (order_id, user_id)
        )
        row = self.cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Заказ не найден")

        order = OrderResponse(
            order_id=row[0],
            total_amount=float(row[1]),
            discount_percent=float(row[2]),
            status=row[3],
            currency=row[4],
            created_at=row[5]
        )

        self.cursor.execute(
            """
            SELECT oi.product_id, p.name, oi.quantity, oi.unit_price
            FROM OrderItem oi
            JOIN Product p ON oi.product_id = p.product_id
            WHERE oi.order_id = %s
            """,
            (order_id,)
        )
        items = []
        for i_row in self.cursor.fetchall():
            items.append(OrderItemResponse(
                product_id=i_row[0],
                name=i_row[1],
                quantity=i_row[2],
                unit_price=float(i_row[3])
            ))
        order.items = items
        return order
