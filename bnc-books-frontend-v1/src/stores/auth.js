import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiMethods } from '@/utils/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('bnc_auth_token'))
  const refreshToken = ref(localStorage.getItem('bnc_refresh_token'))
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isSeller = computed(() => user.value?.role === 'seller')
  const isAffiliate = computed(() => user.value?.role === 'affiliate')
  const isBuyer = computed(() => user.value?.role === 'buyer')

  // Auth actions
  const login = async (credentials) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiMethods.login(credentials)
      
      user.value = response.user
      token.value = response.tokens.access
      refreshToken.value = response.tokens.refresh
      
      // Store in localStorage
      localStorage.setItem('bnc_auth_token', response.tokens.access)
      localStorage.setItem('bnc_refresh_token', response.tokens.refresh)
      localStorage.setItem('bnc_user_data', JSON.stringify(response.user))
      
      // Redirect based on role
      const redirectPath = getRoleRedirectPath(response.user.role)
      router.push(redirectPath)
      
      return { success: true, user: response.user }
    } catch (err) {
      error.value = err.response?.data?.error || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const register = async (userData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiMethods.register(userData)
      
      user.value = response.user
      token.value = response.tokens.access
      refreshToken.value = response.tokens.refresh
      
      // Store in localStorage
      localStorage.setItem('bnc_auth_token', response.tokens.access)
      localStorage.setItem('bnc_refresh_token', response.tokens.refresh)
      localStorage.setItem('bnc_user_data', JSON.stringify(response.user))
      
      // Redirect based on role
      const redirectPath = getRoleRedirectPath(response.user.role)
      router.push(redirectPath)
      
      return { success: true, user: response.user }
    } catch (err) {
      error.value = err.response?.data || 'Registration failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      if (token.value) {
        await apiMethods.logout()
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear local state regardless of API call success
      user.value = null
      token.value = null
      refreshToken.value = null
      localStorage.removeItem('bnc_auth_token')
      localStorage.removeItem('bnc_refresh_token')
      localStorage.removeItem('bnc_user_data')
      
      router.push('/login')
    }
  }

  const refreshToken = async () => {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }
    
    try {
      const response = await apiMethods.refreshToken(refreshToken.value)
      
      token.value = response.access
      localStorage.setItem('bnc_auth_token', response.access)
      
      return response.access
    } catch (err) {
      // Refresh failed, force logout
      logout()
      throw err
    }
  }

  const getProfile = async () => {
    try {
      const response = await apiMethods.getProfile()
      user.value = response
      localStorage.setItem('bnc_user_data', JSON.stringify(response))
      return response
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch profile'
      throw err
    }
  }

  const updateProfile = async (profileData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiMethods.updateProfile(profileData)
      user.value = response
      localStorage.setItem('bnc_user_data', JSON.stringify(response))
      return { success: true, user: response }
    } catch (err) {
      error.value = err.response?.data || 'Profile update failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const checkAuth = () => {
    const storedToken = localStorage.getItem('bnc_auth_token')
    const storedUser = localStorage.getItem('bnc_user_data')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
    }
  }

  const clearError = () => {
    error.value = null
  }

  // Helper function to get redirect path based on role
  const getRoleRedirectPath = (role) => {
    switch (role) {
      case 'seller':
        return '/seller'
      case 'affiliate':
        return '/affiliate'
      case 'buyer':
      default:
        return '/books'
    }
  }

  // Initialize auth state
  checkAuth()

  return {
    // State
    user,
    token,
    loading,
    error,
    
    // Computed
    isAuthenticated,
    isSeller,
    isAffiliate,
    isBuyer,
    
    // Actions
    login,
    register,
    logout,
    refreshToken,
    getProfile,
    updateProfile,
    checkAuth,
    clearError
  }
})