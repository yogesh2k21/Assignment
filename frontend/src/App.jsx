import { CssBaseline } from "@mui/joy";
import { useState } from "react";
import Header from "./components/Header";
import CartSidebar from "./components/CartSidebar";
import Products from "./components/Products";
import { handleAddToCart } from "./services/api";

export default function App() {
  const [cartItems, setCartItems] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  const addToCart = async (product) => {
    try {
      // Call the API to add the product to the cart
      const payload = {
        item_id:product.id,
        name:product.name,
        price:product.price,
        quantity:1
      }
      await handleAddToCart(payload);

      // Update the local state with the new product
      setCartItems((prev) => {
        const existingItem = prev.find((item) => item.id === product.id);
        return existingItem
          ? prev.map((item) =>
              item.id === product.id
                ? { ...item, quantity: item.quantity + 1 }
                : item
            )
          : [...prev, { ...product, quantity: 1 }];
      });
    } catch (error) {
      console.error('Failed to add to cart:', error);
    }
  };

  return (
    <>
      <CssBaseline />

      <Header
        cartCount={cartItems.reduce((sum, item) => sum + item.quantity, 0)}
        openCart={() => setIsCartOpen(true)}
      />

      <Products addToCart={addToCart} />

      {isCartOpen && (
        <CartSidebar
          isOpen={isCartOpen}
          closeCart={() => setIsCartOpen(false)}
          cartItems={cartItems}
          updateCart={setCartItems}
        />
      )}
    </>
  );
}
