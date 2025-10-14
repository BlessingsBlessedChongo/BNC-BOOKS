<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Notifications</h1>
            <p class="mt-2 text-sm text-gray-600">
              Stay updated with your orders, reviews, and account activity
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="markAllAsRead"
              :disabled="markingAllAsRead"
              class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50"
            >
              <CheckIcon class="h-4 w-4 mr-2" />
              {{ markingAllAsRead ? 'Marking...' : 'Mark All Read' }}
            </button>
            <button
              @click="showNotificationSettings = true"
              class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <Cog6ToothIcon class="h-4 w-4 mr-2" />
              Settings
            </button>
          </div>
        </div>

        <!-- Filter Tabs -->
        <div class="mt-6 border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              v-for="tab in tabs"
              :key="tab.name"
              @click="currentTab = tab.name"
              :class="[
                'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm',
                currentTab === tab.name
                  ? 'border-teal-500 text-teal-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.label }}
              <span
                v-if="tab.count > 0"
                :class="[
                  'ml-2 py-0.5 px-2 text-xs rounded-full',
                  currentTab === tab.name
                    ? 'bg-teal-100 text-teal-800'
                    : 'bg-gray-100 text-gray-800'
                ]"
              >
                {{ tab.count }}
              </span>
            </button>
          </nav>
        </div>
      </div>

      <!-- Notifications List -->
      <div class="bg-white shadow-sm rounded-lg border border-gray-200">
        <!-- Loading State -->
        <div v-if="loading" class="p-8">
          <div class="animate-pulse space-y-4">
            <div v-for="n in 5" :key="n" class="flex space-x-4">
              <div class="rounded-full bg-gray-200 h-10 w-10"></div>
              <div class="flex-1 space-y-2">
                <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Notifications -->
        <div v-else-if="filteredNotifications.length > 0" class="divide-y divide-gray-200">
          <div
            v-for="notification in filteredNotifications"
            :key="notification.id"
            :class="[
              'p-6 hover:bg-gray-50 transition-colors cursor-pointer',
              !notification.read ? 'bg-blue-50 hover:bg-blue-100' : ''
            ]"
            @click="handleNotificationClick(notification)"
          >
            <div class="flex items-start space-x-4">
              <!-- Notification Icon -->
              <div
                :class="[
                  'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center',
                  getNotificationIcon(notification.type).bgColor
                ]"
              >
                <component
                  :is="getNotificationIcon(notification.type).icon"
                  :class="['h-5 w-5', getNotificationIcon(notification.type).color]"
                />
              </div>

              <!-- Notification Content -->
              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between">
                  <div>
                    <p class="text-sm font-medium text-gray-900">
                      {{ notification.title }}
                    </p>
                    <p class="mt-1 text-sm text-gray-600">
                      {{ notification.message }}
                    </p>
                    <div class="mt-2 flex items-center space-x-4 text-xs text-gray-500">
                      <span>{{ formatTimeAgo(notification.created_at) }}</span>
                      <span v-if="notification.type" class="inline-flex items-center px-2 py-1 rounded-full bg-gray-100 text-gray-800">
                        {{ notification.type.replace('_', ' ') }}
                      </span>
                    </div>
                  </div>
                  
                  <div class="flex items-center space-x-2">
                    <!-- Action Buttons -->
                    <button
                      v-if="notification.action_url && notification.action_label"
                      @click.stop="handleNotificationAction(notification)"
                      class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-lg text-teal-700 bg-teal-100 hover:bg-teal-200 focus:outline-none focus:ring-2 focus:ring-teal-500"
                    >
                      {{ notification.action_label }}
                    </button>
                    
                    <!-- Mark as Read/Unread -->
                    <button
                      @click.stop="toggleReadStatus(notification)"
                      class="p-1 text-gray-400 hover:text-gray-600"
                      :title="notification.read ? 'Mark as unread' : 'Mark as read'"
                    >
                      <EyeIcon v-if="notification.read" class="h-4 w-4" />
                      <EyeSlashIcon v-else class="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <!-- Additional Data -->
                <div v-if="notification.data" class="mt-3 p-3 bg-gray-50 rounded-lg">
                  <div v-if="notification.data.order_number" class="text-sm">
                    <span class="font-medium">Order:</span> {{ notification.data.order_number }}
                  </div>
                  <div v-if="notification.data.book_title" class="text-sm">
                    <span class="font-medium">Book:</span> {{ notification.data.book_title }}
                  </div>
                  <div v-if="notification.data.amount" class="text-sm">
                    <span class="font-medium">Amount:</span> ${{ notification.data.amount }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <BellAlertIcon class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-4 text-lg font-medium text-gray-900">No notifications</h3>
          <p class="mt-2 text-sm text-gray-600">
            {{ emptyStateMessage }}
          </p>
        </div>

        <!-- Load More -->
        <div v-if="hasMore && !loading" class="border-t border-gray-200 px-6 py-4">
          <button
            @click="loadMore"
            class="w-full text-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            Load More Notifications
          </button>
        </div>
      </div>
    </div>

    <!-- Notification Settings Modal -->
    <NotificationSettingsModal
      v-if="showNotificationSettings"
      @close="showNotificationSettings = false"
      @save="handleSettingsSave"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/stores/notifications'
import {
  BellAlertIcon,
  CheckIcon,
  Cog6ToothIcon,
  EyeIcon,
  EyeSlashIcon,
  ShoppingCartIcon,
  StarIcon,
  CurrencyDollarIcon,
  TruckIcon,
  ChatBubbleLeftRightIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

import NotificationSettingsModal from '@/components/notifications/NotificationSettingsModal.vue'

const router = useRouter()
const notificationStore = useNotificationStore()

// State
const loading = ref(false)
const currentTab = ref('all')
const markingAllAsRead = ref(false)
const showNotificationSettings = ref(false)

// Tabs configuration
const tabs = computed(() => [
  { name: 'all', label: 'All', count: notificationStore.notifications.length },
  { name: 'unread', label: 'Unread', count: notificationStore.unreadCount },
  { name: 'orders', label: 'Orders', count: notificationStore.notificationsByType.orders.length },
  { name: 'reviews', label: 'Reviews', count: notificationStore.notificationsByType.reviews.length },
  { name: 'commissions', label: 'Commissions', count: notificationStore.notificationsByType.commissions.length },
  { name: 'system', label: 'System', count: notificationStore.notificationsByType.system.length }
])

// Filtered notifications based on current tab
const filteredNotifications = computed(() => {
  switch (currentTab.value) {
    case 'unread':
      return notificationStore.unreadNotifications
    case 'orders':
      return notificationStore.notificationsByType.orders
    case 'reviews':
      return notificationStore.notificationsByType.reviews
    case 'commissions':
      return notificationStore.notificationsByType.commissions
    case 'system':
      return notificationStore.notificationsByType.system
    default:
      return notificationStore.notifications
  }
})

const emptyStateMessage = computed(() => {
  switch (currentTab.value) {
    case 'unread':
      return "You're all caught up! No unread notifications."
    case 'orders':
      return 'No order notifications yet.'
    case 'reviews':
      return 'No review notifications yet.'
    case 'commissions':
      return 'No commission notifications yet.'
    case 'system':
      return 'No system notifications yet.'
    default:
      return "You don't have any notifications yet."
  }
})

const hasMore = computed(() => notificationStore.hasMore)

// Notification type icons mapping
const getNotificationIcon = (type) => {
  const icons = {
    order_placed: { icon: ShoppingCartIcon, bgColor: 'bg-blue-100', color: 'text-blue-600' },
    order_shipped: { icon: TruckIcon, bgColor: 'bg-green-100', color: 'text-green-600' },
    order_delivered: { icon: CheckIcon, bgColor: 'bg-teal-100', color: 'text-teal-600' },
    order_cancelled: { icon: ExclamationTriangleIcon, bgColor: 'bg-red-100', color: 'text-red-600' },
    review_received: { icon: StarIcon, bgColor: 'bg-yellow-100', color: 'text-yellow-600' },
    review_replied: { icon: ChatBubbleLeftRightIcon, bgColor: 'bg-purple-100', color: 'text-purple-600' },
    commission_earned: { icon: CurrencyDollarIcon, bgColor: 'bg-green-100', color: 'text-green-600' },
    payout_processed: { icon: CurrencyDollarIcon, bgColor: 'bg-teal-100', color: 'text-teal-600' },
    price_drop: { icon: BellAlertIcon, bgColor: 'bg-orange-100', color: 'text-orange-600' },
    back_in_stock: { icon: BellAlertIcon, bgColor: 'bg-blue-100', color: 'text-blue-600' },
    system: { icon: BellAlertIcon, bgColor: 'bg-gray-100', color: 'text-gray-600' }
  }
  return icons[type] || icons.system
}

// Methods
const loadNotifications = async () => {
  loading.value = true
  try {
    await notificationStore.fetchNotifications()
  } catch (error) {
    console.error('Failed to load notifications:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = async () => {
  try {
    await notificationStore.loadMoreNotifications()
  } catch (error) {
    console.error('Failed to load more notifications:', error)
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

const toggleReadStatus = async (notification) => {
  try {
    if (notification.read) {
      await notificationStore.markAsUnread(notification.id)
    } else {
      await notificationStore.markAsRead(notification.id)
    }
  } catch (error) {
    console.error('Failed to toggle read status:', error)
  }
}

const handleNotificationClick = (notification) => {
  // Mark as read when clicked
  if (!notification.read) {
    notificationStore.markAsRead(notification.id)
  }

  // Navigate if there's an action URL
  if (notification.action_url) {
    router.push(notification.action_url)
  }
}

const handleNotificationAction = (notification) => {
  if (notification.action_url) {
    router.push(notification.action_url)
  }
}

const handleSettingsSave = () => {
  showNotificationSettings.value = false
  // Reload notifications with new settings
  loadNotifications()
}

const formatTimeAgo = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`
  if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

// Lifecycle
onMounted(() => {
  loadNotifications()
})
</script>