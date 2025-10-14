import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useWishlistStore = defineStore('wishlist', () => {
  const wishlistItems = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const wishlistCount = computed(() => wishlistItems.value.length)
  const isInWishlist = computed(() => (bookId) => {
    return wishlistItems.value.some(item => item.book.id === bookId)
  })

  // Actions
  const fetchWishlist = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/wishlist/')
      wishlistItems.value = response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch wishlist'
      console.error('Wishlist fetch error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  

  const addToWishlist = async (bookId) => {
    try {
      const response = await api.post('/wishlist/items/', {
        book_id: bookId
      })
      
      // Add to local state
      wishlistItems.value.push(response.data)
      
      return response.data
    } catch (err) {
      console.error('Add to wishlist error:', err)
      throw err
    }
  }

  const removeFromWishlist = async (wishlistItemId) => {
    try {
      await api.delete(`/wishlist/items/${wishlistItemId}/`)
      
      // Remove from local state
      wishlistItems.value = wishlistItems.value.filter(item => item.id !== wishlistItemId)
    } catch (err) {
      console.error('Remove from wishlist error:', err)
      throw err
    }
  }

  const clearWishlist = async () => {
    try {
      await api.delete('/wishlist/clear/')
      
      // Clear local state
      wishlistItems.value = []
    } catch (err) {
      console.error('Clear wishlist error:', err)
      throw err
    }
  }
  

  const toggleWishlist = async (bookId) => {
    const existingItem = wishlistItems.value.find(item => item.book.id === bookId)
    
    if (existingItem) {
      await removeFromWishlist(existingItem.id)
      return false
    } else {
      await addToWishlist(bookId)
      return true
    }
  }

  return {
    // State
    wishlistItems,
    loading,
    error,
    
    // Computed
    wishlistCount,
    isInWishlist,
    
    // Actions
    fetchWishlist,
    addToWishlist,
    removeFromWishlist,
    clearWishlist,
    toggleWishlist
  }
}, {
  persist: {
    key: 'bnc-wishlist',
    storage: localStorage
  }
})