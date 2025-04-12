from fastapi import APIRouter
from app.models import (
    CartItem
)
from app.services import (
    add_item_to_cart_service,
    update_item_quantity_service
)

router = APIRouter()


@router.get("/")
async def default():
    return {"message": "Welcome to e-com"}


@router.post("/cart/add")
async def add_to_cart(item: CartItem):
    return add_item_to_cart_service(item)


@router.post("/cart/update")
async def update_to_cart(item: CartItem):
    return update_item_quantity_service(item)
