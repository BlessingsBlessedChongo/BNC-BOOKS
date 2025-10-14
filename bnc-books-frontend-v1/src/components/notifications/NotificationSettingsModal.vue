<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Notification Settings</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>

        <!-- Settings Form -->
        <form @submit.prevent="saveSettings" class="space-y-6">
          <!-- Email Notifications -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-3">Email Notifications</h4>
            <div class="space-y-3">
              <label v-for="setting in emailSettings" :key="setting.key" class="flex items-center justify-between">
                <span class="text-sm text-gray-700">{{ setting.label }}</span>
                <input
                  v-model="settings.email[setting.key]"
                  type="checkbox"
                  class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
                >
              </label>
            </div>
          </div>

          <!-- Push Notifications -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-3">Push Notifications</h4>
            <div class="space-y-3">
              <label v-for="setting in pushSettings" :key="setting.key" class="flex items-center justify-between">
                <span class="text-sm text-gray-700">{{ setting.label }}</span>
                <input
                  v-model="settings.push[setting.key]"
                  type="checkbox"
                  class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
                >
              </label>
            </div>
          </div>

          <!-- SMS Notifications -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-3">SMS Notifications</h4>
            <div class="space-y-3">
              <label v-for="setting in smsSettings" :key="setting.key" class="flex items-center justify-between">
                <span class="text-sm text-gray-700">{{ setting.label }}</span>
                <input
                  v-model="settings.sms[setting.key]"
                  type="checkbox"
                  class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
                >
              </label>
            </div>
          </div>

          <!-- Notification Frequency -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-3">Notification Frequency</h4>
            <select
              v-model="settings.frequency"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
            >
              <option value="immediate">Immediate</option>
              <option value="hourly">Hourly Digest</option>
              <option value="daily">Daily Digest</option>
              <option value="weekly">Weekly Digest</option>
            </select>
          </div>

          <!-- Quiet Hours -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-3">Quiet Hours</h4>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs text-gray-600 mb-1">Start Time</label>
                <input
                  v-model="settings.quiet_hours.start"
                  type="time"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                >
              </div>
              <div>
                <label class="block text-xs text-gray-600 mb-1">End Time</label>
                <input
                  v-model="settings.quiet_hours.end"
                  type="time"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                >
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
            <button
              type="button"
              @click="$emit('close')"
              class="px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Save Settings' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

const emit = defineEmits(['close', 'save'])

// State
const settings = ref({
  email: {
    orders: true,
    reviews: true,
    commissions: true,
    promotions: false,
    system: true
  },
  push: {
    orders: true,
    reviews: false,
    commissions: true,
    promotions: false,
    system: true
  },
  sms: {
    orders: false,
    reviews: false,
    commissions: false,
    promotions: false,
    system: false
  },
  frequency: 'immediate',
  quiet_hours: {
    start: '22:00',
    end: '08:00'
  }
})

const saving = ref(false)

// Settings configuration
const emailSettings = [
  { key: 'orders', label: 'Order updates' },
  { key: 'reviews', label: 'Review notifications' },
  { key: 'commissions', label: 'Commission earnings' },
  { key: 'promotions', label: 'Promotions and offers' },
  { key: 'system', label: 'System notifications' }
]

const pushSettings = [
  { key: 'orders', label: 'Order updates' },
  { key: 'reviews', label: 'Review notifications' },
  { key: 'commissions', label: 'Commission earnings' },
  { key: 'promotions', label: 'Promotions and offers' },
  { key: 'system', label: 'System notifications' }
]

const smsSettings = [
  { key: 'orders', label: 'Order updates' },
  { key: 'reviews', label: 'Review notifications' },
  { key: 'commissions', label: 'Commission earnings' },
  { key: 'promotions', label: 'Promotions and offers' },
  { key: 'system', label: 'System notifications' }
]

// Methods
const loadSettings = async () => {
  try {
    // In a real app, this would be an API call
    const savedSettings = localStorage.getItem('bnc_notification_settings')
    if (savedSettings) {
      settings.value = { ...settings.value, ...JSON.parse(savedSettings) }
    }
  } catch (error) {
    console.error('Failed to load notification settings:', error)
  }
}

const saveSettings = async () => {
  saving.value = true
  try {
    // In a real app, this would be an API call
    localStorage.setItem('bnc_notification_settings', JSON.stringify(settings.value))
    
    // Emit save event
    emit('save', settings.value)
    emit('close')
  } catch (error) {
    console.error('Failed to save notification settings:', error)
  } finally {
    saving.value = false
  }
}

// Lifecycle
onMounted(() => {
  loadSettings()
})
</script>