<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Create Referral Link</h3>
          <button @click="close" class="text-gray-400 hover:text-gray-500">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Referral Link Form -->
        <form @submit.prevent="generateLink" class="space-y-6">
          <!-- Campaign Name -->
          <div>
            <label for="campaign" class="block text-sm font-medium text-gray-700">Campaign Name (Optional)</label>
            <input
              id="campaign"
              v-model="form.campaign"
              type="text"
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.campaign }"
              placeholder="e.g., summer_sale_2024"
            />
            <p v-if="errors.campaign" class="mt-1 text-sm text-red-600">{{ errors.campaign[0] }}</p>
            <p class="mt-1 text-xs text-gray-500">
              Add a campaign name to track performance for specific promotions
            </p>
          </div>

          <!-- Generated Link Preview -->
          <div v-if="generatedLink" class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Your Referral Link</h4>
            <div class="flex items-center space-x-2">
              <input
                :value="generatedLink.url"
                type="text"
                readonly
                class="flex-1 input-field bg-white text-sm font-mono"
              />
              <button
                type="button"
                @click="copyToClipboard(generatedLink.url)"
                class="btn-secondary text-sm"
              >
                Copy
              </button>
            </div>
            <div class="mt-2 flex space-x-4 text-xs text-gray-500">
              <span>Campaign: {{ generatedLink.campaign || 'None' }}</span>
              <span>Created: {{ formatDate(generatedLink.created_at) }}</span>
            </div>
          </div>

          <!-- Success Message -->
          <div v-if="showSuccess" class="rounded-md bg-green-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-green-800">Referral link created successfully!</p>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="affiliateStore.error" class="rounded-md bg-red-50 p-4">
            <div class="text-sm text-red-700">{{ affiliateStore.error }}</div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="close"
              class="btn-secondary"
              :disabled="affiliateStore.isLoading"
            >
              {{ generatedLink ? 'Close' : 'Cancel' }}
            </button>
            <button
              v-if="!generatedLink"
              type="submit"
              class="btn-primary"
              :disabled="affiliateStore.isLoading"
            >
              <span v-if="affiliateStore.isLoading">Generating...</span>
              <span v-else>Generate Link</span>
            </button>
            <button
              v-else
              type="button"
              @click="createAnother"
              class="btn-primary"
            >
              Create Another
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';
import { useAffiliateStore } from '../../stores/affiliate';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['close', 'created']);

const affiliateStore = useAffiliateStore();

const form = reactive({
  campaign: ''
});

const generatedLink = ref(null);
const showSuccess = ref(false);
const errors = ref({});

const close = () => {
  emit('close');
};

const generateLink = async () => {
  errors.value = {};
  affiliateStore.clearError();
  showSuccess.value = false;

  try {
    const response = await affiliateStore.generateReferralLink(form);
    generatedLink.value = response;
    showSuccess.value = true;
    emit('created');
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    }
  }
};

const createAnother = () => {
  generatedLink.value = null;
  showSuccess.value = false;
  form.campaign = '';
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    // You could add a toast notification here
    alert('Referral link copied to clipboard!');
  } catch (err) {
    console.error('Failed to copy text: ', err);
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  });
};

// Reset form when modal opens
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    errors.value = {};
    affiliateStore.clearError();
    generatedLink.value = null;
    showSuccess.value = false;
    form.campaign = '';
  }
});
</script>