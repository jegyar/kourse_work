-- ============================================================
-- Автоматизированная информационная система
-- управления интернет-магазином автозапчастей
-- DDL-скрипт: создание базы данных и таблиц (PostgreSQL)
-- ============================================================

-- Создание базы данных выполняется отдельно командой:
-- CREATE DATABASE autopartsdb;
-- \c autopartsdb

-- ============================================================
-- Таблица ролей
-- ============================================================
CREATE TABLE IF NOT EXISTS "Role" (
    role_id     SERIAL PRIMARY KEY,
    role_name   VARCHAR(50) NOT NULL UNIQUE
);

-- ============================================================
-- Таблица пользователей
-- ============================================================
CREATE TABLE IF NOT EXISTS "User" (
    user_id         SERIAL PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    role_id         INTEGER      NOT NULL DEFAULT 2,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),

    CONSTRAINT FK_User_Role FOREIGN KEY (role_id)
        REFERENCES "Role"(role_id)
);

CREATE INDEX IF NOT EXISTS IX_User_Email ON "User"(email);
CREATE INDEX IF NOT EXISTS IX_User_Role  ON "User"(role_id);

-- ============================================================
-- Таблица товаров (автозапчасти)
-- ============================================================
CREATE TABLE IF NOT EXISTS Product (
    product_id      SERIAL PRIMARY KEY,
    name            VARCHAR(255)   NOT NULL,
    description     TEXT           NULL,
    brand           VARCHAR(100)   NOT NULL,
    car_model       VARCHAR(100)   NULL,
    category        VARCHAR(100)   NOT NULL,
    price           NUMERIC(12,2)  NOT NULL CHECK (price >= 0),
    stock_quantity  INTEGER        NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    image_url       VARCHAR(500)   NULL,
    is_active       BOOLEAN        NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS IX_Product_Category ON Product(category);
CREATE INDEX IF NOT EXISTS IX_Product_Brand    ON Product(brand);
CREATE INDEX IF NOT EXISTS IX_Product_Active   ON Product(is_active);

-- ============================================================
-- Таблица корзины
-- ============================================================
CREATE TABLE IF NOT EXISTS Cart (
    cart_id     SERIAL PRIMARY KEY,
    user_id     INTEGER  NOT NULL,
    product_id  INTEGER  NOT NULL,
    quantity    INTEGER  NOT NULL DEFAULT 1 CHECK (quantity > 0),
    added_at    TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT FK_Cart_User    FOREIGN KEY (user_id)    REFERENCES "User"(user_id)  ON DELETE CASCADE,
    CONSTRAINT FK_Cart_Product FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    CONSTRAINT UQ_Cart_User_Product UNIQUE (user_id, product_id)
);

-- ============================================================
-- Таблица заказов
-- ============================================================
CREATE TABLE IF NOT EXISTS "Order" (
    order_id          SERIAL PRIMARY KEY,
    user_id           INTEGER        NOT NULL,
    total_amount      NUMERIC(14,2)  NOT NULL DEFAULT 0,
    discount_percent  NUMERIC(5,2)   NOT NULL DEFAULT 0
                      CHECK (discount_percent >= 0 AND discount_percent <= 100),
    status            VARCHAR(50)    NOT NULL DEFAULT 'new'
                      CHECK (status IN ('new', 'confirmed', 'processing',
                                        'shipped', 'delivered', 'cancelled')),
    currency          VARCHAR(10)    NOT NULL DEFAULT 'BYN',
    created_at        TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMP      NOT NULL DEFAULT NOW(),

    CONSTRAINT FK_Order_User FOREIGN KEY (user_id)
        REFERENCES "User"(user_id)
);

CREATE INDEX IF NOT EXISTS IX_Order_User   ON "Order"(user_id);
CREATE INDEX IF NOT EXISTS IX_Order_Status ON "Order"(status);

-- ============================================================
-- Таблица позиций заказа
-- ============================================================
CREATE TABLE IF NOT EXISTS OrderItem (
    order_item_id  SERIAL PRIMARY KEY,
    order_id       INTEGER       NOT NULL,
    product_id     INTEGER       NOT NULL,
    quantity       INTEGER       NOT NULL CHECK (quantity > 0),
    unit_price     NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),

    CONSTRAINT FK_OrderItem_Order   FOREIGN KEY (order_id)   REFERENCES "Order"(order_id)  ON DELETE CASCADE,
    CONSTRAINT FK_OrderItem_Product FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- ============================================================
-- Таблица транзакций (оплата)
-- ============================================================
CREATE TABLE IF NOT EXISTS "Transaction" (
    transaction_id  SERIAL PRIMARY KEY,
    order_id        INTEGER        NOT NULL,
    payment_method  VARCHAR(50)    NOT NULL
                    CHECK (payment_method IN ('card', 'cash', 'online', 'transfer')),
    amount          NUMERIC(14,2)  NOT NULL CHECK (amount >= 0),
    currency        VARCHAR(10)    NOT NULL DEFAULT 'BYN',
    status          VARCHAR(50)    NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
    paid_at         TIMESTAMP      NULL,

    CONSTRAINT FK_Transaction_Order FOREIGN KEY (order_id)
        REFERENCES "Order"(order_id) ON DELETE CASCADE
);

-- ============================================================
-- Таблица данных доставки
-- ============================================================
CREATE TABLE IF NOT EXISTS DeliveryData (
    delivery_id      SERIAL PRIMARY KEY,
    order_id         INTEGER        NOT NULL,
    address          VARCHAR(500)   NOT NULL,
    city             VARCHAR(100)   NOT NULL,
    postal_code      VARCHAR(20)    NOT NULL,
    phone            VARCHAR(30)    NOT NULL,
    delivery_status  VARCHAR(50)    NOT NULL DEFAULT 'pending'
                     CHECK (delivery_status IN ('pending', 'in_transit',
                                                'delivered', 'returned')),
    estimated_date   TIMESTAMP      NULL,
    delivered_at     TIMESTAMP      NULL,

    CONSTRAINT FK_Delivery_Order FOREIGN KEY (order_id)
        REFERENCES "Order"(order_id) ON DELETE CASCADE
);

-- Schema created successfully.
