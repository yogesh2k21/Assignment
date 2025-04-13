from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    item_id: int
    name: str
    price: float

class CartItem(BaseModel):
    item_id: int
    quantity: int
    name: str
    price: float

class CheckoutRequest(BaseModel):
    discount_code: Optional[str] = None

class CheckoutResponse(BaseModel):
    total_amount: float
    discount_applied: bool = False

class DiscountCodeResponse(BaseModel):
    code: str

class StatsResponse(BaseModel):
    total_items_purchased: int
    total_purchase_amount: float
    discount_codes: list[dict]
    total_discount_amount: float