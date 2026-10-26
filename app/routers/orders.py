from fastapi import APIRouter, Depends
import psycopg2.extensions

from app.database import get_db_dependency
from app.models.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.models.user import UserResponse
from app.utils.security import get_current_user

router = APIRouter(
    prefix="/orders_api",
    tags=["Orders"]
)

@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    current_user: UserResponse = Depends(get_current_user),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency)
):
    service = OrderService(conn)
    return service.create_order(current_user.user_id, order_data)

@router.get("/", response_model=list[OrderResponse])
def get_orders(
    current_user: UserResponse = Depends(get_current_user),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency)
):
    service = OrderService(conn)
    return service.get_orders(current_user.user_id)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: UserResponse = Depends(get_current_user),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency)
):
    service = OrderService(conn)
    return service.get_order(current_user.user_id, order_id)
