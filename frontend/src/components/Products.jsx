import { Card, Grid, Typography, Button, AspectRatio } from "@mui/joy";

const products = [
  {
    id: 1,
    name: "Pot",
    price: 10,
    image:
      "https://images.unsplash.com/photo-1509423350716-97f9360b4e09?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fHBvdHxlbnwwfHwwfHx8MA%3D%3D",
  },
  {
    id: 2,
    name: "IPhone",
    price: 20,
    image:
      "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cGhvbmV8ZW58MHx8MHx8fDA%3D",
  },
  {
    id: 3,
    name: "AMD Ryzen 9",
    price: 30,
    image:
      "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y3B1fGVufDB8fDB8fHww",
  },
  {
    id: 4,
    name: "PS5",
    price: 40,
    image:
      "https://images.unsplash.com/photo-1605296830714-7c02e14957ac?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8cHM1fGVufDB8fDB8fHww",
  },
  {
    id: 5,
    name: "i Pad",
    price: 50,
    image:
      "https://images.unsplash.com/photo-1542751110-97427bbecf20?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fGlwYWR8ZW58MHx8MHx8fDA%3D",
  },
  {
    id: 6,
    name: "HeadPhone",
    price: 60,
    image:
      "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8aGVhZHBob25lfGVufDB8fDB8fHww",
  },
  {
    id: 7,
    name: "TV",
    price: 70,
    image:
      "https://images.unsplash.com/photo-1717295248230-93ea71f48f92?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHR2fGVufDB8fDB8fHww",
  },
  {
    id: 8,
    name: "Bottle",
    price: 80,
    image:
      "https://images.unsplash.com/photo-1589365278144-c9e705f843ba?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Ym90dGxlfGVufDB8fDB8fHww",
  },
];

export default function Products({ addToCart }) {
  return (
    <Grid
      container
      spacing={3}
      sx={{
        padding: "60px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        overflowX: "hidden",
        width:'100%',
        marginTop:3
      }}
    >
      {products?.map((product) => (
        <Grid
          item
          xs={12}
          sm={6}
          md={4}
          lg={3}
          key={product.id}
          sx={{ display: "flex" }}
        >
          <Card
            variant="outlined"
            sx={{
              height: "100%",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              flex: 1,
            }}
          >
            <AspectRatio ratio="4/3" sx={{ flex: "1 1 auto" }}>
              <img
                src={product.image}
                alt={product.name}
                loading="lazy"
                style={{ objectFit: "cover", width: "100%", height: "100%" }}
              />
            </AspectRatio>
            <Typography level="h6" component="h3" mt={1}>
              {product.name}
            </Typography>
            <Typography level="body1" mb={2}>
              ${product.price.toFixed(2)}
            </Typography>
            <Button
              fullWidth
              onClick={() => addToCart(product)}
              sx={{ mt: "auto" }}
            >
              Add to Cart
            </Button>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}
