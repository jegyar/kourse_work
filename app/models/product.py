from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    brand: str
    car_model: Optional[str] = None
    category: str
    price: float
    stock_quantity: int
    image_url: Optional[str] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedProducts(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    size: int
