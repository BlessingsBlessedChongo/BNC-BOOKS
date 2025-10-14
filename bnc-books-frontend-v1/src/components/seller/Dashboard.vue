<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Seller Dashboard</h1>
      <p class="mt-2 text-lg text-gray-600">Manage your books and track your sales</p>
    </div>

    <!-- Stats Cards -->
    <StatsCards />

    <!-- Quick Actions -->
    <QuickActions class="mb-8" />

    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Recent Orders -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Recent Orders</h3>
          <router-link to="/seller/orders" class="text-sm text-primary-600 hover:text-primary-500">
            View all
          </router-link>
        </div>
        
        <div v-if="recentOrders.length === 0" class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
          </svg>
          <p class="mt-2 text-sm text-gray-600">No recent orders</p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="order in recentOrders"
            :key="order.id"
            class="flex items-center justify-between py-3 border-b border-gray-200 last:border-0"
          >
            <div>
              <p class="text-sm font-medium text-gray-900">
                Order #{{ order.order_number }}
              </p>
              <p class="text-sm text-gray-500">
                {{ formatDate(order.created_at) }}
              </p>
            </div>
            <div class="text-right">
              <span class="badge" :class="getStatusBadgeClass(order.status)">
                {{ formatStatus(order.status) }}
              </span>
              <p class="text-sm font-medium text-gray-900 mt-1">
                ${{ order.total_amount.toFixed(2) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Low Stock Alert -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Low Stock Alert</h3>
          <router-link to="/seller/books" class="text-sm text-primary-600 hover:text-primary-500">
            Manage stock
          </router-link>
        </div>
        
        <div v-if="lowStockBooks.length === 0" class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
          </svg>
          <p class="mt-2 text-sm text-gray-600">All books are well stocked</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="book in lowStockBooks"
            :key="book.id"
            class="flex items-center justify-between p-3 bg-yellow-50 border border-yellow-200 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <img
                :src="book.cover_image || '/placeholder-book.jpg'"
                :alt="book.title"
                class="w-10 h-12 object-cover rounded"
              />
              <div>
                <p class="text-sm font-medium text-gray-900 line-clamp-1">
                  {{ book.title }}
                </p>
                <p class="text-xs text-gray-500">Stock: {{ book.stock_quantity }}</p>
              </div>
            </div>
            <button
              @click="updateInventory(book)"
              class="text-sm text-primary-600 hover:text-primary-500 font-medium"
            >
              Restock
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSellerStore } from '@/stores/seller'
import { useNotificationStore } from '@/stores/notifications'
import StatsCards from '@/components/seller/StatsCards.vue'
import QuickActions from '@/components/seller/QuickActions.vue'
import InventoryModal from '@/components/seller/InventoryModal.vue'

const sellerStore = useSellerStore()
const notificationStore = useNotificationStore()

const selectedBook = ref(null)
const showInventoryModal = ref(false)

const recentOrders = computed(() => sellerStore.orders.slice(0, 5))

const lowStockBooks = computed(() => {
  return sellerStore.books.filter(book => book.stock_quantity > 0 && book.stock_quantity < 10)
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}

const formatStatus = (status) => {
  const statusMap = {
    pending: 'Pending',
    processing: 'Processing',
    shipped: 'Shipped',
    delivered: 'Delivered',
    cancelled: 'Cancelled'
  }
  return statusMap[status] || status
}

const getStatusBadgeClass = (status) => {
  const statusClasses = {
    pending: 'badge-warning',
    processing: 'badge-info',
    shipped: 'badge-primary',
    delivered: 'badge-success',
    cancelled: 'badge-error'
  }
  return statusClasses[status] || 'badge-secondary'
}

const updateInventory = (book) => {
  selectedBook.value = book
  showInventoryModal.value = true
}

const handleInventoryUpdate = async (stockData) => {
  const result = await sellerStore.updateInventory(selectedBook.value.id, stockData)
  if (result.success) {
    notificationStore.success('Inventory updated successfully')
    showInventoryModal.value = false
  } else {
    notificationStore.error(result.error || 'Failed to update inventory')
  }
}

onMounted(async () => {
  await sellerStore.fetchBooks()
  await sellerStore.fetchOrders()
  await sellerStore.fetchAnalytics()
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

.badge-primary {
  @apply bg-primary-100 text-primary-800;
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

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>