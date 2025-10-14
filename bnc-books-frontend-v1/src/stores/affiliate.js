import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useAffiliateStore = defineStore('affiliate', () => {
  const affiliateInfo = ref(null)
  const referrals = ref([])
  const commissions = ref([])
  const analytics = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const filters = ref({
    period: '30d',
    status: '',
    type: ''
  })

  // Computed properties
  const referralStats = computed(() => {
    const stats = {
      total: referrals.value.length,
      pending: 0,
      approved: 0,
      converted: 0,
      total_commissions: 0,
      pending_commissions: 0,
      available_commissions: 0
    }

    referrals.value.forEach(referral => {
      stats[referral.status] = (stats[referral.status] || 0) + 1
      if (referral.status === 'converted') {
        stats.converted++
      }
    })

    commissions.value.forEach(commission => {
      if (commission.status === 'pending') {
        stats.pending_commissions += commission.amount
      } else if (commission.status === 'available') {
        stats.available_commissions += commission.amount
      }
      stats.total_commissions += commission.amount
    })

    return stats
  })

  const commissionStats = computed(() => {
    const stats = {
      total: commissions.value.length,
      pending: 0,
      available: 0,
      paid: 0,
      total_amount: 0,
      pending_amount: 0,
      available_amount: 0,
      paid_amount: 0
    }

    commissions.value.forEach(commission => {
      stats[commission.status] = (stats[commission.status] || 0) + 1
      stats[`${commission.status}_amount`] += commission.amount
      stats.total_amount += commission.amount
    })

    return stats
  })

  const filteredCommissions = computed(() => {
    let filtered = [...commissions.value]

    if (filters.value.status) {
      filtered = filtered.filter(commission => commission.status === filters.value.status)
    }

    if (filters.value.type) {
      filtered = filtered.filter(commission => commission.type === filters.value.type)
    }

    return filtered
  })

  // Affiliate actions
  const fetchAffiliateInfo = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get('/affiliate/info/')
      affiliateInfo.value = response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch affiliate info'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const registerAffiliate = async (affiliateData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post('/affiliate/register/', affiliateData)
      affiliateInfo.value = response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to register as affiliate'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateAffiliateSettings = async (settings) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.put('/affiliate/settings/', settings)
      affiliateInfo.value = { ...affiliateInfo.value, ...response.data }
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update affiliate settings'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Referral actions
  const fetchReferrals = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const queryParams = new URLSearchParams()
      if (params.status) queryParams.append('status', params.status)
      if (params.page) queryParams.append('page', params.page)

      const response = await api.get(`/affiliate/referrals/?${queryParams}`)
      referrals.value = response.data.results || response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch referrals'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const generateReferralLink = async (campaign = null) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post('/affiliate/referral-links/', {
        campaign: campaign
      })
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to generate referral link'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Commission actions
  const fetchCommissions = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const queryParams = new URLSearchParams()
      if (params.status) queryParams.append('status', params.status)
      if (params.type) queryParams.append('type', params.type)
      if (params.page) queryParams.append('page', params.page)

      const response = await api.get(`/affiliate/commissions/?${queryParams}`)
      commissions.value = response.data.results || response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch commissions'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const requestPayout = async (amount) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.post('/affiliate/payouts/', { amount })
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to request payout'
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
      const response = await api.get(`/affiliate/analytics/?period=${period}`)
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

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    affiliateInfo,
    referrals,
    commissions,
    analytics,
    isLoading,
    error,
    filters,
    
    // Computed
    referralStats,
    commissionStats,
    filteredCommissions,
    
    // Actions
    fetchAffiliateInfo,
    registerAffiliate,
    updateAffiliateSettings,
    fetchReferrals,
    generateReferralLink,
    fetchCommissions,
    requestPayout,
    fetchAnalytics,
    updateFilters,
    clearError
  }
})