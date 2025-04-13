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

# Create API router instance
router = APIRouter()


# Root endpoint to confirm the service is running
@router.get("/")
async def default():
    return {"message": "Welcome to e-com"}


# Endpoint to add an item to the cart
@router.post("/cart/add")
async def add_to_cart(item: CartItem):
    try:
        return add_item_to_cart_service(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint to update item quantity in the cart (or remove if quantity is zero)
@router.post("/cart/update")
async def update_to_cart(item: CartItem):
    try:
        return update_item_quantity_service(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint to fetch all available (unredeemed) discount codes
@router.get("/discount/available")
async def get_available_discounts():
    try:
        return get_available_discount_codes_service()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Checkout endpoint that calculates total and applies discount if valid
@router.post("/checkout")
async def checkout(checkout_request: CheckoutRequest = None):
    try:
        return checkout_service(checkout_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Admin-only endpoint to generate a discount code manually (if eligible)
@router.post("/admin/discount/generate")
async def generate_discount():
    try:
        return generate_discount_code_service()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Admin-only endpoint to get current stats: orders, discounts, totals
@router.get("/admin/status")
async def get_status():
    try:
        return get_store_status_service()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
