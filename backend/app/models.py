from pydantic import BaseModel

class Item(BaseModel):
    item_id: int
    name: str
    price: float

class CartItem(BaseModel):
    item_id: int
    quantity: int
    name: str
    price: float