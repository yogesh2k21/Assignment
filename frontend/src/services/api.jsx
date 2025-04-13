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

const getAvailableDiscounts = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/discount/available`);
    return response.data;
  } catch (error) {
    console.error('Error fetching available discounts:', error);
    throw error;
  }
};

const checkout = async (discountCode) => {
  try {
    const response = await axios.post(`${BASE_URL}/checkout`, { discount_code: discountCode });
    return response.data;
  } catch (error) {
    console.error('Error during checkout:', error);
    throw error;
  }
};

export { handleAddToCart, handleUpdateToCart, getAvailableDiscounts,checkout };
