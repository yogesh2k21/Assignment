import {
  Drawer,
  ModalClose,
  Typography,
  Divider,
  List,
  ListItem,
  ListItemContent,
  ListItemDecorator,
  Avatar,
  IconButton,
  Input,
  Button,
  Stack,
  Box,
} from "@mui/joy";
import { useState, useEffect } from "react";
import { handleUpdateToCart, getAvailableDiscounts } from "../services/api";

export default function CartSidebar({
  isOpen,
  closeCart,
  cartItems,
  updateCart,
}) {
  const [discounts, setDiscounts] = useState([]);

  const updateQuantity = async (item) => {
    try {
      const payload = {
        item_id: item.id,
        name: item.name,
        quantity: item.newQuantity,
        price: item.price,
      };

      await handleUpdateToCart(payload);

      updateCart((prev) => {
        const existingItemIndex = prev.findIndex((el) => el.id === item.id);

        if (existingItemIndex !== -1) {
          if (item.newQuantity <= 0) {
            return prev.filter((el) => el.id !== item.id);
          } else {
            const updatedItems = [...prev];
            updatedItems[existingItemIndex] = {
              ...updatedItems[existingItemIndex],
              quantity: item.newQuantity,
            };
            return updatedItems;
          }
        }

        return prev;
      });
    } catch (error) {
      console.error("Failed to update quantity:", error);
    }
  };

  const total = cartItems?.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  useEffect(() => {
    const fetchDiscounts = async () => {
      try {
        const data = await getAvailableDiscounts();
        console.log(data)
        if (data && data?.codes.length > 0) {
          setDiscounts(data.codes);
        }
      } catch (error) {
        console.error("Failed to fetch discounts", error);
      }
    };

    fetchDiscounts(); // Only runs once on mount
  }, []);

  return (
    <Drawer
      open={isOpen}
      onClose={closeCart}
      anchor="right"
      size="md"
      slotProps={{
        content: {
          sx: {
            bgcolor: "background.surface",
            display: "flex",
            flexDirection: "column",
            height: "100%",
          },
        },
      }}
    >
      <Box sx={{ p: 2, display: "flex", alignItems: "center" }}>
        <Typography level="h5" component="h2" sx={{ flex: 1 }}>
          Your Cart
        </Typography>
        <ModalClose />
      </Box>
      <Divider />

      {cartItems.length === 0 ? (
        <Box sx={{ p: 4, textAlign: "center" }}>
          <Typography level="body1" color="neutral">
            Your cart is empty
          </Typography>
        </Box>
      ) : (
        <>
          <List sx={{ flex: 1, overflow: "auto" }}>
            {cartItems?.map((item) => (
              <ListItem key={item.id}>
                <ListItemDecorator>
                  <Avatar src={item.image} alt={item.name} />
                </ListItemDecorator>
                <ListItemContent sx={{ marginLeft: "8px" }}>
                  <Typography level="title-sm">{item.name}</Typography>
                  <Typography level="body-sm">
                    ${item.price.toFixed(2)}
                  </Typography>
                </ListItemContent>
                <Stack direction="row" spacing={1} alignItems="center">
                  <IconButton
                    size="sm"
                    variant="outlined"
                    onClick={() =>
                      updateQuantity({
                        ...item,
                        newQuantity: item.quantity - 1,
                      })
                    }
                  >
                    -
                  </IconButton>
                  <Input
                    value={item.quantity}
                    size="sm"
                    sx={{ width: "50px", textAlign: "center" }}
                    readOnly
                  />
                  <IconButton
                    size="sm"
                    variant="outlined"
                    onClick={() =>
                      updateQuantity({
                        ...item,
                        newQuantity: item.quantity + 1,
                      })
                    }
                  >
                    +
                  </IconButton>
                </Stack>
              </ListItem>
            ))}
          </List>

          <Divider />
          <Box sx={{ p: 2, display: "flex", flexDirection: "column", gap: 2 }}>
            {discounts.length > 0 && (
              <Box>
                <Typography level="body-sm" mb={1}>
                  Available Discounts
                </Typography>
                <Box
                  component="select"
                  sx={{
                    width: "100%",
                    p: 1.2,
                    borderRadius: "md",
                    border: "1px solid",
                    borderColor: "neutral.outlinedBorder",
                    fontSize: "sm",
                    color: "text.primary",
                    backgroundColor: "background.level1",
                    outline: "none",
                    "&:focus": {
                      borderColor: "primary.outlinedBorder",
                    },
                  }}
                >
                  <option value="">-- Select a Discount --</option>
                  {discounts.map((discount) => (
                    <option key={discount} value={discount}>
                      {discount}
                    </option>
                  ))}
                </Box>
              </Box>
            )}

            <Stack
              direction="row"
              justifyContent="space-between"
              alignItems="center"
            >
              <Typography level="title-md">Total:</Typography>
              <Typography level="title-lg">${total.toFixed(2)}</Typography>
            </Stack>

            <Button fullWidth size="lg" variant="solid" color="primary">
              Proceed to Checkout
            </Button>
          </Box>
        </>
      )}
    </Drawer>
  );
}
