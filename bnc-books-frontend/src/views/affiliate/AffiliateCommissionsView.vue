<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Commissions</h1>
        <p class="mt-2 text-lg text-gray-600">Track your referral commissions and earnings</p>
      </div>

      <!-- Error Message -->
      <div v-if="affiliateStore.error" class="mb-6 rounded-md bg-red-50 p-4">
        <div class="text-sm text-red-700">{{ affiliateStore.error }}</div>
      </div>

      <!-- Stats Summary -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
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
              <p class="text-sm font-medium text-gray-600">Total Earned</p>
              <p class="text-2xl font-bold text-gray-900">
                ${{ totalEarned.toFixed(2) }}
              </p>
            </div>
          </div>
        </div>

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
              <p class="text-sm font-medium text-gray-600">Available</p>
              <p class="text-2xl font-bold text-gray-900">
                ${{ availableBalance.toFixed(2) }}
              </p>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Pending</p>
              <p class="text-2xl font-bold text-gray-900">
                ${{ pendingBalance.toFixed(2) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="card p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select
              v-model="statusFilter"
              class="input-field"
              @change="applyFilters"
            >
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="paid">Paid</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          <div class="flex items-end">
            <button
              @click="clearFilters"
              class="btn-secondary w-full"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      <!-- Commissions Table -->
      <div class="card overflow-hidden">
        <!-- Loading State -->
        <div v-if="affiliateStore.isLoading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
          <p class="mt-2 text-sm text-gray-600">Loading commissions...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="affiliateStore.commissions.length === 0" class="p-12 text-center">
          <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900">No commissions yet</h3>
          <p class="mt-2 text-sm text-gray-500">Start earning by sharing your referral links!</p>
          <div class="mt-6">
            <router-link to="/affiliate" class="btn-primary">
              Create Referral Link
            </router-link>
          </div>
        </div>

        <!-- Commissions List -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Commission
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Referral
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Order
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr 
                v-for="commission in affiliateStore.commissions" 
                :key="commission.id"
                class="hover:bg-gray-50 transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">${{ commission.amount }}</div>
                  <div class="text-sm text-gray-500">{{ commission.commission_rate }}% rate</div>
                  <div class="text-sm text-gray-500">{{ commission.type }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ commission.referral.user_email }}</div>
                  <div class="text-sm text-gray-500 capitalize">{{ commission.referral.status }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ commission.order.order_number }}</div>
                  <div class="text-sm text-gray-500">${{ commission.order.total_amount }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusBadgeClass(commission.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize">
                    {{ commission.status }}
                  </span>
                  <div v-if="commission.paid_at" class="text-xs text-gray-500 mt-1">
                    Paid: {{ formatDate(commission.paid_at) }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(commission.created_at) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="affiliateStore.commissions.length > 0" class="px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <p class="text-sm text-gray-700">
              Showing {{ (affiliateStore.pagination.current_page - 1) * affiliateStore.pagination.page_size + 1 }} to 
              {{ Math.min(affiliateStore.pagination.current_page * affiliateStore.pagination.page_size, affiliateStore.pagination.count) }} of 
              {{ affiliateStore.pagination.count }} results
            </p>
            <div class="flex space-x-2">
              <button
                @click="loadPreviousPage"
                :disabled="!affiliateStore.pagination.previous"
                class="btn-secondary text-sm disabled:opacity-50"
              >
                Previous
              </button>
              <button
                @click="loadNextPage"
                :disabled="!affiliateStore.pagination.next"
                class="btn-secondary text-sm disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import AppLayout from '../../layouts/AppLayout.vue';
import { useAffiliateStore } from '../../stores/affiliate';

const affiliateStore = useAffiliateStore();

const statusFilter = ref('');

const totalEarned = computed(() => {
  return affiliateStore.commissions
    .filter(c => c.status === 'paid')
    .reduce((total, commission) => total + commission.amount, 0);
});

const availableBalance = computed(() => {
  return affiliateStore.analytics?.available_balance || 0;
});

const pendingBalance = computed(() => {
  return affiliateStore.commissions
    .filter(c => c.status === 'pending')
    .reduce((total, commission) => total + commission.amount, 0);
});

const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    paid: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800'
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

const applyFilters = () => {
  affiliateStore.updateCommissionFilters({ 
    status: statusFilter.value,
    page: 1
  });
  affiliateStore.fetchCommissions();
};

const clearFilters = () => {
  statusFilter.value = '';
  affiliateStore.updateCommissionFilters({ 
    status: '',
    page: 1
  });
  affiliateStore.fetchCommissions();
};

const loadNextPage = () => {
  if (affiliateStore.pagination.next) {
    affiliateStore.updateCommissionFilters({ page: affiliateStore.pagination.current_page + 1 });
    affiliateStore.fetchCommissions();
  }
};

const loadPreviousPage = () => {
  if (affiliateStore.pagination.previous) {
    affiliateStore.updateCommissionFilters({ page: affiliateStore.pagination.current_page - 1 });
    affiliateStore.fetchCommissions();
  }
};

onMounted(async () => {
  await affiliateStore.fetchCommissions();
});
</script>