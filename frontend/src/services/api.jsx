import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

const handleAddToCart = async (product) => {
  try {
    const result = await axios.post(`${BASE_URL}/cart/add`, product);
    return result.data;
  } catch (error) {
    console.error('Failed to add to cart:', error);
    throw error;
  }
};

const handleUpdateToCart = async (product) => {
  try {
    const result = await axios.post(`${BASE_URL}/cart/update`, product);
    return result.data;
  } catch (error) {
    console.error('Failed to update to cart:', error);
    throw error;
  }
};

export { handleAddToCart, handleUpdateToCart };
