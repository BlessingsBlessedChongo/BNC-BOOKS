import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useReviewStore = defineStore('reviews', () => {
  const reviews = ref([])
  const userReviews = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  // Computed properties
  const reviewStats = computed(() => {
    const stats = {
      total: reviews.value.length,
      average_rating: 0,
      rating_distribution: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
    }

    if (stats.total > 0) {
      let totalRating = 0
      reviews.value.forEach(review => {
        totalRating += review.rating
        stats.rating_distribution[review.rating]++
      })
      stats.average_rating = totalRating / stats.total
    }

    return stats
  })

  // Actions
  const fetchReviews = async (bookId = null) => {
    isLoading.value = true
    error.value = null
    
    try {
      const url = bookId ? `/reviews/?book=${bookId}` : '/reviews/'
      const response = await api.get(url)
      reviews.value = response.data.results || response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch reviews'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchUserReviews = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get('/reviews/my-reviews/')
      userReviews.value = response.data.results || response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch user reviews'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const createReview = async (reviewData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post('/reviews/', reviewData)
      
      // Add to local state
      reviews.value.unshift(response.data)
      userReviews.value.unshift(response.data)
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to create review'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateReview = async (reviewId, reviewData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.put(`/reviews/${reviewId}/`, reviewData)
      
      // Update local state
      const reviewIndex = reviews.value.findIndex(review => review.id === reviewId)
      if (reviewIndex !== -1) {
        reviews.value[reviewIndex] = response.data
      }
      
      const userReviewIndex = userReviews.value.findIndex(review => review.id === reviewId)
      if (userReviewIndex !== -1) {
        userReviews.value[userReviewIndex] = response.data
      }
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update review'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const deleteReview = async (reviewId) => {
    isLoading.value = true
    error.value = null
    
    try {
      await api.delete(`/reviews/${reviewId}/`)
      
      // Remove from local state
      reviews.value = reviews.value.filter(review => review.id !== reviewId)
      userReviews.value = userReviews.value.filter(review => review.id !== reviewId)
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to delete review'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const canReviewBook = async (bookId) => {
    try {
      const response = await api.get(`/reviews/can-review/${bookId}/`)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data?.message }
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    reviews,
    userReviews,
    isLoading,
    error,
    
    // Computed
    reviewStats,
    
    // Actions
    fetchReviews,
    fetchUserReviews,
    createReview,
    updateReview,
    deleteReview,
    canReviewBook,
    clearError
  }
})