<template>
  <div class="card hover:shadow-md transition-shadow duration-300">
    <div class="p-6">
      <!-- Order Header -->
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">
            Order #{{ order.order_number }}
          </h3>
          <p class="text-sm text-gray-500">
            {{ formatDate(order.created_at) }}
          </p>
        </div>
        <div class="text-right">
          <span class="badge" :class="statusBadgeClass">
            {{ formatStatus(order.status) }}
          </span>
          <p class="text-lg font-bold text-gray-900 mt-1">
            ${{ order.total_amount.toFixed(2) }}
          </p>
        </div>
      </div>

      <!-- Order Items Preview -->
      <div class="border-t border-gray-200 pt-4">
        <div class="flex items-center space-x-3 mb-3">
          <div class="flex -space-x-2">
            <div
              v-for="(item, index) in previewItems"
              :key="item.id"
              class="w-10 h-10 border-2 border-white rounded-lg overflow-hidden"
              :style="{ zIndex: previewItems.length - index }"
            >
              <img
                :src="item.book.cover_image || '/placeholder-book.jpg'"
                :alt="item.book.title"
                class="w-full h-full object-cover"
              />
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-600 truncate">
              {{ getItemTitles(order.items) }}
            </p>
            <p class="text-xs text-gray-500">
              {{ order.items.length }} item{{ order.items.length > 1 ? 's' : '' }}
            </p>
          </div>
        </div>

        <!-- Order Actions -->
        <div class="flex items-center justify-between pt-4 border-t border-gray-200">
          <div class="flex space-x-2">
            <router-link
              :to="`/orders/${order.id}`"
              class="btn-secondary text-sm px-3 py-1"
            >
              View Details
            </router-link>
            
            <button
              v-if="canCancel"
              @click="cancelOrder"
              class="btn-secondary text-sm px-3 py-1 text-red-600 border-red-200 hover:bg-red-50"
            >
              Cancel Order
            </button>
          </div>

          <!-- Review Button -->
          <button
            v-if="canReview"
            @click="writeReview"
            class="btn-primary text-sm px-3 py-1"
          >
            Write Review
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useOrderStore } from '@/stores/orders'
import { useNotificationStore } from '@/stores/notifications'

const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const orderStore = useOrderStore()
const notificationStore = useNotificationStore()

const previewItems = computed(() => props.order.items.slice(0, 3))

const statusBadgeClass = computed(() => {
  const statusClasses = {
    pending: 'badge-warning',
    processing: 'badge-info',
    shipped: 'badge-primary',
    delivered: 'badge-success',
    cancelled: 'badge-error'
  }
  return statusClasses[props.order.status] || 'badge-secondary'
})

const canCancel = computed(() => {
  return ['pending', 'processing'].includes(props.order.status)
})

const canReview = computed(() => {
  return props.order.status === 'delivered' && !props.order.has_reviewed
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
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

const getItemTitles = (items) => {
  if (items.length === 0) return ''
  if (items.length === 1) return items[0].book.title
  return `${items[0].book.title} and ${items.length - 1} more`
}

const cancelOrder = async () => {
  if (!confirm('Are you sure you want to cancel this order?')) return

  const result = await orderStore.cancelOrder(props.order.id)
  if (result.success) {
    notificationStore.success('Order cancelled successfully')
  } else {
    notificationStore.error(result.error || 'Failed to cancel order')
  }
}

const writeReview = () => {
  router.push(`/books/${props.order.items[0].book.id}?review=true`)
}
</script>

<style scoped>
.badge {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium;
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