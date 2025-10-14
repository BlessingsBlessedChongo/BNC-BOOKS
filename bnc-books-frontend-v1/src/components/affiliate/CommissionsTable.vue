<template>
  <div class="card">
    <!-- Table Header -->
    <div class="px-6 py-4 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-medium text-gray-900">Commission History</h3>
        <div class="flex items-center space-x-4">
          <!-- Period Filter -->
          <select
            v-model="localFilters.period"
            class="input-field text-sm"
            @change="applyFilters"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="1y">Last year</option>
            <option value="all">All time</option>
          </select>

          <!-- Status Filter -->
          <select
            v-model="localFilters.status"
            class="input-field text-sm"
            @change="applyFilters"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="available">Available</option>
            <option value="paid">Paid</option>
            <option value="cancelled">Cancelled</option>
          </select>

          <!-- Type Filter -->
          <select
            v-model="localFilters.type"
            class="input-field text-sm"
            @change="applyFilters"
          >
            <option value="">All Types</option>
            <option value="sale">Sales</option>
            <option value="signup">Signups</option>
            <option value="bonus">Bonuses</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="affiliateStore.isLoading" class="p-8 text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-2 text-sm text-gray-600">Loading commissions...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredCommissions.length === 0" class="p-8 text-center">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No commissions yet</h3>
      <p class="mt-1 text-sm text-gray-500">Start sharing your referral links to earn commissions!</p>
    </div>

    <!-- Commissions Table -->
    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Date
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Description
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Type
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Amount
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="commission in filteredCommissions"
            :key="commission.id"
            class="hover:bg-gray-50 transition-colors duration-150"
          >
            <!-- Date -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ formatDate(commission.created_at) }}
            </td>

            <!-- Description -->
            <td class="px-6 py-4 text-sm text-gray-900">
              <div>
                <p class="font-medium">{{ commission.description }}</p>
                <p v-if="commission.referral" class="text-gray-500 text-xs">
                  Referral: {{ commission.referral.user_email }}
                </p>
                <p v-if="commission.order" class="text-gray-500 text-xs">
                  Order: #{{ commission.order.order_number }}
                </p>
              </div>
            </td>

            <!-- Type -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="badge" :class="getTypeBadgeClass(commission.type)">
                {{ formatType(commission.type) }}
              </span>
            </td>

            <!-- Status -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="badge" :class="getStatusBadgeClass(commission.status)">
                {{ formatStatus(commission.status) }}
              </span>
              <p v-if="commission.paid_at" class="text-xs text-gray-500 mt-1">
                Paid: {{ formatDate(commission.paid_at) }}
              </p>
            </td>

            <!-- Amount -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              <div class="text-right">
                <p class="font-semibold">${{ commission.amount.toFixed(2) }}</p>
                <p v-if="commission.order" class="text-xs text-gray-500">
                  {{ commission.commission_rate }}% of ${{ commission.order.total_amount.toFixed(2) }}
                </p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table Footer -->
    <div v-if="filteredCommissions.length > 0" class="px-6 py-4 border-t border-gray-200 bg-gray-50">
      <div class="flex items-center justify-between">
        <div class="text-sm text-gray-700">
          Showing {{ filteredCommissions.length }} commissions
        </div>
        <div class="text-sm font-medium text-gray-900">
          Total: ${{ affiliateStore.commissionStats.total_amount.toFixed(2) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useAffiliateStore } from '@/stores/affiliate'

const affiliateStore = useAffiliateStore()

const localFilters = reactive({
  period: '30d',
  status: '',
  type: ''
})

const filteredCommissions = affiliateStore.filteredCommissions

// Initialize with current filters
onMounted(() => {
  Object.assign(localFilters, affiliateStore.filters)
})

const applyFilters = () => {
  affiliateStore.updateFilters(localFilters)
  affiliateStore.fetchCommissions()
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatType = (type) => {
  const typeMap = {
    sale: 'Sale',
    signup: 'Signup',
    bonus: 'Bonus'
  }
  return typeMap[type] || type
}

const formatStatus = (status) => {
  const statusMap = {
    pending: 'Pending',
    available: 'Available',
    paid: 'Paid',
    cancelled: 'Cancelled'
  }
  return statusMap[status] || status
}

const getTypeBadgeClass = (type) => {
  const typeClasses = {
    sale: 'badge-primary',
    signup: 'badge-info',
    bonus: 'badge-warning'
  }
  return typeClasses[type] || 'badge-secondary'
}

const getStatusBadgeClass = (status) => {
  const statusClasses = {
    pending: 'badge-warning',
    available: 'badge-success',
    paid: 'badge-info',
    cancelled: 'badge-error'
  }
  return statusClasses[status] || 'badge-secondary'
}
</script>

<style scoped>
.badge {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium;
}

.badge-primary {
  @apply bg-primary-100 text-primary-800;
}

.badge-info {
  @apply bg-blue-100 text-blue-800;
}

.badge-warning {
  @apply bg-yellow-100 text-yellow-800;
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