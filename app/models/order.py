from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeliveryDataCreate(BaseModel):
    address: str
    city: str
    postal_code: str
    phone: str

class OrderCreate(BaseModel):
    delivery: DeliveryDataCreate
    payment_method: str = "card"

class OrderItemResponse(BaseModel):
    product_id: int
    name: str
    quantity: int
    unit_price: float

class OrderResponse(BaseModel):
    order_id: int
    total_amount: float
    discount_percent: float
    status: str
    currency: str
    created_at: datetime
    items: list[OrderItemResponse] = []
    
    class Config:
        from_attributes = True
