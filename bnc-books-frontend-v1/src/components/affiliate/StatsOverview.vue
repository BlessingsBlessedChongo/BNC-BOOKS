<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    <!-- Total Commissions -->
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
          <p class="text-sm font-medium text-gray-600">Total Commissions</p>
          <p class="text-2xl font-bold text-gray-900">${{ commissionStats.total_amount.toFixed(2) }}</p>
          <p class="text-sm text-green-600 flex items-center">
            <span v-if="analytics?.commission_growth >= 0">↑</span>
            <span v-else>↓</span>
            {{ Math.abs(analytics?.commission_growth || 0) }}% from last period
          </p>
        </div>
      </div>
    </div>

    <!-- Available for Payout -->
    <div class="card p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
        </div>
        <div class="ml-4">
          <p class="text-sm font-medium text-gray-600">Available for Payout</p>
          <p class="text-2xl font-bold text-gray-900">${{ commissionStats.available_amount.toFixed(2) }}</p>
          <p class="text-sm text-blue-600">
            {{ commissionStats.available }} commissions
          </p>
        </div>
      </div>
    </div>

    <!-- Total Referrals -->
    <div class="card p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
            </svg>
          </div>
        </div>
        <div class="ml-4">
          <p class="text-sm font-medium text-gray-600">Total Referrals</p>
          <p class="text-2xl font-bold text-gray-900">{{ referralStats.total }}</p>
          <p class="text-sm text-purple-600">
            {{ referralStats.converted }} converted
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
          <p class="text-2xl font-bold text-gray-900">
            {{ referralStats.total > 0 ? ((referralStats.converted / referralStats.total) * 100).toFixed(1) : '0.0' }}%
          </p>
          <p class="text-sm text-orange-600">
            {{ analytics?.clicks || 0 }} clicks
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAffiliateStore } from '@/stores/affiliate'

const affiliateStore = useAffiliateStore()

const commissionStats = affiliateStore.commissionStats
const referralStats = affiliateStore.referralStats
const analytics = affiliateStore.analytics
</script>