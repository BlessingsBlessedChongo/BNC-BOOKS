import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import api from '../utils/api';

export const useOrdersStore = defineStore('orders', () => {
  const orders = ref([]);
  const currentOrder = ref(null);
  const isLoading = ref(false);
  const error = ref('');
  const filters = reactive({
    status: '',
    page: 1,
    page_size: 10
  });
  const pagination = reactive({
    count: 0,
    next: null,
    previous: null,
    total_pages: 0,
    current_page: 1
  });

  // Actions
  const fetchOrders = async (params = {}) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.get('/orders/', { 
        params: { ...filters, ...params } 
      });
      orders.value = response.data.results;
      Object.assign(pagination, {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        total_pages: response.data.total_pages,
        current_page: response.data.current_page || 1
      });
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch orders';
      console.error('Failed to fetch orders:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const fetchOrderById = async (orderId) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.get(`/orders/${orderId}/`);
      currentOrder.value = response.data;
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch order details';
      console.error('Failed to fetch order:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const cancelOrder = async (orderId) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.post(`/orders/${orderId}/cancel/`);
      // Update the order in the list
      const orderIndex = orders.value.findIndex(order => order.id === orderId);
      if (orderIndex !== -1) {
        orders.value[orderIndex] = response.data;
      }
      // Update current order if it's the one being viewed
      if (currentOrder.value && currentOrder.value.id === orderId) {
        currentOrder.value = response.data;
      }
      return response.data;
    } catch (err) {
      error.value = 'Failed to cancel order';
      console.error('Failed to cancel order:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const requestReturn = async (orderId, returnData) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.post(`/orders/${orderId}/return/`, returnData);
      // Update the order in the list
      const orderIndex = orders.value.findIndex(order => order.id === orderId);
      if (orderIndex !== -1) {
        orders.value[orderIndex].return_requested = true;
      }
      // Update current order if it's the one being viewed
      if (currentOrder.value && currentOrder.value.id === orderId) {
        currentOrder.value.return_requested = true;
      }
      return response.data;
    } catch (err) {
      error.value = 'Failed to request return';
      console.error('Failed to request return:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateFilters = (newFilters) => {
    Object.assign(filters, newFilters);
  };

  const clearError = () => {
    error.value = '';
  };

  return {
    // State
    orders,
    currentOrder,
    isLoading,
    error,
    filters,
    pagination,
    
    // Actions
    fetchOrders,
    fetchOrderById,
    cancelOrder,
    requestReturn,
    updateFilters,
    clearError
  };
});