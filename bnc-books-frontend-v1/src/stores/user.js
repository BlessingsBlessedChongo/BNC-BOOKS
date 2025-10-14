import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useUserStore = defineStore('user', () => {
  const profile = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  const fetchProfile = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get('/users/profile/')
      profile.value = response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch profile'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateProfile = async (profileData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.put('/users/profile/', profileData)
      profile.value = response.data
      
      // Update user in localStorage
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      const updatedUser = { ...user, ...response.data }
      localStorage.setItem('user', JSON.stringify(updatedUser))
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update profile'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const changePassword = async (passwordData) => {
    isLoading.value = true
    error.value = null
    
    try {
      await api.post('/auth/password/change/', passwordData)
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to change password'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    profile,
    isLoading,
    error,
    fetchProfile,
    updateProfile,
    changePassword,
    clearError
  }
})