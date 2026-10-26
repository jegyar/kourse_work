from pydantic import BaseModel
from datetime import datetime

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    cart_id: int
    product_id: int
    name: str
    price: float
    quantity: int
    image_url: str | None
    added_at: datetime

    class Config:
        from_attributes = True

class CartSummary(BaseModel):
    items: list[CartItemResponse]
    total_amount: float
