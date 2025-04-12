from app.models import CartItem
from app import store

def add_item_to_cart_service(item: CartItem):
    if item.item_id in store.cart:
        store.cart[item.item_id].quantity += item.quantity
    else:
        store.cart[item.item_id] = item
    return {"message": f"{item.quantity} x {item.name} added to cart"}


def update_item_quantity_service(item: CartItem):
    if item.item_id in store.cart:
        # Update the quantity of the item
        store.cart[item.item_id].quantity = item.quantity
        # If the quantity becomes zero, remove the item from the cart
        if store.cart[item.item_id].quantity == 0:
            del store.cart[item.item_id]
            return {"message": f"{item.name} removed from cart"}
        else:
            return {"message": f"{item.name} quantity updated to {store.cart[item.item_id].quantity}"}
    else:
        return {"message": f"Item with ID {item.item_id} not found in cart"}
