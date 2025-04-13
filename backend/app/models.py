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
