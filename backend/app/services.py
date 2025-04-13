from app.models import CartItem, CheckoutRequest, CheckoutResponse
from app import store
from app.utility import generate_discount_code


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
            return {
                "message": f"{item.name} quantity updated to {store.cart[item.item_id].quantity}"
            }
    else:
        return {"message": f"Item with ID {item.item_id} not found in cart"}


def get_available_discount_codes_service():
    available_codes = [
        code
        for code, details in store.discount_codes.items()
        if not details.get("redeem", False)
    ]
    return {"codes": available_codes}


def checkout_service(checkout_request: CheckoutRequest = None):
    print(store.cart)
    total_amount = sum(item.price * item.quantity for item in store.cart.values())
    discount_applied = False
    discount_amount = 0.0

    if checkout_request and checkout_request.discount_code:
        discount_code = checkout_request.discount_code.upper()
        if (
            discount_code in store.discount_codes
            and not store.discount_codes[discount_code]["redeem"]
        ):
            discount_amount = total_amount * 0.1
            total_amount -= discount_amount
            store.discount_codes[discount_code]["redeem"] = True
            discount_applied = True
        else:
            raise ValueError("Invalid or redeemed discount code")

    store.order_count += 1
    store.order_history.append(
        {
            "items": list(store.cart.values()),
            "total_amount": total_amount
            + discount_amount,  # Store original total before discount
            "discount_applied": discount_applied,
            "discount_code": (
                checkout_request.discount_code if checkout_request else None
            ),
            "discount_amount": discount_amount,
        }
    )

    # Check if next order (order_count + 1) is eligible for discount
    # means if order is 2 generate code so that is will be visible for order 3
    if (store.order_count + 1) % store.nth_discount == 0:
        new_code = generate_discount_code()
        store.discount_codes[new_code] = {"redeem": False}

    store.cart.clear()
    return CheckoutResponse(
        total_amount=total_amount, discount_applied=discount_applied
    )
