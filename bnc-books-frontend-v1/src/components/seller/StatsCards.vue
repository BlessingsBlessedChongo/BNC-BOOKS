<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    <!-- Total Revenue -->
    <div class="card p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
            </svg>
          </div>
        </div>
        <div class="ml-4">
          <p class="text-sm font-medium text-gray-600">Total Revenue</p>
          <p class="text-2xl font-bold text-gray-900">${{ analytics?.total_revenue?.toFixed(2) || '0.00' }}</p>
          <p class="text-sm text-green-600 flex items-center">
            <span v-if="analytics?.revenue_growth >= 0">↑</span>
            <span v-else>↓</span>
            {{ Math.abs(analytics?.revenue_growth || 0) }}% from last period
          </p>
        </div>
      </div>
    </div>

    <!-- Total Orders -->
    <div class="card p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
            </svg>
          </div>
        </div>
        <div class="ml-4">
          <p class="text-sm font-medium text-gray-600">Total Orders</p>
          <p class="text-2xl font-bold text-gray-900">{{ analytics?.total_orders || 0 }}</p>
          <p class="text-sm text-blue-600 flex items-center">
            <span v-if="analytics?.order_growth >= 0">↑</span>
            <span v-else>↓</span>
            {{ Math.abs(analytics?.order_growth || 0) }}% from last period
          </p>
        </div>
      </div>
    </div>

    <!-- Books Listed -->
    <div class="card p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
            </svg>
          </div>
        </div>
        <div class="ml-4">
          <p class="text-sm font-medium text-gray-600">Books Listed</p>
          <p class="text-2xl font-bold text-gray-900">{{ bookStats.total }}</p>
          <p class="text-sm text-purple-600">
            {{ bookStats.published }} published
          </p>
        </div>
      </div>
    </div>

    <!-- Conversion Rate -->
    <div class="card p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
          </div>
        </div>
        <div class="ml-4">
          <p class="text-sm font-medium text-gray-600">Conversion Rate</p>
          <p class="text-2xl font-bold text-gray-900">{{ analytics?.conversion_rate?.toFixed(1) || '0.0' }}%</p>
          <p class="text-sm text-orange-600">
            {{ analytics?.total_views || 0 }} views
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSellerStore } from '@/stores/seller'

const sellerStore = useSellerStore()

const analytics = sellerStore.analytics
const bookStats = sellerStore.bookStats
</script>