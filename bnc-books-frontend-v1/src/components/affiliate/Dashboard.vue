<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Affiliate Dashboard</h1>
      <p class="mt-2 text-lg text-gray-600">Track your referrals and earnings</p>
    </div>

    <!-- Not Registered Banner -->
    <div v-if="!affiliateStore.affiliateInfo && !showRegistration" class="card p-6 bg-primary-50 border-primary-200 mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium text-primary-800">Become an Affiliate</h3>
          <p class="mt-1 text-primary-700">
            Join our affiliate program and start earning commissions by referring customers to BNC Books.
          </p>
        </div>
        <button @click="showRegistration = true" class="btn-primary">
          Join Now
        </button>
      </div>
    </div>

    <!-- Registration Form -->
    <div v-if="showRegistration" class="card p-6 mb-8">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Affiliate Registration</h3>
      <AffiliateRegistration @registered="handleRegistrationComplete" />
    </div>

    <!-- Dashboard Content -->
    <div v-if="affiliateStore.affiliateInfo">
      <!-- Stats Overview -->
      <StatsOverview />

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <!-- Referral Links -->
        <div class="lg:col-span-2">
          <ReferralLinkGenerator />
        </div>

        <!-- Payout Request -->
        <div>
          <PayoutRequest />
        </div>
      </div>

      <!-- Analytics & Commissions -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Performance Metrics -->
        <div class="card p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Performance Metrics</h3>
          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Click-Through Rate</span>
              <span class="text-sm font-medium text-gray-900">
                {{ analytics?.click_through_rate?.toFixed(1) || '0.0' }}%
              </span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Conversion Rate</span>
              <span class="text-sm font-medium text-gray-900">
                {{ analytics?.conversion_rate?.toFixed(1) || '0.0' }}%
              </span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Average Commission</span>
              <span class="text-sm font-medium text-gray-900">
                ${{ analytics?.average_commission?.toFixed(2) || '0.00' }}
              </span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Total Clicks</span>
              <span class="text-sm font-medium text-gray-900">
                {{ analytics?.total_clicks || 0 }}
              </span>
            </div>
          </div>
        </div>

        <!-- Recent Referrals -->
        <div class="card p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900">Recent Referrals</h3>
            <router-link to="/affiliate/referrals" class="text-sm text-primary-600 hover:text-primary-500">
              View all
            </router-link>
          </div>
          
          <div v-if="recentReferrals.length === 0" class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
            </svg>
            <p class="mt-2 text-sm text-gray-600">No referrals yet</p>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="referral in recentReferrals"
              :key="referral.id"
              class="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
            >
              <div>
                <p class="text-sm font-medium text-gray-900">
                  {{ referral.user_email }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ formatDate(referral.created_at) }}
                </p>
              </div>
              <span class="badge" :class="getReferralStatusBadge(referral.status)">
                {{ formatReferralStatus(referral.status) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Commission Breakdown -->
        <div class="card p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Commission Breakdown</h3>
          <div class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Sales Commission</span>
              <span class="text-sm font-medium text-gray-900">
                ${{ commissionBreakdown.sales.toFixed(2) }}
              </span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Signup Bonus</span>
              <span class="text-sm font-medium text-gray-900">
                ${{ commissionBreakdown.signups.toFixed(2) }}
              </span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Performance Bonus</span>
              <span class="text-sm font-medium text-gray-900">
                ${{ commissionBreakdown.bonus.toFixed(2) }}
              </span>
            </div>
            <div class="border-t border-gray-200 pt-2 flex justify-between items-center">
              <span class="text-sm font-medium text-gray-900">Total</span>
              <span class="text-sm font-medium text-gray-900">
                ${{ commissionBreakdown.total.toFixed(2) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Commissions Table -->
      <div class="mt-8">
        <CommissionsTable />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAffiliateStore } from '@/stores/affiliate'
import StatsOverview from '@/components/affiliate/StatsOverview.vue'
import ReferralLinkGenerator from '@/components/affiliate/ReferralLinkGenerator.vue'
import PayoutRequest from '@/components/affiliate/PayoutRequest.vue'
import CommissionsTable from '@/components/affiliate/CommissionsTable.vue'
import AffiliateRegistration from '@/components/affiliate/AffiliateRegistration.vue'

const affiliateStore = useAffiliateStore()

const showRegistration = ref(false)

const analytics = computed(() => affiliateStore.analytics)

const recentReferrals = computed(() => affiliateStore.referrals.slice(0, 5))

const commissionBreakdown = computed(() => {
  const breakdown = {
    sales: 0,
    signups: 0,
    bonus: 0,
    total: 0
  }

  affiliateStore.commissions.forEach(commission => {
    breakdown[commission.type] += commission.amount
    breakdown.total += commission.amount
  })

  return breakdown
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}

const formatReferralStatus = (status) => {
  const statusMap = {
    pending: 'Pending',
    approved: 'Approved',
    converted: 'Converted',
    expired: 'Expired'
  }
  return statusMap[status] || status
}

const getReferralStatusBadge = (status) => {
  const statusClasses = {
    pending: 'badge-warning',
    approved: 'badge-info',
    converted: 'badge-success',
    expired: 'badge-error'
  }
  return statusClasses[status] || 'badge-secondary'
}

const handleRegistrationComplete = () => {
  showRegistration.value = false
  affiliateStore.fetchAffiliateInfo()
}

onMounted(async () => {
  await affiliateStore.fetchAffiliateInfo()
  if (affiliateStore.affiliateInfo) {
    await affiliateStore.fetchReferrals()
    await affiliateStore.fetchCommissions()
    await affiliateStore.fetchAnalytics()
  }
})
</script>

<style scoped>
.badge {
  @apply inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium;
}

.badge-warning {
  @apply bg-yellow-100 text-yellow-800;
}

.badge-info {
  @apply bg-blue-100 text-blue-800;
}

.badge-success {
  @apply bg-green-100 text-green-800;
}

.badge-error {
  @apply bg-red-100 text-red-800;
}

.badge-secondary {
  @apply bg-gray-100 text-gray-800;
}
</style>