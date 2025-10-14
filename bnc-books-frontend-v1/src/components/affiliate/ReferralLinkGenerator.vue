<template>
  <div class="card p-6">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Referral Links</h3>
    
    <!-- Main Referral Link -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Your Main Referral Link
      </label>
      <div class="flex space-x-2">
        <input
          :value="mainReferralLink"
          type="text"
          readonly
          class="input-field flex-1 bg-gray-50"
          ref="mainLinkInput"
        />
        <button
          @click="copyToClipboard(mainReferralLink, 'mainLinkInput')"
          class="btn-secondary whitespace-nowrap"
        >
          Copy Link
        </button>
      </div>
    </div>

    <!-- Generate Campaign Link -->
    <div class="border-t border-gray-200 pt-6">
      <h4 class="text-md font-medium text-gray-900 mb-3">Generate Campaign Link</h4>
      <form @submit.prevent="generateCampaignLink" class="space-y-4">
        <div>
          <label for="campaign_name" class="block text-sm font-medium text-gray-700 mb-1">
            Campaign Name
          </label>
          <input
            id="campaign_name"
            v-model="campaignForm.name"
            type="text"
            placeholder="e.g., Summer Promotion, Book Launch"
            class="input-field"
            :class="{ 'border-red-500': errors.name }"
          />
          <p v-if="errors.name" class="mt-2 text-sm text-red-600">{{ errors.name }}</p>
          <p class="mt-1 text-sm text-gray-500">
            Track performance for specific campaigns or promotions
          </p>
        </div>

        <div class="flex space-x-2">
          <button
            type="submit"
            :disabled="affiliateStore.isLoading"
            class="btn-primary"
          >
            <span v-if="affiliateStore.isLoading">Generating...</span>
            <span v-else>Generate Link</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Campaign Links -->
    <div v-if="campaignLinks.length > 0" class="border-t border-gray-200 pt-6">
      <h4 class="text-md font-medium text-gray-900 mb-3">Your Campaign Links</h4>
      <div class="space-y-3">
        <div
          v-for="link in campaignLinks"
          :key="link.id"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">
              {{ link.url }}
            </p>
            <p class="text-xs text-gray-500">
              Campaign: {{ link.campaign || 'General' }} • 
              Clicks: {{ link.clicks || 0 }} • 
              Created: {{ formatDate(link.created_at) }}
            </p>
          </div>
          <button
            @click="copyToClipboard(link.url)"
            class="ml-2 text-primary-600 hover:text-primary-500 text-sm font-medium"
          >
            Copy
          </button>
        </div>
      </div>
    </div>

    <!-- Share Buttons -->
    <div class="border-t border-gray-200 pt-6">
      <h4 class="text-md font-medium text-gray-900 mb-3">Share Your Link</h4>
      <div class="flex flex-wrap gap-2">
        <button
          @click="shareOnFacebook"
          class="flex items-center px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
          </svg>
          Facebook
        </button>
        
        <button
          @click="shareOnTwitter"
          class="flex items-center px-3 py-2 bg-blue-400 text-white rounded-lg hover:bg-blue-500 transition-colors"
        >
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
          </svg>
          Twitter
        </button>
        
        <button
          @click="shareOnLinkedIn"
          class="flex items-center px-3 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition-colors"
        >
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
          </svg>
          LinkedIn
        </button>
        
        <button
          @click="copyToClipboard(mainReferralLink)"
          class="flex items-center px-3 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
          </svg>
          Copy Link
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useAffiliateStore } from '@/stores/affiliate'
import { useNotificationStore } from '@/stores/notifications'

const affiliateStore = useAffiliateStore()
const notificationStore = useNotificationStore()

const mainLinkInput = ref(null)
const campaignLinks = ref([])

const campaignForm = reactive({
  name: ''
})

const errors = reactive({})

const mainReferralLink = computed(() => {
  if (!affiliateStore.affiliateInfo?.referral_code) return ''
  return `${window.location.origin}/ref/${affiliateStore.affiliateInfo.referral_code}`
})

const copyToClipboard = async (text, inputRef = null) => {
  try {
    if (inputRef && mainLinkInput.value) {
      mainLinkInput.value.select()
    }
    await navigator.clipboard.writeText(text)
    notificationStore.success('Link copied to clipboard!')
  } catch (err) {
    // Fallback for older browsers
    const textArea = document.createElement('textarea')
    textArea.value = text
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    notificationStore.success('Link copied to clipboard!')
  }
}

const generateCampaignLink = async () => {
  if (!campaignForm.name.trim()) {
    errors.name = 'Campaign name is required'
    return
  }

  const result = await affiliateStore.generateReferralLink(campaignForm.name)
  if (result.success) {
    campaignLinks.value.unshift(result.data)
    campaignForm.name = ''
    notificationStore.success('Campaign link generated successfully!')
  } else {
    notificationStore.error(result.error || 'Failed to generate campaign link')
  }
}

const shareOnFacebook = () => {
  const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(mainReferralLink.value)}`
  window.open(url, '_blank', 'width=600,height=400')
}

const shareOnTwitter = () => {
  const text = `Check out these amazing books on BNC Books!`
  const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(mainReferralLink.value)}`
  window.open(url, '_blank', 'width=600,height=400')
}

const shareOnLinkedIn = () => {
  const url = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(mainReferralLink.value)}`
  window.open(url, '_blank', 'width=600,height=400')
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}
</script>