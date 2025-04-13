from typing import Dict, List
from app.models import CartItem

# In-memory cart to store items using item_id as key
cart: Dict[int, CartItem] = {}

# Dictionary to store generated discount codes and their redeem status
# Format: {'CODE123': {'redeem': False}}
discount_codes: Dict[str, Dict[str, bool]] = {}

# List to store the history of all completed orders
order_history: List[Dict] = []

# Determines on which order a new discount code should be generated
nth_discount: int = 3

# Counter to track the number of successful orders placed
order_count: int = 0
