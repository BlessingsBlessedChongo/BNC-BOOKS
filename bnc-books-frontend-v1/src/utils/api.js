import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.token
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const authStore = useAuthStore()
        await authStore.refreshToken()
        
        // Retry the original request with new token
        const token = authStore.token
        originalRequest.headers.Authorization = `Bearer ${token}`
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh failed, redirect to login
        authStore.logout()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    // Handle other errors
    if (error.response?.status === 403) {
      console.error('Access forbidden')
    } else if (error.response?.status === 404) {
      console.error('Resource not found')
    } else if (error.response?.status >= 500) {
      console.error('Server error')
    }
    
    return Promise.reject(error)
  }
)

// API methods
export const apiMethods = {
  // Auth
  async login(credentials) {
    const response = await api.post('/auth/login/', credentials)
    return response.data
  },

  async register(userData) {
    const response = await api.post('/auth/register/', userData)
    return response.data
  },

  async refreshToken(refreshToken) {
    const response = await api.post('/auth/token/refresh/', { refresh: refreshToken })
    return response.data
  },

  async logout() {
    await api.post('/auth/logout/')
  },

  async getProfile() {
    const response = await api.get('/auth/profile/')
    return response.data
  },

  async updateProfile(profileData) {
    const response = await api.put('/auth/profile/', profileData)
    return response.data
  },

  // Books
  async getBooks(params = {}) {
    const response = await api.get('/books/', { params })
    return response.data
  },

  async getBook(bookId) {
    const response = await api.get(`/books/${bookId}/`)
    return response.data
  },

  async getFeaturedBooks() {
    const response = await api.get('/books/featured/')
    return response.data
  },

  async getCategories() {
    const response = await api.get('/books/categories/')
    return response.data
  },

  // Cart
  async getCart() {
    const response = await api.get('/cart/')
    return response.data
  },

  async addToCart(itemData) {
    const response = await api.post('/cart/items/', itemData)
    return response.data
  },

  async updateCartItem(itemId, quantity) {
    const response = await api.patch(`/cart/items/${itemId}/`, { quantity })
    return response.data
  },

  async removeFromCart(itemId) {
    await api.delete(`/cart/items/${itemId}/`)
  },

  async clearCart() {
    await api.delete('/cart/clear/')
  },

  // Orders
  async createOrder(orderData) {
    const response = await api.post('/orders/', orderData)
    return response.data
  },

  async getOrders(params = {}) {
    const response = await api.get('/orders/', { params })
    return response.data
  },

  async getOrder(orderId) {
    const response = await api.get(`/orders/${orderId}/`)
    return response.data
  },

  async cancelOrder(orderId) {
    const response = await api.post(`/orders/${orderId}/cancel/`)
    return response.data
  },

  // Reviews
  async createReview(reviewData) {
    const response = await api.post('/reviews/', reviewData)
    return response.data
  },

  async getReviews(params = {}) {
    const response = await api.get('/reviews/', { params })
    return response.data
  },

  async updateReview(reviewId, reviewData) {
    const response = await api.put(`/reviews/${reviewId}/`, reviewData)
    return response.data
  },

  async deleteReview(reviewId) {
    await api.delete(`/reviews/${reviewId}/`)
  },

  async checkCanReview(bookId) {
    const response = await api.get(`/reviews/can-review/${bookId}/`)
    return response.data
  },

  // Wishlist
  async getWishlist() {
    const response = await api.get('/wishlist/')
    return response.data
  },

  async addToWishlist(bookId) {
    const response = await api.post('/wishlist/items/', { book_id: bookId })
    return response.data
  },

  async removeFromWishlist(itemId) {
    await api.delete(`/wishlist/items/${itemId}/`)
  },

  async clearWishlist() {
    await api.delete('/wishlist/clear/')
  },

  // Notifications
  async getNotifications(params = {}) {
    const response = await api.get('/notifications/', { params })
    return response.data
  },

  async markNotificationAsRead(notificationId) {
    const response = await api.patch(`/notifications/${notificationId}/read/`)
    return response.data
  },

  async markAllNotificationsAsRead() {
    const response = await api.post('/notifications/mark-all-read/')
    return response.data
  },

  // Seller
  async getSellerBooks(params = {}) {
    const response = await api.get('/seller/books/', { params })
    return response.data
  },

  async createSellerBook(bookData) {
    const response = await api.post('/seller/books/', bookData)
    return response.data
  },

  async updateSellerBook(bookId, bookData) {
    const response = await api.put(`/seller/books/${bookId}/`, bookData)
    return response.data
  },

  async updateInventory(bookId, inventoryData) {
    const response = await api.patch(`/seller/books/${bookId}/inventory/`, inventoryData)
    return response.data
  },

  async getSellerOrders(params = {}) {
    const response = await api.get('/seller/orders/', { params })
    return response.data
  },

  async updateOrderStatus(orderId, statusData) {
    const response = await api.patch(`/seller/orders/${orderId}/`, statusData)
    return response.data
  },

  async getSellerAnalytics(params = {}) {
    const response = await api.get('/seller/analytics/', { params })
    return response.data
  },

  // Affiliate
  async registerAffiliate(affiliateData) {
    const response = await api.post('/affiliate/register/', affiliateData)
    return response.data
  },

  async generateReferralLink(campaignData) {
    const response = await api.post('/affiliate/referral-links/', campaignData)
    return response.data
  },

  async getCommissions(params = {}) {
    const response = await api.get('/affiliate/commissions/', { params })
    return response.data
  },

  async requestPayout(payoutData) {
    const response = await api.post('/affiliate/payouts/', payoutData)
    return response.data
  },

  async getAffiliateAnalytics(params = {}) {
    const response = await api.get('/affiliate/analytics/', { params })
    return response.data
  }
}

export default api