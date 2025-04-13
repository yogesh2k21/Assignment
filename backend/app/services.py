from app.models import (
    CartItem,
    CheckoutRequest,
    CheckoutResponse,
    DiscountCodeResponse,
    StatsResponse,
)
from app import store
from app.utility import generate_discount_code


# Add an item to the cart
def add_item_to_cart_service(item: CartItem):
    if item.item_id in store.cart:
        store.cart[item.item_id].quantity += item.quantity
    else:
        store.cart[item.item_id] = item
    return {"message": f"{item.quantity} {item.name} added to cart"}


# Update the quantity of an item in the cart
def update_item_quantity_service(item: CartItem):
    if item.item_id in store.cart:
        store.cart[item.item_id].quantity = item.quantity
        if store.cart[item.item_id].quantity == 0:
            # Remove item if quantity is 0
            del store.cart[item.item_id]
            return {"message": f"{item.name} removed from cart"}
        else:
            return {
                "message": f"{item.name} quantity updated to {store.cart[item.item_id].quantity}"
            }
    else:
        return {"message": f"Item with ID {item.item_id} not found in cart"}


# Get all unused discount codes
def get_available_discount_codes_service():
    available_codes = [
        code
        for code, details in store.discount_codes.items()
        if not details.get("redeem", False)
    ]
    return {"codes": available_codes}


# Handles the checkout process
def checkout_service(checkout_request: CheckoutRequest = None):
    total_amount = sum(item.price * item.quantity for item in store.cart.values())
    discount_applied = False
    discount_amount = 0.0

    # Apply discount if a valid discount code is provided
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

    # Increment order count and save order history
    store.order_count += 1
    store.order_history.append(
        {
            "items": list(store.cart.values()),
            "total_amount": total_amount + discount_amount,  # Original total
            "discount_applied": discount_applied,
            "discount_code": (
                checkout_request.discount_code if checkout_request else None
            ),
            "discount_amount": discount_amount,
        }
    )

    # Generate discount code if the *next* order will qualify for it
    if (store.order_count + 1) % store.nth_discount == 0:
        new_code = generate_discount_code()
        store.discount_codes[new_code] = {"redeem": False}

    store.cart.clear()
    return CheckoutResponse(
        total_amount=total_amount, discount_applied=discount_applied
    )


# Generate a discount code if the next order qualifies
def generate_discount_code_service():
    next_order_number = store.order_count + 1
    if next_order_number % store.nth_discount == 0:
        new_code = generate_discount_code()
        store.discount_codes[new_code] = {"redeem": False}
        return DiscountCodeResponse(code=new_code)
    else:
        remaining = store.nth_discount - (next_order_number % store.nth_discount)
        return {
            "message": f"No discount code generated. Next discount available after {remaining} more order(s)."
        }


# Get current store status like stats
def get_store_status_service():
    total_items_ordered = sum(
        item.quantity for order in store.order_history for item in order["items"]
    )
    total_purchase_amount = sum(order["total_amount"] for order in store.order_history)
    discount_codes = [{code: status} for code, status in store.discount_codes.items()]
    total_discount_amount = sum(
        order["discount_amount"] for order in store.order_history
    )

    return StatsResponse(
        total_items_purchased=total_items_ordered,
        total_purchase_amount=total_purchase_amount,
        discount_codes=discount_codes,
        total_discount_amount=total_discount_amount,
    )
