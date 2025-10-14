import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useSellerStore = defineStore('seller', () => {
  const books = ref([])
  const currentBook = ref(null)
  const orders = ref([])
  const analytics = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const filters = ref({
    status: '',
    search: '',
    category: '',
    low_stock: false
  })

  // Computed properties
  const filteredBooks = computed(() => {
    let filtered = [...books.value]

    // Apply search filter
    if (filters.value.search) {
      const searchTerm = filters.value.search.toLowerCase()
      filtered = filtered.filter(book =>
        book.title.toLowerCase().includes(searchTerm) ||
        book.author.toLowerCase().includes(searchTerm) ||
        book.isbn.includes(searchTerm)
      )
    }

    // Apply category filter
    if (filters.value.category) {
      filtered = filtered.filter(book => book.category === filters.value.category)
    }

    // Apply low stock filter
    if (filters.value.low_stock) {
      filtered = filtered.filter(book => book.stock_quantity < 10)
    }

    return filtered
  })

  const bookStats = computed(() => {
    const stats = {
      total: books.value.length,
      published: 0,
      draft: 0,
      out_of_stock: 0,
      low_stock: 0,
      total_revenue: 0
    }

    books.value.forEach(book => {
      if (book.is_published) stats.published++
      else stats.draft++

      if (book.stock_quantity === 0) stats.out_of_stock++
      else if (book.stock_quantity < 10) stats.low_stock++

      stats.total_revenue += book.total_revenue || 0
    })

    return stats
  })

  const orderStats = computed(() => {
    const stats = {
      total: orders.value.length,
      pending: 0,
      processing: 0,
      shipped: 0,
      delivered: 0,
      cancelled: 0,
      total_revenue: 0
    }

    orders.value.forEach(order => {
      stats[order.status] = (stats[order.status] || 0) + 1
      if (order.status !== 'cancelled') {
        stats.total_revenue += order.total_amount
      }
    })

    return stats
  })

  // Book management actions
  const fetchBooks = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const queryParams = new URLSearchParams()
      if (params.status) queryParams.append('status', params.status)
      if (params.search) queryParams.append('search', params.search)
      if (params.page) queryParams.append('page', params.page)

      const response = await api.get(`/seller/books/?${queryParams}`)
      books.value = response.data.results || response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch books'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchBook = async (bookId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get(`/seller/books/${bookId}/`)
      currentBook.value = response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch book'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const createBook = async (bookData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post('/seller/books/', bookData)
      books.value.unshift(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to create book'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateBook = async (bookId, bookData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.put(`/seller/books/${bookId}/`, bookData)
      
      // Update local state
      const bookIndex = books.value.findIndex(book => book.id === bookId)
      if (bookIndex !== -1) {
        books.value[bookIndex] = response.data
      }
      if (currentBook.value && currentBook.value.id === bookId) {
        currentBook.value = response.data
      }
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update book'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const deleteBook = async (bookId) => {
    isLoading.value = true
    error.value = null
    
    try {
      await api.delete(`/seller/books/${bookId}/`)
      books.value = books.value.filter(book => book.id !== bookId)
      if (currentBook.value && currentBook.value.id === bookId) {
        currentBook.value = null
      }
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to delete book'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateInventory = async (bookId, stockData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.patch(`/seller/books/${bookId}/inventory/`, stockData)
      
      // Update local state
      const bookIndex = books.value.findIndex(book => book.id === bookId)
      if (bookIndex !== -1) {
        books.value[bookIndex].stock_quantity = response.data.stock_quantity
      }
      if (currentBook.value && currentBook.value.id === bookId) {
        currentBook.value.stock_quantity = response.data.stock_quantity
      }
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update inventory'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Order management actions
  const fetchOrders = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const queryParams = new URLSearchParams()
      if (params.status) queryParams.append('status', params.status)
      if (params.search) queryParams.append('search', params.search)
      if (params.page) queryParams.append('page', params.page)

      const response = await api.get(`/seller/orders/?${queryParams}`)
      orders.value = response.data.results || response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch orders'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateOrderStatus = async (orderId, status) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.patch(`/seller/orders/${orderId}/`, { status })
      
      // Update local state
      const orderIndex = orders.value.findIndex(order => order.id === orderId)
      if (orderIndex !== -1) {
        orders.value[orderIndex] = response.data
      }
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update order status'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Analytics actions
  const fetchAnalytics = async (period = '30d') => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get(`/seller/analytics/?period=${period}`)
      analytics.value = response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch analytics'
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
      search: '',
      category: '',
      low_stock: false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    books,
    currentBook,
    orders,
    analytics,
    isLoading,
    error,
    filters,
    
    // Computed
    filteredBooks,
    bookStats,
    orderStats,
    
    // Actions
    fetchBooks,
    fetchBook,
    createBook,
    updateBook,
    deleteBook,
    updateInventory,
    fetchOrders,
    updateOrderStatus,
    fetchAnalytics,
    updateFilters,
    clearFilters,
    clearError
  }
})