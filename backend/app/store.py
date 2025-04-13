from typing import Dict, List
from app.models import CartItem

cart: Dict[int, CartItem] = {}
discount_codes: Dict[str, Dict[str, bool]] = {} # {'DISC-235F9DBA': {'redeem': False}}
order_history: List[Dict] = []
nth_discount: int = 3
order_count: int = 0