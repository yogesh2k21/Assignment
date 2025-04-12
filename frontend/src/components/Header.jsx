import { IconButton, Badge, Typography, Sheet } from "@mui/joy";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";

export default function Header({ cartCount, openCart }) {
  return (
    <Sheet
      component="header"
      sx={{
        position: "fixed",
        top: 0,
        width: "100%",
        height: "50px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        px: 2,
        boxShadow: "sm",
        zIndex: 1000,
      }}
    >
      <Typography level="h4" component="h1" sx={{ color: "primary.500" }}>
        JoyMart
      </Typography>

      <IconButton
        variant="outlined"
        color="neutral"
        onClick={openCart}
        sx={{ borderRadius: "50%" }}
      >
        <Badge badgeContent={cartCount} color="danger" size="sm">
          <ShoppingCartIcon />
        </Badge>
      </IconButton>
    </Sheet>
  );
}
