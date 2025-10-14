<template>
  <div class="relative">
    <!-- Notification Bell -->
    <button
      @click="toggleNotificationCenter"
      class="relative p-2 text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-teal-500 rounded-lg"
    >
      <BellIcon class="h-6 w-6" />
      <span
        v-if="unreadCount > 0"
        class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <!-- Notification Dropdown -->
    <div
      v-if="isOpen"
      class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50 max-h-96 overflow-hidden"
    >
      <!-- Header -->
      <div class="p-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Notifications</h3>
          <div class="flex items-center space-x-2">
            <button
              @click="markAllAsRead"
              :disabled="markingAllAsRead"
              class="text-sm text-teal-600 hover:text-teal-700 disabled:opacity-50"
            >
              {{ markingAllAsRead ? 'Marking...' : 'Mark all read' }}
            </button>
            <button
              @click="viewAllNotifications"
              class="text-sm text-teal-600 hover:text-teal-700"
            >
              View all
            </button>
          </div>
        </div>
      </div>

      <!-- Notifications List -->
      <div class="overflow-y-auto max-h-64">
        <div v-if="loading" class="p-4">
          <div class="animate-pulse space-y-3">
            <div v-for="n in 3" :key="n" class="flex space-x-3">
              <div class="rounded-full bg-gray-200 h-8 w-8"></div>
              <div class="flex-1 space-y-2">
                <div class="h-3 bg-gray-200 rounded w-3/4"></div>
                <div class="h-2 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="recentNotifications.length > 0" class="divide-y divide-gray-200">
          <div
            v-for="notification in recentNotifications"
            :key="notification.id"
            :class="[
              'p-4 hover:bg-gray-50 cursor-pointer transition-colors',
              !notification.read ? 'bg-blue-50 hover:bg-blue-100' : ''
            ]"
            @click="handleNotificationClick(notification)"
          >
            <div class="flex items-start space-x-3">
              <!-- Notification Icon -->
              <div
                :class="[
                  'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
                  getNotificationIcon(notification.type).bgColor
                ]"
              >
                <component
                  :is="getNotificationIcon(notification.type).icon"
                  :class="['h-4 w-4', getNotificationIcon(notification.type).color]"
                />
              </div>

              <!-- Notification Content -->
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">
                  {{ notification.title }}
                </p>
                <p class="mt-1 text-sm text-gray-600 line-clamp-2">
                  {{ notification.message }}
                </p>
                <p class="mt-1 text-xs text-gray-500">
                  {{ formatTimeAgo(notification.created_at) }}
                </p>
              </div>

              <!-- Unread Indicator -->
              <div v-if="!notification.read" class="flex-shrink-0">
                <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="p-8 text-center">
          <BellIcon class="mx-auto h-8 w-8 text-gray-400" />
          <p class="mt-2 text-sm text-gray-600">No notifications</p>
        </div>
      </div>

      <!-- Footer -->
      <div v-if="recentNotifications.length > 0" class="p-4 border-t border-gray-200 bg-gray-50">
        <button
          @click="viewAllNotifications"
          class="w-full text-center px-4 py-2 text-sm font-medium text-teal-600 hover:text-teal-700 focus:outline-none"
        >
          See all notifications
        </button>
      </div>
    </div>

    <!-- Backdrop -->
    <div
      v-if="isOpen"
      class="fixed inset-0 z-40"
      @click="isOpen = false"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/stores/notifications'
import {
  BellIcon,
  ShoppingCartIcon,
  StarIcon,
  CurrencyDollarIcon,
  TruckIcon,
  CheckIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const notificationStore = useNotificationStore()

// State
const isOpen = ref(false)
const markingAllAsRead = ref(false)

// Computed
const unreadCount = computed(() => notificationStore.unreadCount)
const recentNotifications = computed(() => 
  notificationStore.notifications.slice(0, 5) // Show only 5 most recent
)
const loading = computed(() => notificationStore.loading)

// Notification type icons mapping
const getNotificationIcon = (type) => {
  const icons = {
    order_placed: { icon: ShoppingCartIcon, bgColor: 'bg-blue-100', color: 'text-blue-600' },
    order_shipped: { icon: TruckIcon, bgColor: 'bg-green-100', color: 'text-green-600' },
    order_delivered: { icon: CheckIcon, bgColor: 'bg-teal-100', color: 'text-teal-600' },
    order_cancelled: { icon: ExclamationTriangleIcon, bgColor: 'bg-red-100', color: 'text-red-600' },
    review_received: { icon: StarIcon, bgColor: 'bg-yellow-100', color: 'text-yellow-600' },
    commission_earned: { icon: CurrencyDollarIcon, bgColor: 'bg-green-100', color: 'text-green-600' },
    system: { icon: BellIcon, bgColor: 'bg-gray-100', color: 'text-gray-600' }
  }
  return icons[type] || icons.system
}

// Methods
const toggleNotificationCenter = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value && notificationStore.notifications.length === 0) {
    notificationStore.fetchNotifications()
  }
}

const markAllAsRead = async () => {
  markingAllAsRead.value = true
  try {
    await notificationStore.markAllAsRead()
  } catch (error) {
    console.error('Failed to mark all as read:', error)
  } finally {
    markingAllAsRead.value = false
  }
}

const viewAllNotifications = () => {
  isOpen.value = false
  router.push('/notifications')
}

const handleNotificationClick = (notification) => {
  // Mark as read
  if (!notification.read) {
    notificationStore.markAsRead(notification.id)
  }

  // Close dropdown
  isOpen.value = false

  // Navigate if there's an action URL
  if (notification.action_url) {
    router.push(notification.action_url)
  }
}

const formatTimeAgo = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    isOpen.value = false
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  // Load notifications if not already loaded
  if (notificationStore.notifications.length === 0) {
    notificationStore.fetchNotifications()
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>