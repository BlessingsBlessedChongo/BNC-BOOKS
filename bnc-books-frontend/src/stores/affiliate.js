import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import api from '../utils/api';

export const useAffiliateStore = defineStore('affiliate', () => {
  const affiliateInfo = ref(null);
  const referralLinks = ref([]);
  const commissions = ref([]);
  const analytics = ref(null);
  const isLoading = ref(false);
  const error = ref('');
  
  const commissionFilters = reactive({
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

  // Affiliate Registration
  const registerAffiliate = async (affiliateData) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.post('/affiliate/register/', affiliateData);
      affiliateInfo.value = response.data;
      return response.data;
    } catch (err) {
      if (err.response?.data) {
        error.value = Object.values(err.response.data).flat().join(', ');
      } else {
        error.value = 'Failed to register as affiliate';
      }
      console.error('Failed to register affiliate:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Referral Links
  const generateReferralLink = async (campaignData) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.post('/affiliate/referral-links/', campaignData);
      referralLinks.value.unshift(response.data);
      return response.data;
    } catch (err) {
      if (err.response?.data) {
        error.value = Object.values(err.response.data).flat().join(', ');
      } else {
        error.value = 'Failed to generate referral link';
      }
      console.error('Failed to generate referral link:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const fetchReferralLinks = async () => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.get('/affiliate/referral-links/');
      referralLinks.value = response.data.results;
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch referral links';
      console.error('Failed to fetch referral links:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Commissions
  const fetchCommissions = async (params = {}) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.get('/affiliate/commissions/', { 
        params: { ...commissionFilters, ...params } 
      });
      commissions.value = response.data.results;
      Object.assign(pagination, {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        total_pages: response.data.total_pages,
        current_page: response.data.current_page || 1
      });
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch commissions';
      console.error('Failed to fetch commissions:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Payouts
  const requestPayout = async (payoutData) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.post('/affiliate/payouts/', payoutData);
      return response.data;
    } catch (err) {
      if (err.response?.data) {
        error.value = Object.values(err.response.data).flat().join(', ');
      } else {
        error.value = 'Failed to request payout';
      }
      console.error('Failed to request payout:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Analytics
  const fetchAffiliateAnalytics = async (period = '30d') => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await api.get('/affiliate/analytics/', { 
        params: { period } 
      });
      analytics.value = response.data;
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch affiliate analytics';
      console.error('Failed to fetch affiliate analytics:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateCommissionFilters = (newFilters) => {
    Object.assign(commissionFilters, newFilters);
  };

  const clearError = () => {
    error.value = '';
  };

  return {
    // State
    affiliateInfo,
    referralLinks,
    commissions,
    analytics,
    isLoading,
    error,
    commissionFilters,
    pagination,
    
    // Actions
    registerAffiliate,
    generateReferralLink,
    fetchReferralLinks,
    fetchCommissions,
    requestPayout,
    fetchAffiliateAnalytics,
    updateCommissionFilters,
    clearError
  };
});