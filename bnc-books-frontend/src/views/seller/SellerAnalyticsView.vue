<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Sales Analytics</h1>
          <p class="mt-2 text-lg text-gray-600">Track your sales performance and insights</p>
        </div>
        <div class="mt-4 sm:mt-0">
          <select
            v-model="selectedPeriod"
            @change="loadAnalytics"
            class="input-field"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="1y">Last year</option>
          </select>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="sellerStore.error" class="mb-6 rounded-md bg-red-50 p-4">
        <div class="text-sm text-red-700">{{ sellerStore.error }}</div>
      </div>

      <!-- Loading State -->
      <div v-if="sellerStore.isLoading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading analytics...</p>
      </div>

      <!-- Analytics Content -->
      <div v-else-if="analytics" class="space-y-8">
        <!-- Key Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Total Revenue -->
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
                <p class="text-sm font-medium text-gray-600">Total Revenue</p>
                <p class="text-2xl font-bold text-gray-900">${{ analytics.total_revenue.toFixed(2) }}</p>
                <p v-if="analytics.revenue_growth" class="text-sm" :class="analytics.revenue_growth >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ analytics.revenue_growth >= 0 ? '+' : '' }}{{ analytics.revenue_growth.toFixed(1) }}%
                </p>
              </div>
            </div>
          </div>

          <!-- Total Orders -->
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Orders</p>
                <p class="text-2xl font-bold text-gray-900">{{ analytics.total_orders }}</p>
                <p v-if="analytics.order_growth" class="text-sm" :class="analytics.order_growth >= 0 ? 'text-green-600' : 'text-red-600'">
                  {{ analytics.order_growth >= 0 ? '+' : '' }}{{ analytics.order_growth.toFixed(1) }}%
                </p>
              </div>
            </div>
          </div>

          <!-- Total Books -->
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Books</p>
                <p class="text-2xl font-bold text-gray-900">{{ analytics.total_books }}</p>
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
                <p class="text-2xl font-bold text-gray-900">{{ analytics.conversion_rate.toFixed(1) }}%</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Additional Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Average Commission -->
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Avg Commission</p>
                <p class="text-2xl font-bold text-gray-900">${{ analytics.average_commission.toFixed(2) }}</p>
              </div>
            </div>
          </div>

          <!-- Total Views -->
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-pink-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Views</p>
                <p class="text-2xl font-bold text-gray-900">{{ analytics.total_views.toLocaleString() }}</p>
              </div>
            </div>
          </div>

          <!-- Available Balance -->
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Available Balance</p>
                <p class="text-2xl font-bold text-gray-900">${{ (analytics.total_revenue * 0.85).toFixed(2) }}</p>
                <p class="text-sm text-gray-500">After 15% platform fee</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Selling Books -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Top Selling Books</h2>
          </div>
          <div class="p-6">
            <div v-if="!analytics.top_selling_books?.length" class="text-center py-4">
              <p class="text-sm text-gray-500">No sales data available</p>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="book in analytics.top_selling_books" 
                :key="book.id"
                class="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
              >
                <div class="flex items-center space-x-4">
                  <img
                    :src="book.cover_image"
                    :alt="book.title"
                    class="w-12 h-16 object-cover rounded"
                    @error="handleImageError"
                  />
                  <div>
                    <p class="font-medium text-gray-900">{{ book.title }}</p>
                    <p class="text-sm text-gray-600">{{ book.sales }} sold</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="font-medium text-gray-900">${{ book.revenue.toFixed(2) }}</p>
                  <p class="text-sm text-gray-600">Revenue</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Revenue Chart Placeholder -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Revenue Over Time</h2>
          </div>
          <div class="p-6">
            <div class="text-center py-12">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <h3 class="mt-4 text-sm font-medium text-gray-900">Revenue Chart</h3>
              <p class="mt-1 text-sm text-gray-500">Revenue visualization would be displayed here with a charting library.</p>
              <div class="mt-4 space-y-2">
                <div 
                  v-for="period in analytics.revenue_by_period" 
                  :key="period.date"
                  class="flex justify-between text-sm"
                >
                  <span class="text-gray-600">{{ formatDate(period.date) }}</span>
                  <span class="font-medium text-gray-900">${{ period.revenue.toFixed(2) }}</span>
                </div>
              </div>
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
import { useSellerStore } from '../../stores/seller';

const sellerStore = useSellerStore();

const selectedPeriod = ref('30d');

const analytics = computed(() => sellerStore.analytics);

const loadAnalytics = async () => {
  await sellerStore.fetchAnalytics(selectedPeriod.value);
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  });
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};

onMounted(async () => {
  await loadAnalytics();
});
</script>