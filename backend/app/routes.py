from fastapi import APIRouter, HTTPException
from app.models import CartItem, CheckoutRequest
from app.services import (
    add_item_to_cart_service,
    update_item_quantity_service,
    get_available_discount_codes_service,
    checkout_service,
    get_store_status_service,
    generate_discount_code_service,
)

router = APIRouter()


@router.get("/")
async def default():
    return {"message": "Welcome to e-com"}


@router.post("/cart/add")
async def add_to_cart(item: CartItem):
    try:
        return add_item_to_cart_service(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cart/update")
async def update_to_cart(item: CartItem):
    try:
        return update_item_quantity_service(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/discount/available")
async def get_available_discounts():
    try:
        return get_available_discount_codes_service()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/checkout")
async def checkout(checkout_request: CheckoutRequest = None):
    try:
        return checkout_service(checkout_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/admin/discount/generate")
async def generate_discount():
    try:
        return generate_discount_code_service()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/admin/status")
async def get_status():
    try:
        return get_store_status_service()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
