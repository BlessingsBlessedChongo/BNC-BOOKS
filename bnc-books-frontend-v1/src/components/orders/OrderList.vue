<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">My Orders</h1>
      <p class="mt-2 text-lg text-gray-600">Track and manage your orders</p>
    </div>

    <!-- Order Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
      <div class="card p-6 text-center">
        <div class="text-2xl font-bold text-primary-600">{{ orderStats.total }}</div>
        <div class="text-sm text-gray-600 mt-1">Total Orders</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-2xl font-bold text-green-600">${{ orderStats.total_spent.toFixed(2) }}</div>
        <div class="text-sm text-gray-600 mt-1">Total Spent</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-2xl font-bold text-blue-600">{{ orderStats.delivered || 0 }}</div>
        <div class="text-sm text-gray-600 mt-1">Delivered</div>
      </div>
      <div class="card p-6 text-center">
        <div class="text-2xl font-bold text-yellow-600">{{ orderStats.pending || 0 }}</div>
        <div class="text-sm text-gray-600 mt-1">Pending</div>
      </div>
    </div>

    <!-- Filters -->
    <OrderFilters />

    <!-- Loading State -->
    <div v-if="orderStore.isLoading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Loading your orders...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredOrders.length === 0" class="text-center py-12">
      <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
      </svg>
      <h3 class="mt-4 text-lg font-medium text-gray-900">No orders found</h3>
      <p class="mt-2 text-gray-600">You haven't placed any orders yet.</p>
      <div class="mt-6">
        <router-link to="/books" class="btn-primary text-lg px-8 py-3">
          Start Shopping
        </router-link>
      </div>
    </div>

    <!-- Orders Grid -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <OrderCard
        v-for="order in filteredOrders"
        :key="order.id"
        :order="order"
      />
    </div>

    <!-- Load More Button -->
    <div v-if="hasMoreOrders" class="mt-8 text-center">
      <button
        @click="loadMore"
        :disabled="orderStore.isLoading"
        class="btn-primary"
      >
        Load More Orders
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '@/stores/orders'
import OrderFilters from '@/components/orders/OrderFilters.vue'
import OrderCard from '@/components/orders/OrderCard.vue'

const orderStore = useOrderStore()

const currentPage = ref(1)
const hasMoreOrders = ref(true)

const filteredOrders = computed(() => orderStore.filteredOrders)
const orderStats = computed(() => orderStore.orderStats)

const loadMore = async () => {
  currentPage.value++
  const result = await orderStore.fetchOrders({ page: currentPage.value })
  if (result.data && (!result.data.next || result.data.results.length === 0)) {
    hasMoreOrders.value = false
  }
}

onMounted(async () => {
  await orderStore.fetchOrders()
})
</script>