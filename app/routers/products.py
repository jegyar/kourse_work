from fastapi import APIRouter, Depends, Query
import psycopg2.extensions
from typing import Optional

from app.database import get_db_dependency
from app.models.product import ProductResponse, PaginatedProducts
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=PaginatedProducts)
def get_products(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    car_model: Optional[str] = None,
    sort_by: str = Query("product_id"),
    sort_desc: bool = Query(False),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency)
):
    """Получить список товаров (с фильтрацией и пагинацией)."""
    skip = (page - 1) * size
    product_service = ProductService(conn)
    return product_service.get_products(
        skip=skip,
        limit=size,
        search=search,
        category=category,
        brand=brand,
        car_model=car_model,
        sort_by=sort_by,
        sort_desc=sort_desc
    )


@router.get("/categories", response_model=list[str])
def get_categories(conn: psycopg2.extensions.connection = Depends(get_db_dependency)):
    """Получить список доступных категорий."""
    product_service = ProductService(conn)
    return product_service.get_categories()


@router.get("/brands", response_model=list[str])
def get_brands(conn: psycopg2.extensions.connection = Depends(get_db_dependency)):
    """Получить список доступных брендов."""
    product_service = ProductService(conn)
    return product_service.get_brands()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, conn: psycopg2.extensions.connection = Depends(get_db_dependency)):
    """Получить информацию о конкретном товаре по ID."""
    product_service = ProductService(conn)
    return product_service.get_product(product_id)
