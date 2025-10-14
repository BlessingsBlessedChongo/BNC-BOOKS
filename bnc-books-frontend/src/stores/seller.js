import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import api from '../utils/api';

export const useSellerStore = defineStore('seller', () => {
  const sellerBooks = ref([]);
  const sellerOrders = ref([]);
  const analytics = ref(null);
  const isLoading = ref(false);
  const error = ref('');
  
  const bookFilters = reactive({
    page: 1,
    page_size: 10,
    search: '',
    is_published: ''
  });
  
  const orderFilters = reactive({
    page: 1,
    page_size: 10,
    status: ''
  });
  
  const pagination = reactive({
    count: 0,
    next: null,
    previous: null,
    total_pages: 0,
    current_page: 1
  });

  // Book Management Actions
  const fetchSellerBooks = async (params = {}) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.get('/seller/books/', { 
        params: { ...bookFilters, ...params } 
      });
      sellerBooks.value = response.data.results;
      Object.assign(pagination, {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        total_pages: response.data.total_pages,
        current_page: response.data.current_page || 1
      });
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch books';
      console.error('Failed to fetch seller books:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const createBook = async (bookData) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.post('/seller/books/', bookData);
      sellerBooks.value.unshift(response.data);
      return response.data;
    } catch (err) {
      if (err.response?.data) {
        error.value = Object.values(err.response.data).flat().join(', ');
      } else {
        error.value = 'Failed to create book';
      }
      console.error('Failed to create book:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateBook = async (bookId, bookData) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.put(`/seller/books/${bookId}/`, bookData);
      const index = sellerBooks.value.findIndex(book => book.id === bookId);
      if (index !== -1) {
        sellerBooks.value[index] = response.data;
      }
      return response.data;
    } catch (err) {
      if (err.response?.data) {
        error.value = Object.values(err.response.data).flat().join(', ');
      } else {
        error.value = 'Failed to update book';
      }
      console.error('Failed to update book:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const deleteBook = async (bookId) => {
    isLoading.value = true;
    error.value = '';
    try {
      await api.delete(`/seller/books/${bookId}/`);
      sellerBooks.value = sellerBooks.value.filter(book => book.id !== bookId);
      pagination.count -= 1;
      return true;
    } catch (err) {
      error.value = 'Failed to delete book';
      console.error('Failed to delete book:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateInventory = async (bookId, inventoryData) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.patch(`/seller/books/${bookId}/inventory/`, inventoryData);
      const index = sellerBooks.value.findIndex(book => book.id === bookId);
      if (index !== -1) {
        sellerBooks.value[index] = { ...sellerBooks.value[index], ...response.data };
      }
      return response.data;
    } catch (err) {
      if (err.response?.data) {
        error.value = Object.values(err.response.data).flat().join(', ');
      } else {
        error.value = 'Failed to update inventory';
      }
      console.error('Failed to update inventory:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Order Management Actions
  const fetchSellerOrders = async (params = {}) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.get('/seller/orders/', { 
        params: { ...orderFilters, ...params } 
      });
      sellerOrders.value = response.data.results;
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch orders';
      console.error('Failed to fetch seller orders:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateOrderStatus = async (orderId, statusData) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.patch(`/seller/orders/${orderId}/`, statusData);
      const index = sellerOrders.value.findIndex(order => order.id === orderId);
      if (index !== -1) {
        sellerOrders.value[index] = response.data;
      }
      return response.data;
    } catch (err) {
      if (err.response?.data) {
        error.value = Object.values(err.response.data).flat().join(', ');
      } else {
        error.value = 'Failed to update order status';
      }
      console.error('Failed to update order status:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Analytics Actions
  const fetchAnalytics = async (period = '30d') => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.get('/seller/analytics/', { 
        params: { period } 
      });
      analytics.value = response.data;
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch analytics';
      console.error('Failed to fetch analytics:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateBookFilters = (newFilters) => {
    Object.assign(bookFilters, newFilters);
  };

  const updateOrderFilters = (newFilters) => {
    Object.assign(orderFilters, newFilters);
  };

  const clearError = () => {
    error.value = '';
  };

  return {
    // State
    sellerBooks,
    sellerOrders,
    analytics,
    isLoading,
    error,
    bookFilters,
    orderFilters,
    pagination,
    
    // Book Actions
    fetchSellerBooks,
    createBook,
    updateBook,
    deleteBook,
    updateInventory,
    
    // Order Actions
    fetchSellerOrders,
    updateOrderStatus,
    
    // Analytics Actions
    fetchAnalytics,
    
    // Utility Actions
    updateBookFilters,
    updateOrderFilters,
    clearError
  };
});