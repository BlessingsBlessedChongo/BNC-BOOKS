import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../utils/api';

export const useCartStore = defineStore('cart', () => {
  const items = ref([]);
  const isLoading = ref(false);
  const error = ref('');

  // Load cart from localStorage on initialization
  const loadCartFromStorage = () => {
    const savedCart = localStorage.getItem('bnc_cart');
    if (savedCart) {
      try {
        items.value = JSON.parse(savedCart);
      } catch (e) {
        console.error('Failed to load cart from storage:', e);
        items.value = [];
      }
    }
  };

  // Save cart to localStorage
  const saveCartToStorage = () => {
    localStorage.setItem('bnc_cart', JSON.stringify(items.value));
  };

  // Getters
  const totalItems = computed(() => 
    items.value.reduce((total, item) => total + item.quantity, 0)
  );

  const subtotal = computed(() =>
    items.value.reduce((total, item) => total + (item.book.price * item.quantity), 0)
  );

  const shippingCost = computed(() => {
    // Free shipping over $50, otherwise $4.99
    return subtotal.value >= 50 ? 0 : 4.99;
  });

  const taxAmount = computed(() => {
    // 8.5% tax rate
    return subtotal.value * 0.085;
  });

  const totalAmount = computed(() =>
    subtotal.value + shippingCost.value + taxAmount.value
  );

  const hasItems = computed(() => items.value.length > 0);

  // Actions
  const fetchCart = async () => {
    if (!api.defaults.headers.common['Authorization']) {
      loadCartFromStorage();
      return;
    }

    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.get('/cart/');
      items.value = response.data.items || [];
      saveCartToStorage();
    } catch (error) {
      console.error('Failed to fetch cart:', error);
      // Fallback to local storage
      loadCartFromStorage();
    } finally {
      isLoading.value = false;
    }
  };

  const addToCart = async (book, quantity = 1) => {
    if (!book.stock_quantity || book.stock_quantity < quantity) {
      error.value = 'Not enough stock available';
      return false;
    }

    const existingItem = items.value.find(item => item.book.id === book.id);
    
    if (existingItem) {
      // Update quantity if item already in cart
      const newQuantity = existingItem.quantity + quantity;
      if (newQuantity > book.stock_quantity) {
        error.value = 'Requested quantity exceeds available stock';
        return false;
      }
      return await updateCartItem(existingItem.id, newQuantity);
    } else {
      // Add new item to cart
      if (api.defaults.headers.common['Authorization']) {
        return await addToCartAPI(book, quantity);
      } else {
        // Local cart for non-authenticated users
        items.value.push({
          id: Date.now(), // Temporary ID for local storage
          book,
          quantity,
          total_price: book.price * quantity,
          added_at: new Date().toISOString()
        });
        saveCartToStorage();
        return true;
      }
    }
  };

  const addToCartAPI = async (book, quantity) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.post('/cart/items/', {
        book: book.id,
        quantity
      });
      items.value.push(response.data);
      saveCartToStorage();
      return true;
    } catch (error) {
      console.error('Failed to add item to cart:', error);
      if (error.response?.data) {
        error.value = Object.values(error.response.data).flat().join(', ');
      } else {
        error.value = 'Failed to add item to cart';
      }
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const updateCartItem = async (itemId, quantity) => {
    if (quantity <= 0) {
      return await removeFromCart(itemId);
    }

    const item = items.value.find(item => item.id === itemId);
    if (!item) return false;

    if (quantity > item.book.stock_quantity) {
      error.value = 'Requested quantity exceeds available stock';
      return false;
    }

    if (api.defaults.headers.common['Authorization']) {
      return await updateCartItemAPI(itemId, quantity);
    } else {
      // Local update
      item.quantity = quantity;
      item.total_price = item.book.price * quantity;
      saveCartToStorage();
      return true;
    }
  };

  const updateCartItemAPI = async (itemId, quantity) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.patch(`/cart/items/${itemId}/`, {
        quantity
      });
      const index = items.value.findIndex(item => item.id === itemId);
      if (index !== -1) {
        items.value[index] = response.data;
      }
      saveCartToStorage();
      return true;
    } catch (error) {
      console.error('Failed to update cart item:', error);
      if (error.response?.data) {
        error.value = Object.values(error.response.data).flat().join(', ');
      } else {
        error.value = 'Failed to update cart item';
      }
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const removeFromCart = async (itemId) => {
    if (api.defaults.headers.common['Authorization']) {
      return await removeFromCartAPI(itemId);
    } else {
      // Local removal
      items.value = items.value.filter(item => item.id !== itemId);
      saveCartToStorage();
      return true;
    }
  };

  const removeFromCartAPI = async (itemId) => {
    isLoading.value = true;
    error.value = '';
    try {
      await api.delete(`/cart/items/${itemId}/`);
      items.value = items.value.filter(item => item.id !== itemId);
      saveCartToStorage();
      return true;
    } catch (error) {
      console.error('Failed to remove item from cart:', error);
      error.value = 'Failed to remove item from cart';
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const clearCart = async () => {
    if (api.defaults.headers.common['Authorization']) {
      isLoading.value = true;
      error.value = '';
      try {
        await api.delete('/cart/clear/');
        items.value = [];
        saveCartToStorage();
      } catch (error) {
        console.error('Failed to clear cart:', error);
        error.value = 'Failed to clear cart';
      } finally {
        isLoading.value = false;
      }
    } else {
      items.value = [];
      saveCartToStorage();
    }
  };

  const syncCartWithAPI = async () => {
    if (!api.defaults.headers.common['Authorization']) return;

    try {
      // Get current API cart
      const response = await api.get('/cart/');
      const apiCartItems = response.data.items || [];
      
      // Merge local cart with API cart
      const localItems = items.value.filter(item => !item.id || typeof item.id === 'number');
      
      for (const localItem of localItems) {
        const existingApiItem = apiCartItems.find(apiItem => 
          apiItem.book.id === localItem.book.id
        );
        
        if (existingApiItem) {
          // Update quantity in API
          const newQuantity = existingApiItem.quantity + localItem.quantity;
          await api.patch(`/cart/items/${existingApiItem.id}/`, {
            quantity: newQuantity
          });
        } else {
          // Add to API
          await api.post('/cart/items/', {
            book: localItem.book.id,
            quantity: localItem.quantity
          });
        }
      }
      
      // Reload cart from API
      await fetchCart();
    } catch (error) {
      console.error('Failed to sync cart with API:', error);
    }
  };

  // Initialize
  loadCartFromStorage();

  return {
    // State
    items,
    isLoading,
    error,
    
    // Getters
    totalItems,
    subtotal,
    shippingCost,
    taxAmount,
    totalAmount,
    hasItems,
    
    // Actions
    fetchCart,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
    syncCartWithAPI,
    clearError: () => error.value = ''
  };
});