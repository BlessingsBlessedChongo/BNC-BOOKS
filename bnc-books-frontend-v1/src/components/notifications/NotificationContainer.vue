<template>
  <div
    aria-live="assertive"
    class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:items-start sm:p-6 z-50"
  >
    <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
      <!-- Notification list -->
      <transition-group
        enter-active-class="transform ease-out duration-300 transition"
        enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
        enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        class="w-full max-w-sm space-y-2"
      >
        <div
          v-for="notification in visibleNotifications"
          :key="notification.id"
          class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5"
        >
          <div class="p-4">
            <div class="flex items-start">
              <!-- Notification Icon -->
              <div
                :class="[
                  'flex-shrink-0',
                  getNotificationIcon(notification.type).bgColor,
                  'rounded-full p-2'
                ]"
              >
                <component
                  :is="getNotificationIcon(notification.type).icon"
                  :class="['h-5 w-5', getNotificationIcon(notification.type).color]"
                />
              </div>

              <!-- Notification Content -->
              <div class="ml-3 w-0 flex-1 pt-0.5">
                <p class="text-sm font-medium text-gray-900">
                  {{ notification.title }}
                </p>
                <p class="mt-1 text-sm text-gray-500">
                  {{ notification.message }}
                </p>
                <div class="mt-3 flex space-x-4">
                  <button
                    v-if="notification.action"
                    @click="handleAction(notification)"
                    type="button"
                    class="rounded-md bg-white text-sm font-medium text-teal-600 hover:text-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
                  >
                    {{ notification.action.label }}
                  </button>
                  <button
                    @click="dismissNotification(notification.id)"
                    type="button"
                    class="rounded-md bg-white text-sm font-medium text-gray-700 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
                  >
                    Dismiss
                  </button>
                </div>
              </div>

              <!-- Close Button -->
              <div class="ml-4 flex flex-shrink-0">
                <button
                  @click="dismissNotification(notification.id)"
                  class="inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
                >
                  <span class="sr-only">Close</span>
                  <XMarkIcon class="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  XMarkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  ShoppingCartIcon,
  StarIcon,
  CurrencyDollarIcon
} from '@heroicons/vue/24/outline'

// State
const notifications = ref([])

// Computed
const visibleNotifications = computed(() => 
  notifications.value.filter(n => !n.dismissed)
)

// Notification type configuration
const notificationTypes = {
  success: {
    icon: CheckCircleIcon,
    bgColor: 'bg-green-100',
    color: 'text-green-600'
  },
  error: {
    icon: ExclamationTriangleIcon,
    bgColor: 'bg-red-100',
    color: 'text-red-600'
  },
  warning: {
    icon: ExclamationTriangleIcon,
    bgColor: 'bg-yellow-100',
    color: 'text-yellow-600'
  },
  info: {
    icon: InformationCircleIcon,
    bgColor: 'bg-blue-100',
    color: 'text-blue-600'
  },
  order: {
    icon: ShoppingCartIcon,
    bgColor: 'bg-teal-100',
    color: 'text-teal-600'
  },
  review: {
    icon: StarIcon,
    bgColor: 'bg-yellow-100',
    color: 'text-yellow-600'
  },
  commission: {
    icon: CurrencyDollarIcon,
    bgColor: 'bg-green-100',
    color: 'text-green-600'
  }
}

const router = useRouter()

// Methods
const getNotificationIcon = (type) => {
  return notificationTypes[type] || notificationTypes.info
}

const showNotification = (notification) => {
  const id = Date.now() + Math.random()
  const newNotification = {
    id,
    type: notification.type || 'info',
    title: notification.title,
    message: notification.message,
    action: notification.action,
    duration: notification.duration || 5000,
    dismissed: false
  }

  notifications.value.push(newNotification)

  // Auto-dismiss after duration
  if (newNotification.duration > 0) {
    setTimeout(() => {
      dismissNotification(id)
    }, newNotification.duration)
  }

  return id
}

const dismissNotification = (id) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) {
    notification.dismissed = true
    
    // Remove from array after animation
    setTimeout(() => {
      notifications.value = notifications.value.filter(n => n.id !== id)
    }, 300)
  }
}

const handleAction = (notification) => {
  if (notification.action?.url) {
    router.push(notification.action.url)
  }
  
  if (notification.action?.handler) {
    notification.action.handler()
  }
  
  dismissNotification(notification.id)
}

// Global notification bus
const handleGlobalNotification = (event) => {
  const { type, title, message, action, duration } = event.detail
  showNotification({ type, title, message, action, duration })
}

// Lifecycle
onMounted(() => {
  // Listen for global notification events
  window.addEventListener('bnc-notification', handleGlobalNotification)
})

onUnmounted(() => {
  window.removeEventListener('bnc-notification', handleGlobalNotification)
})

// Export methods for global use
defineExpose({
  showNotification,
  dismissNotification
})
</script>