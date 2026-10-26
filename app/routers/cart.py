from fastapi import APIRouter, Depends
import psycopg2.extensions

from app.database import get_db_dependency
from app.models.cart import CartItemCreate, CartItemUpdate, CartSummary
from app.services.cart_service import CartService
from app.models.user import UserResponse
from app.utils.security import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.get("/", response_model=CartSummary)
def get_cart(
    current_user: UserResponse = Depends(get_current_user),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency)
):
    service = CartService(conn)
    return service.get_cart(current_user.user_id)

@router.post("/", response_model=CartSummary)
def add_to_cart(
    item: CartItemCreate,
    current_user: UserResponse = Depends(get_current_user),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency)
):
    service = CartService(conn)
    service.add_to_cart(current_user.user_id, item)
    return service.get_cart(current_user.user_id)

@router.patch("/{cart_id}", response_model=CartSummary)
def update_cart_item(
    cart_id: int,
    item: CartItemUpdate,
    current_user: UserResponse = Depends(get_current_user),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency)
):
    service = CartService(conn)
    return service.update_quantity(current_user.user_id, cart_id, item)

@router.delete("/{cart_id}", response_model=CartSummary)
def remove_from_cart(
    cart_id: int,
    current_user: UserResponse = Depends(get_current_user),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency)
):
    service = CartService(conn)
    return service.remove_from_cart(current_user.user_id, cart_id)
