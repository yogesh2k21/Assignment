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

export default function CartSidebar({
  isOpen,
  closeCart,
  cartItems,
  updateCart,
}) {
  const updateQuantity = (id, newQuantity) => {
    if (newQuantity < 1) {
      // Remove the item from the cart if the new quantity is less than 1
      updateCart((prev) => prev.filter((item) => item.id !== id));
    } else {
      // Update the quantity of the item in the cart
      updateCart((prev) =>
        prev.map((item) =>
          item.id === id ? { ...item, quantity: newQuantity } : item
        )
      );
    }
  };

  const total = cartItems?.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

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
                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
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
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  >
                    +
                  </IconButton>
                </Stack>
              </ListItem>
            ))}
          </List>

          <Divider />
          <Box sx={{ p: 2 }}>
            <Stack direction="row" justifyContent="space-between" mb={2}>
              <Typography level="title-md">Total:</Typography>
              <Typography level="title-lg">${total.toFixed(2)}</Typography>
            </Stack>
            <Button fullWidth size="lg">
              Proceed to Checkout
            </Button>
          </Box>
        </>
      )}
    </Drawer>
  );
}
