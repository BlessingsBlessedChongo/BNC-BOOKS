<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Share Your Wishlist</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>

        <!-- Share Options -->
        <div class="space-y-4">
          <!-- Share Link -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Shareable Link
            </label>
            <div class="flex space-x-2">
              <input
                ref="shareLinkInput"
                :value="shareableLink"
                type="text"
                readonly
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm bg-gray-50"
              >
              <button
                @click="copyToClipboard"
                class="px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
              >
                {{ copyButtonText }}
              </button>
            </div>
          </div>

          <!-- Share via Social Media -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Share via
            </label>
            <div class="flex space-x-3">
              <button
                v-for="platform in socialPlatforms"
                :key="platform.name"
                @click="shareOnSocial(platform)"
                class="flex-1 flex flex-col items-center p-3 border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
              >
                <component :is="platform.icon" class="h-6 w-6 mb-1" :class="platform.color" />
                <span class="text-xs text-gray-600">{{ platform.name }}</span>
              </button>
            </div>
          </div>

          <!-- Privacy Settings -->
          <div class="border-t border-gray-200 pt-4">
            <label class="flex items-center">
              <input
                v-model="isPublic"
                type="checkbox"
                class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
              >
              <span class="ml-2 text-sm text-gray-700">Make wishlist public</span>
            </label>
            <p class="mt-1 text-xs text-gray-500">
              When public, anyone with the link can view your wishlist
            </p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="mt-6 flex justify-end space-x-3">
          <button
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useNotificationStore } from '@/stores/notifications'
import {
  XMarkIcon,
  ChatBubbleLeftRightIcon,
  EnvelopeIcon,
  LinkIcon
} from '@heroicons/vue/24/outline'

const notificationStore = useNotificationStore()

// State
const isPublic = ref(false)
const copyButtonText = ref('Copy Link')

// Computed
const shareableLink = computed(() => {
  const baseUrl = window.location.origin
  return `${baseUrl}/wishlist/shared/abc123` // This would be a real shared ID in production
})

// Social platforms
const socialPlatforms = ref([
  {
    name: 'Email',
    icon: EnvelopeIcon,
    color: 'text-gray-600',
    shareUrl: (link, title) => `mailto:?subject=Check out my wishlist&body=${title}: ${link}`
  },
  {
    name: 'WhatsApp',
    icon: ChatBubbleLeftRightIcon,
    color: 'text-green-500',
    shareUrl: (link, title) => `https://wa.me/?text=${encodeURIComponent(`${title}: ${link}`)}`
  },
  {
    name: 'Copy',
    icon: LinkIcon,
    color: 'text-blue-500',
    action: 'copy'
  }
])

// Methods
const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(shareableLink.value)
    copyButtonText.value = 'Copied!'
    setTimeout(() => {
      copyButtonText.value = 'Copy Link'
    }, 2000)
    
    notificationStore.addNotification({
      type: 'success',
      title: 'Link copied',
      message: 'Wishlist link copied to clipboard'
    })
  } catch (err) {
    console.error('Failed to copy: ', err)
    notificationStore.addNotification({
      type: 'error',
      title: 'Copy failed',
      message: 'Failed to copy link to clipboard'
    })
  }
}

const shareOnSocial = (platform) => {
  if (platform.action === 'copy') {
    copyToClipboard()
    return
  }

  const title = 'My Book Wishlist'
  const url = platform.shareUrl(shareableLink.value, title)
  window.open(url, '_blank', 'width=600,height=400')
}

defineEmits(['close'])
</script>