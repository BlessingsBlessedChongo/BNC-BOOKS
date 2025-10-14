<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Affiliate Dashboard</h1>
        <p class="mt-2 text-lg text-gray-600">Track your referrals and commissions</p>
      </div>

      <!-- Not Registered State -->
      <div v-if="!affiliateStore.affiliateInfo && !affiliateStore.isLoading" class="card p-8 text-center">
        <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
        <h2 class="mt-4 text-xl font-bold text-gray-900">Become an Affiliate</h2>
        <p class="mt-2 text-gray-600">Start earning commissions by referring customers to BNC Books.</p>
        <div class="mt-6">
          <button
            @click="openRegistrationModal"
            class="btn-primary"
          >
            Register as Affiliate
          </button>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="affiliateStore.error" class="mb-6 rounded-md bg-red-50 p-4">
        <div class="text-sm text-red-700">{{ affiliateStore.error }}</div>
      </div>

      <!-- Affiliate Content -->
      <div v-else-if="affiliateStore.affiliateInfo" class="space-y-8">
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Total Commissions -->
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Commissions</p>
                <p class="text-2xl font-bold text-gray-900">${{ analytics?.total_commissions?.toFixed(2) || '0.00' }}</p>
                <p v-if="analytics?.commission_growth" class="text-sm text-green-600">
                  +{{ analytics.commission_growth.toFixed(1) }}%
                </p>
              </div>
            </div>
          </div>

          <!-- Available Balance -->
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Available Balance</p>
                <p class="text-2xl font-bold text-gray-900">${{ analytics?.available_balance?.toFixed(2) || '0.00' }}</p>
              </div>
            </div>
          </div>

          <!-- Total Referrals -->
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Referrals</p>
                <p class="text-2xl font-bold text-gray-900">{{ analytics?.total_referrals || 0 }}</p>
              </div>
            </div>
          </div>

          <!-- Conversion Rate -->
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Conversion Rate</p>
                <p class="text-2xl font-bold text-gray-900">{{ analytics?.conversion_rate?.toFixed(1) || '0.0' }}%</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <button
            @click="openReferralModal"
            class="card p-6 text-center hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900">Create Referral Link</h3>
            <p class="mt-1 text-sm text-gray-600">Generate a new referral link</p>
          </button>

          <router-link 
            to="/affiliate/commissions" 
            class="card p-6 text-center hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900">View Commissions</h3>
            <p class="mt-1 text-sm text-gray-600">Track your earnings</p>
          </router-link>

          <button
            @click="openPayoutModal"
            class="card p-6 text-center hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900">Request Payout</h3>
            <p class="mt-1 text-sm text-gray-600">Withdraw your earnings</p>
          </button>
        </div>

        <!-- Recent Referral Links -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Recent Referral Links</h2>
          </div>
          <div class="p-6">
            <div v-if="affiliateStore.referralLinks.length === 0" class="text-center py-4">
              <p class="text-sm text-gray-500">No referral links created yet</p>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="link in affiliateStore.referralLinks.slice(0, 5)" 
                :key="link.id"
                class="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
              >
                <div>
                  <p class="font-medium text-primary-600">{{ link.url }}</p>
                  <p class="text-sm text-gray-600" v-if="link.campaign">Campaign: {{ link.campaign }}</p>
                  <div class="flex space-x-4 text-sm text-gray-500 mt-1">
                    <span>{{ link.clicks }} clicks</span>
                    <span>{{ link.conversions }} conversions</span>
                  </div>
                </div>
                <button
                  @click="copyToClipboard(link.url)"
                  class="text-primary-600 hover:text-primary-700 text-sm font-medium"
                >
                  Copy
                </button>
              </div>
            </div>
            <div class="mt-4 text-center">
              <button
                @click="openReferralModal"
                class="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                Create new link →
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Registration Modal -->
    <AffiliateRegistrationModal
      :isOpen="showRegistrationModal"
      @close="closeRegistrationModal"
      @registered="handleAffiliateRegistered"
    />

    <!-- Referral Link Modal -->
    <ReferralLinkModal
      :isOpen="showReferralModal"
      @close="closeReferralModal"
      @created="handleReferralCreated"
    />

    <!-- Payout Modal -->
    <PayoutModal
      :isOpen="showPayoutModal"
      :availableBalance="analytics?.available_balance || 0"
      @close="closePayoutModal"
      @requested="handlePayoutRequested"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import AppLayout from '../../layouts/AppLayout.vue';
import AffiliateRegistrationModal from '../../components/affiliate/AffiliateRegistrationModal.vue';
import ReferralLinkModal from '../../components/affiliate/ReferralLinkModal.vue';
import PayoutModal from '../../components/affiliate/PayoutModal.vue';
import { useAffiliateStore } from '../../stores/affiliate';

const affiliateStore = useAffiliateStore();

const showRegistrationModal = ref(false);
const showReferralModal = ref(false);
const showPayoutModal = ref(false);

const analytics = computed(() => affiliateStore.analytics);

const openRegistrationModal = () => {
  showRegistrationModal.value = true;
};

const closeRegistrationModal = () => {
  showRegistrationModal.value = false;
};

const openReferralModal = () => {
  if (!affiliateStore.affiliateInfo) {
    openRegistrationModal();
    return;
  }
  showReferralModal.value = true;
};

const closeReferralModal = () => {
  showReferralModal.value = false;
};

const openPayoutModal = () => {
  if (!affiliateStore.affiliateInfo) {
    openRegistrationModal();
    return;
  }
  showPayoutModal.value = true;
};

const closePayoutModal = () => {
  showPayoutModal.value = false;
};

const handleAffiliateRegistered = () => {
  affiliateStore.fetchAffiliateAnalytics();
  affiliateStore.fetchReferralLinks();
};

const handleReferralCreated = () => {
  affiliateStore.fetchReferralLinks();
};

const handlePayoutRequested = () => {
  affiliateStore.fetchAffiliateAnalytics();
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    // You could add a toast notification here
    alert('Referral link copied to clipboard!');
  } catch (err) {
    console.error('Failed to copy text: ', err);
  }
};

onMounted(async () => {
  if (affiliateStore.affiliateInfo) {
    await affiliateStore.fetchAffiliateAnalytics();
    await affiliateStore.fetchReferralLinks();
  }
});
</script>