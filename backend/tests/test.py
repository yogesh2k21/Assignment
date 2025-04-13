from fastapi.testclient import TestClient
from app.main import app
from app import store
from app.models import CartItem
from app.services import (
    get_available_discount_codes_service,
    update_item_quantity_service,
)

client = TestClient(app)


def test_add_to_cart():
    # Clear the cart to start with a clean state
    store.cart.clear()

    # Send a POST request to the /cart/add endpoint with item details
    response = client.post(
        "/cart/add",
        json={"item_id": 1, "quantity": 5, "name": "Test Item", "price": 50},
    )

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that the response JSON matches the expected message
    assert response.json() == {"message": "5 Test Item added to cart"}

    # Confirm that the item is correctly added to the store's cart with the specified quantity
    assert store.cart[1].quantity == 5



def test_update_item_quantity_service():
    # Clear cart before test
    store.cart.clear()

    # Add an item to the cart manually
    item = CartItem(item_id=101, name="Test Product", price=20.0, quantity=2)
    store.cart[item.item_id] = item

    # 1. Update item quantity to 5
    update_item = CartItem(item_id=101, name="Test Product", price=20.0, quantity=5)
    response = update_item_quantity_service(update_item)
    assert response["message"] == "Test Product quantity updated to 5"
    assert store.cart[101].quantity == 5

    # 2. Update item quantity to 0 (should remove item)
    update_item.quantity = 0
    response = update_item_quantity_service(update_item)
    assert response["message"] == "Test Product removed from cart"
    assert 101 not in store.cart

    # 3. Try updating non-existing item
    missing_item = CartItem(item_id=999, name="Missing", price=10.0, quantity=3)
    response = update_item_quantity_service(missing_item)
    assert response["message"] == "Item with ID 999 not found in cart"


def test_checkout_no_discount():
    # Clear the cart and order history to start with a clean state
    store.cart.clear()
    store.order_history.clear()
    store.order_count = 0

    # Add an item to the cart before proceeding to checkout
    client.post(
        "/cart/add",
        json={"item_id": 1, "quantity": 1, "name": "Test Item", "price": 20.0},
    )

    # Send a POST request to the /checkout endpoint
    response = client.post("/checkout")

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that the total amount in the response is correct
    assert response.json()["total_amount"] == 20.0

    # Ensure that no discount was applied
    assert not response.json()["discount_applied"]

    # Confirm that the cart is empty after checkout
    assert len(store.cart) == 0

    # Verify that the order history has been updated with the new order
    assert len(store.order_history) == 1

    # Check that the order count has been incremented
    assert store.order_count == 1



def test_checkout_with_valid_discount():
    # Clear the cart, order history, and discount codes to start with a clean state
    store.cart.clear()
    store.order_history.clear()
    store.discount_codes.clear()
    store.order_count = 0

    # Simulate generating a discount code and mark it as not redeemed
    store.discount_codes["TESTCODE"] = {"redeem": False}

    # Add an item to the cart before proceeding to checkout
    client.post(
        "/cart/add",
        json={"item_id": 2, "quantity": 1, "name": "Another Item", "price": 50.0},
    )

    # Send a POST request to the /checkout endpoint with a discount code
    response = client.post("/checkout", json={"discount_code": "TESTCODE"})

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that the total amount in the response is correct after applying the discount
    assert response.json()["total_amount"] == 45

    # Ensure that the discount code has been marked as redeemed
    assert store.discount_codes["TESTCODE"]["redeem"] is True

    # Confirm that the cart is empty after checkout
    assert len(store.cart) == 0

    # Verify that the order history has been updated with the new order
    assert len(store.order_history) == 1

    # Check that the order count has been incremented
    assert store.order_count == 1



def test_checkout_with_invalid_discount():
    # Clear the cart to start with a clean state
    store.cart.clear()

    # Add an item to the cart before proceeding to checkout
    client.post(
        "/cart/add",
        json={"item_id": 3, "quantity": 1, "name": "Item", "price": 30.0},
    )

    # Send a POST request to the /checkout endpoint with an invalid discount code
    response = client.post("/checkout", json={"discount_code": "bdzfb"})

    # Check that the response status code is 400 (Bad Request)
    assert response.status_code == 400

    # Verify that the response JSON contains the expected error message
    assert response.json() == {"detail": "Invalid or redeemed discount code"}

    # Clear the cart again to ensure the test ends with a clean state
    store.cart.clear()

    # Confirm that the cart is empty after the test
    assert len(store.cart) == 0



def test_generate_discount_on_nth_order():
    # Clear any existing discount codes to start with a clean state
    store.discount_codes.clear()

    # Set the initial order count to simulate previous orders
    store.order_count = 1

    # Add an item to the cart before proceeding to checkout
    client.post(
        "/cart/add",
        json={"item_id": 4, "quantity": 1, "name": "Final Item", "price": 100.0},
    )

    # Perform a checkout to trigger the nth order discount generation
    response = client.post("/checkout")

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Verify that a discount code has been generated
    assert len(store.discount_codes) == 1

    # Ensure that the order count is incremented correctly,
    # and it is one less than the nth discount threshold
    assert store.order_count == store.nth_discount - 1



def test_get_stats():
    # Reset the store state before the test to ensure a clean starting point
    store.cart.clear()
    store.order_history.clear()
    store.discount_codes.clear()
    store.order_count = 0

    # Simulate the first order
    client.post(
        "/cart/add",
        json={"item_id": 1, "quantity": 1, "name": "Stat Item 1", "price": 10.0},
    )
    client.post("/checkout")

    # Simulate the second order
    client.post(
        "/cart/add",
        json={"item_id": 2, "quantity": 2, "name": "Stat Item 2", "price": 5.0},
    )
    client.post("/checkout")

    # Manually simulate a discounted order (third order)
    store.discount_codes["XYZ"] = {"redeem": True}
    store.order_count += 1
    store.order_history.append(
        {
            "items": [CartItem(item_id=2, quantity=2, name="Stat Item 2", price=5.0)],
            "total_amount": 10.0,
            "discount_applied": True,
            "discount_code": "XYZ",
            "discount_amount": 1.0,
        }
    )

    # Call the status endpoint to retrieve statistics
    response = client.get("/admin/status")

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the response JSON to get the stats
    stats = response.json()

    # Verify that the total number of items purchased is at least 3
    assert stats["total_items_purchased"] >= 3

    # Verify that the total purchase amount is at least 20.0
    assert stats["total_purchase_amount"] >= 20.0

    # Check that the discount code "XYZ" is present in the discount codes list
    assert any("XYZ" in d for d in stats["discount_codes"])

    # Verify that the total discount amount is at least 1.0
    assert stats["total_discount_amount"] >= 1.0



# Mock the generate_discount_code function
def generate_discount_code():
    return "NEW-DISCOUNT-CODE"


def test_get_available_discount_codes_service():
    # Clear any existing discount codes to start with a clean state
    store.discount_codes.clear()

    # Set up test data in the in-memory store
    # Add both available and redeemed discount codes
    store.discount_codes["DISC-AVAILABLE-1"] = {"redeem": False}
    store.discount_codes["DISC-REDEEMED-1"] = {"redeem": True}
    store.discount_codes["DISC-AVAILABLE-2"] = {"redeem": False}
    store.discount_codes["DISC-REDEEMED-2"] = {"redeem": True}

    # Call the service function to get available discount codes
    result = get_available_discount_codes_service()

    # Assert that the result is a dictionary
    assert isinstance(result, dict), "The result should be a dictionary"

    # Check that the result contains a 'codes' key
    assert "codes" in result, "The result should contain a 'codes' key"

    # Verify that 'codes' is a list
    assert isinstance(result["codes"], list), "'codes' should be a list"

    # Ensure that only available discount codes are included in the result
    assert "DISC-AVAILABLE-1" in result["codes"], "DISC-AVAILABLE-1 should be in the result"
    assert "DISC-AVAILABLE-2" in result["codes"], "DISC-AVAILABLE-2 should be in the result"

    # Ensure that redeemed discount codes are not included in the result
    assert "DISC-REDEEMED-1" not in result["codes"], "DISC-REDEEMED-1 should not be in the result"
    assert "DISC-REDEEMED-2" not in result["codes"], "DISC-REDEEMED-2 should not be in the result"

    # Verify the number of available discount codes
    assert len(result["codes"]) == 2, "There should be exactly 2 available discount codes"
