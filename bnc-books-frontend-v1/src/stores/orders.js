import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useOrderStore = defineStore('orders', () => {
  const orders = ref([])
  const currentOrder = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const filters = ref({
    status: '',
    date_from: '',
    date_to: '',
    search: ''
  })

  // Computed properties
  const filteredOrders = computed(() => {
    let filtered = [...orders.value]

    // Apply status filter
    if (filters.value.status) {
      filtered = filtered.filter(order => order.status === filters.value.status)
    }

    // Apply date range filter
    if (filters.value.date_from) {
      const fromDate = new Date(filters.value.date_from)
      filtered = filtered.filter(order => new Date(order.created_at) >= fromDate)
    }

    if (filters.value.date_to) {
      const toDate = new Date(filters.value.date_to)
      filtered = filtered.filter(order => new Date(order.created_at) <= toDate)
    }

    // Apply search filter
    if (filters.value.search) {
      const searchTerm = filters.value.search.toLowerCase()
      filtered = filtered.filter(order =>
        order.order_number.toLowerCase().includes(searchTerm) ||
        order.items.some(item =>
          item.book.title.toLowerCase().includes(searchTerm) ||
          item.book.author.toLowerCase().includes(searchTerm)
        )
      )
    }

    return filtered
  })

  const orderStats = computed(() => {
    const stats = {
      total: orders.value.length,
      pending: 0,
      processing: 0,
      shipped: 0,
      delivered: 0,
      cancelled: 0,
      total_spent: 0
    }

    orders.value.forEach(order => {
      stats[order.status] = (stats[order.status] || 0) + 1
      if (order.status !== 'cancelled') {
        stats.total_spent += order.total_amount
      }
    })

    return stats
  })

  // Actions
  const fetchOrders = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const queryParams = new URLSearchParams()
      if (params.status) queryParams.append('status', params.status)
      if (params.page) queryParams.append('page', params.page)
      if (params.page_size) queryParams.append('page_size', params.page_size)

      const response = await api.get(`/orders/?${queryParams}`)
      orders.value = response.data.results || response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch orders'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchOrder = async (orderId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get(`/orders/${orderId}/`)
      currentOrder.value = response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch order'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const cancelOrder = async (orderId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post(`/orders/${orderId}/cancel/`)
      
      // Update local state
      const orderIndex = orders.value.findIndex(order => order.id === orderId)
      if (orderIndex !== -1) {
        orders.value[orderIndex] = response.data
      }
      if (currentOrder.value && currentOrder.value.id === orderId) {
        currentOrder.value = response.data
      }
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to cancel order'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const requestReturn = async (orderId, returnData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post(`/orders/${orderId}/return/`, returnData)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to request return'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
  }

  const clearFilters = () => {
    filters.value = {
      status: '',
      date_from: '',
      date_to: '',
      search: ''
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    orders,
    currentOrder,
    isLoading,
    error,
    filters,
    
    // Computed
    filteredOrders,
    orderStats,
    
    // Actions
    fetchOrders,
    fetchOrder,
    cancelOrder,
    requestReturn,
    updateFilters,
    clearFilters,
    clearError
  }
})