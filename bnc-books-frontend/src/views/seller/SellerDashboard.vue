<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Seller Dashboard</h1>
        <p class="mt-2 text-lg text-gray-600">Manage your books, orders, and track your performance</p>
      </div>

      <!-- Error Message -->
      <div v-if="sellerStore.error" class="mb-6 rounded-md bg-red-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error</h3>
            <div class="mt-1 text-sm text-red-700">
              <p>{{ sellerStore.error }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
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
              <p class="text-2xl font-bold text-gray-900">
                ${{ analytics?.total_revenue?.toFixed(2) || '0.00' }}
              </p>
              <p v-if="analytics?.revenue_growth" class="text-sm text-green-600">
                +{{ analytics.revenue_growth.toFixed(1) }}%
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
              <p class="text-2xl font-bold text-gray-900">{{ analytics?.total_orders || 0 }}</p>
              <p v-if="analytics?.order_growth" class="text-sm text-green-600">
                +{{ analytics.order_growth.toFixed(1) }}%
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
              <p class="text-2xl font-bold text-gray-900">{{ analytics?.total_books || 0 }}</p>
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
              <p class="text-2xl font-bold text-gray-900">
                {{ analytics?.conversion_rate?.toFixed(1) || '0.0' }}%
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <router-link 
          to="/seller/books" 
          class="card p-6 text-center hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">Manage Books</h3>
          <p class="mt-1 text-sm text-gray-600">Add, edit, or remove books</p>
        </router-link>

        <router-link 
          to="/seller/orders" 
          class="card p-6 text-center hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">Manage Orders</h3>
          <p class="mt-1 text-sm text-gray-600">Process and ship orders</p>
        </router-link>

        <router-link 
          to="/seller/analytics" 
          class="card p-6 text-center hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">View Analytics</h3>
          <p class="mt-1 text-sm text-gray-600">Track sales and performance</p>
        </router-link>

        <router-link 
          to="/seller/inventory" 
          class="card p-6 text-center hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900">Inventory</h3>
          <p class="mt-1 text-sm text-gray-600">Manage stock levels</p>
        </router-link>
      </div>

      <!-- Recent Activity -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Recent Orders -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Recent Orders</h2>
          </div>
          <div class="p-6">
            <div v-if="recentOrders.length === 0" class="text-center py-4">
              <p class="text-sm text-gray-500">No recent orders</p>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="order in recentOrders" 
                :key="order.id"
                class="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
              >
                <div>
                  <p class="font-medium text-gray-900">{{ order.order_number }}</p>
                  <p class="text-sm text-gray-600">{{ formatDate(order.created_at) }}</p>
                </div>
                <div class="text-right">
                  <p class="font-medium text-gray-900">${{ order.total_amount }}</p>
                  <span :class="getStatusBadgeClass(order.status)" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium capitalize">
                    {{ order.status }}
                  </span>
                </div>
              </div>
            </div>
            <div class="mt-4 text-center">
              <router-link to="/seller/orders" class="text-primary-600 hover:text-primary-700 text-sm font-medium">
                View all orders →
              </router-link>
            </div>
          </div>
        </div>

        <!-- Top Selling Books -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Top Selling Books</h2>
          </div>
          <div class="p-6">
            <div v-if="!analytics?.top_selling_books?.length" class="text-center py-4">
              <p class="text-sm text-gray-500">No sales data available</p>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="book in analytics.top_selling_books.slice(0, 5)" 
                :key="book.id"
                class="flex items-center space-x-3"
              >
                <img
                  :src="book.cover_image"
                  :alt="book.title"
                  class="w-10 h-14 object-cover rounded"
                  @error="handleImageError"
                />
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ book.title }}</p>
                  <p class="text-sm text-gray-600">{{ book.sales }} sold</p>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-900">${{ book.revenue.toFixed(2) }}</p>
                </div>
              </div>
            </div>
            <div class="mt-4 text-center">
              <router-link to="/seller/books" class="text-primary-600 hover:text-primary-700 text-sm font-medium">
                View all books →
              </router-link>
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

const analytics = computed(() => sellerStore.analytics);
const recentOrders = computed(() => sellerStore.sellerOrders.slice(0, 5));

const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    processing: 'bg-blue-100 text-blue-800',
    shipped: 'bg-purple-100 text-purple-800',
    delivered: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800'
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
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
  await sellerStore.fetchAnalytics();
  await sellerStore.fetchSellerOrders({ page_size: 5 });
});
</script>