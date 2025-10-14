<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Loading State -->
    <div v-if="orderStore.isLoading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Loading order details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="orderStore.error" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">Order not found</h3>
      <p class="mt-1 text-sm text-gray-500">{{ orderStore.error }}</p>
      <div class="mt-6">
        <router-link to="/orders" class="btn-primary">
          Back to Orders
        </router-link>
      </div>
    </div>

    <!-- Order Details -->
    <div v-else-if="orderStore.currentOrder" class="space-y-8">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">
            Order #{{ orderStore.currentOrder.order_number }}
          </h1>
          <p class="mt-1 text-sm text-gray-500">
            Placed on {{ formatDate(orderStore.currentOrder.created_at) }}
          </p>
        </div>
        <div class="mt-4 sm:mt-0">
          <span class="badge" :class="statusBadgeClass">
            {{ formatStatus(orderStore.currentOrder.status) }}
          </span>
        </div>
      </div>

      <!-- Order Progress -->
      <div class="card p-6">
        <h2 class="text-lg font-medium text-gray-900 mb-4">Order Status</h2>
        <OrderTimeline :order="orderStore.currentOrder" />
      </div>

      <!-- Order Items -->
      <div class="card p-6">
        <h2 class="text-lg font-medium text-gray-900 mb-4">Order Items</h2>
        <div class="space-y-4">
          <div
            v-for="item in orderStore.currentOrder.items"
            :key="item.id"
            class="flex items-center space-x-4 py-4 border-b border-gray-200 last:border-0"
          >
            <div class="flex-shrink-0 w-16 h-20">
              <img
                :src="item.book.cover_image || '/placeholder-book.jpg'"
                :alt="item.book.title"
                class="w-full h-full object-cover rounded"
              />
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="text-sm font-medium text-gray-900">
                {{ item.book.title }}
              </h3>
              <p class="text-sm text-gray-500">by {{ item.book.author }}</p>
              <p class="text-sm text-gray-500">Qty: {{ item.quantity }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium text-gray-900">
                ${{ (item.book.price * item.quantity).toFixed(2) }}
              </p>
              <p class="text-sm text-gray-500">${{ item.book.price.toFixed(2) }} each</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Shipping and Payment Information -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Shipping Address -->
        <div class="card p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-4">Shipping Address</h2>
          <div class="text-sm text-gray-600">
            <p class="font-medium">{{ orderStore.currentOrder.shipping_address.first_name }} {{ orderStore.currentOrder.shipping_address.last_name }}</p>
            <p>{{ orderStore.currentOrder.shipping_address.street_address }}</p>
            <p v-if="orderStore.currentOrder.shipping_address.apartment">
              {{ orderStore.currentOrder.shipping_address.apartment }}
            </p>
            <p>
              {{ orderStore.currentOrder.shipping_address.city }}, {{ orderStore.currentOrder.shipping_address.state }} {{ orderStore.currentOrder.shipping_address.zip_code }}
            </p>
            <p>{{ orderStore.currentOrder.shipping_address.country }}</p>
            <p class="mt-2">{{ orderStore.currentOrder.shipping_address.phone }}</p>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="card p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-4">Order Summary</h2>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Subtotal</span>
              <span class="text-gray-900">${{ orderStore.currentOrder.subtotal.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Shipping</span>
              <span class="text-gray-900">${{ orderStore.currentOrder.shipping_cost.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Tax</span>
              <span class="text-gray-900">${{ orderStore.currentOrder.tax_amount.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between border-t border-gray-200 pt-2">
              <span class="text-lg font-medium text-gray-900">Total</span>
              <span class="text-lg font-medium text-gray-900">${{ orderStore.currentOrder.total_amount.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Payment Method -->
          <div class="mt-6 pt-6 border-t border-gray-200">
            <h3 class="text-sm font-medium text-gray-900">Payment Method</h3>
            <p class="mt-1 text-sm text-gray-600 capitalize">
              {{ orderStore.currentOrder.payment_method }}
            </p>
          </div>
        </div>
      </div>

      <!-- Order Actions -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <router-link to="/orders" class="btn-secondary">
          Back to Orders
        </router-link>
        
        <div class="flex space-x-3">
          <button
            v-if="canCancel"
            @click="cancelOrder"
            class="btn-secondary text-red-600 border-red-200 hover:bg-red-50"
          >
            Cancel Order
          </button>
          
          <button
            v-if="canReturn"
            @click="requestReturn"
            class="btn-primary"
          >
            Request Return
          </button>
          
          <button
            v-if="canReview"
            @click="writeReview"
            class="btn-primary"
          >
            Write Review
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOrderStore } from '@/stores/orders'
import { useNotificationStore } from '@/stores/notifications'
import OrderTimeline from '@/components/orders/OrderTimeline.vue'

const route = useRoute()
const router = useRouter()
const orderStore = useOrderStore()
const notificationStore = useNotificationStore()

const orderId = computed(() => route.params.id)

const statusBadgeClass = computed(() => {
  const statusClasses = {
    pending: 'badge-warning',
    processing: 'badge-info',
    shipped: 'badge-primary',
    delivered: 'badge-success',
    cancelled: 'badge-error'
  }
  return statusClasses[orderStore.currentOrder?.status] || 'badge-secondary'
})

const canCancel = computed(() => {
  return ['pending', 'processing'].includes(orderStore.currentOrder?.status)
})

const canReturn = computed(() => {
  return orderStore.currentOrder?.status === 'delivered' && 
         !orderStore.currentOrder?.return_requested
})

const canReview = computed(() => {
  return orderStore.currentOrder?.status === 'delivered' && 
         !orderStore.currentOrder?.has_reviewed
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
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

const cancelOrder = async () => {
  if (!confirm('Are you sure you want to cancel this order?')) return

  const result = await orderStore.cancelOrder(orderId.value)
  if (result.success) {
    notificationStore.success('Order cancelled successfully')
  } else {
    notificationStore.error(result.error || 'Failed to cancel order')
  }
}

const requestReturn = () => {
  // Implement return request modal or page
  notificationStore.info('Return request feature coming soon')
}

const writeReview = () => {
  const firstBook = orderStore.currentOrder.items[0]?.book
  if (firstBook) {
    router.push(`/books/${firstBook.id}?review=true`)
  }
}

onMounted(async () => {
  await orderStore.fetchOrder(orderId.value)
})
</script>

<style scoped>
.badge {
  @apply inline-flex items-center px-3 py-1 rounded-full text-sm font-medium;
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
</style>