import { CssVarsProvider } from "@mui/joy/styles";
import { CssBaseline, GlobalStyles } from "@mui/joy";
import { useState } from "react";
import Header from "./components/Header";
import CartSidebar from "./components/CartSidebar";
import Products from "./components/Products";

export default function App() {
  const [cartItems, setCartItems] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  const addToCart = (product) => {
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
