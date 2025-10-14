<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Request Payout</h3>
          <button @click="close" class="text-gray-400 hover:text-gray-500">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Payout Form -->
        <form @submit.prevent="requestPayout" class="space-y-6">
          <!-- Available Balance -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium text-gray-700">Available Balance:</span>
              <span class="text-lg font-bold text-gray-900">${{ availableBalance.toFixed(2) }}</span>
            </div>
            <p class="text-xs text-gray-500 mt-1">
              Minimum payout amount: $50.00
            </p>
          </div>

          <!-- Payout Amount -->
          <div>
            <label for="amount" class="block text-sm font-medium text-gray-700">Payout Amount *</label>
            <div class="mt-1 relative rounded-md shadow-sm">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class="text-gray-500 sm:text-sm">$</span>
              </div>
              <input
                id="amount"
                v-model="form.amount"
                type="number"
                step="0.01"
                min="50"
                :max="availableBalance"
                required
                class="input-field pl-7"
                :class="{ 'border-red-500': errors.amount }"
                placeholder="0.00"
              />
            </div>
            <p v-if="errors.amount" class="mt-1 text-sm text-red-600">{{ errors.amount[0] }}</p>
            <p class="mt-1 text-xs text-gray-500">
              Enter amount between $50.00 and ${{ availableBalance.toFixed(2) }}
            </p>
          </div>

          <!-- Payment Method -->
          <div>
            <label for="payment_method" class="block text-sm font-medium text-gray-700">Payment Method</label>
            <select
              id="payment_method"
              v-model="form.payment_method"
              required
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.payment_method }"
            >
              <option value="paypal">PayPal</option>
              <option value="bank_transfer">Bank Transfer</option>
            </select>
            <p v-if="errors.payment_method" class="mt-1 text-sm text-red-600">{{ errors.payment_method[0] }}</p>
          </div>

          <!-- Processing Info -->
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 class="text-sm font-medium text-blue-800 mb-2">Payout Information</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• Payouts are processed within 3-5 business days</li>
              <li>• Minimum payout amount: $50.00</li>
              <li>• No transaction fees for payouts over $100</li>
              <li v-if="form.payment_method === 'paypal'">• Will be sent to your registered PayPal email</li>
              <li v-if="form.payment_method === 'bank_transfer'">• Will be transferred to your registered bank account</li>
            </ul>
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
                <p class="text-sm font-medium text-green-800">Payout request submitted successfully!</p>
                <p class="mt-1 text-sm text-green-700">
                  Your payout of ${{ form.amount }} will be processed within 3-5 business days.
                </p>
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
              {{ showSuccess ? 'Close' : 'Cancel' }}
            </button>
            <button
              v-if="!showSuccess"
              type="submit"
              class="btn-primary"
              :disabled="affiliateStore.isLoading || form.amount < 50 || form.amount > availableBalance"
            >
              <span v-if="affiliateStore.isLoading">Processing...</span>
              <span v-else>Request Payout</span>
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
  },
  availableBalance: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['close', 'requested']);

const affiliateStore = useAffiliateStore();

const form = reactive({
  amount: 0,
  payment_method: 'paypal'
});

const showSuccess = ref(false);
const errors = ref({});

const close = () => {
  emit('close');
};

const requestPayout = async () => {
  errors.value = {};
  affiliateStore.clearError();

  if (form.amount < 50) {
    errors.value.amount = ['Minimum payout amount is $50.00'];
    return;
  }

  if (form.amount > props.availableBalance) {
    errors.value.amount = ['Payout amount cannot exceed available balance'];
    return;
  }

  try {
    await affiliateStore.requestPayout(form);
    showSuccess.value = true;
    emit('requested');
    
    // Reset form after delay
    setTimeout(() => {
      if (showSuccess.value) {
        close();
      }
    }, 3000);
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    }
  }
};

// Initialize form when modal opens
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    errors.value = {};
    affiliateStore.clearError();
    showSuccess.value = false;
    form.amount = Math.min(props.availableBalance, Math.max(50, props.availableBalance));
    form.payment_method = 'paypal';
  }
});

// Update amount when available balance changes
watch(() => props.availableBalance, (newBalance) => {
  if (props.isOpen) {
    form.amount = Math.min(newBalance, Math.max(50, newBalance));
  }
});
</script>