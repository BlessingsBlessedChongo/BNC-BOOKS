<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Become an Affiliate</h3>
          <button @click="close" class="text-gray-400 hover:text-gray-500">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Registration Form -->
        <form @submit.prevent="registerAffiliate" class="space-y-6">
          <!-- PayPal Email -->
          <div>
            <label for="paypal_email" class="block text-sm font-medium text-gray-700">PayPal Email *</label>
            <input
              id="paypal_email"
              v-model="form.paypal_email"
              type="email"
              required
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.paypal_email }"
              placeholder="your-email@example.com"
            />
            <p v-if="errors.paypal_email" class="mt-1 text-sm text-red-600">{{ errors.paypal_email[0] }}</p>
          </div>

          <!-- Preferred Payment Method -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Preferred Payment Method</label>
            <div class="grid grid-cols-2 gap-4">
              <button
                type="button"
                @click="form.preferred_payment_method = 'paypal'"
                :class="[
                  'p-3 border rounded-lg text-center transition-colors',
                  form.preferred_payment_method === 'paypal'
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                ]"
              >
                PayPal
              </button>
              <button
                type="button"
                @click="form.preferred_payment_method = 'bank_transfer'"
                :class="[
                  'p-3 border rounded-lg text-center transition-colors',
                  form.preferred_payment_method === 'bank_transfer'
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                ]"
              >
                Bank Transfer
              </button>
            </div>
          </div>

          <!-- Bank Account Details (Conditional) -->
          <div v-if="form.preferred_payment_method === 'bank_transfer'" class="space-y-4 border-t border-gray-200 pt-4">
            <h4 class="text-sm font-medium text-gray-700">Bank Account Details</h4>
            
            <div>
              <label for="account_holder" class="block text-sm font-medium text-gray-700">Account Holder Name *</label>
              <input
                id="account_holder"
                v-model="form.bank_account.account_holder"
                type="text"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors['bank_account.account_holder'] }"
              />
              <p v-if="errors['bank_account.account_holder']" class="mt-1 text-sm text-red-600">{{ errors['bank_account.account_holder'][0] }}</p>
            </div>

            <div>
              <label for="account_number" class="block text-sm font-medium text-gray-700">Account Number *</label>
              <input
                id="account_number"
                v-model="form.bank_account.account_number"
                type="text"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors['bank_account.account_number'] }"
              />
              <p v-if="errors['bank_account.account_number']" class="mt-1 text-sm text-red-600">{{ errors['bank_account.account_number'][0] }}</p>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="routing_number" class="block text-sm font-medium text-gray-700">Routing Number *</label>
                <input
                  id="routing_number"
                  v-model="form.bank_account.routing_number"
                  type="text"
                  required
                  class="input-field mt-1"
                  :class="{ 'border-red-500': errors['bank_account.routing_number'] }"
                />
                <p v-if="errors['bank_account.routing_number']" class="mt-1 text-sm text-red-600">{{ errors['bank_account.routing_number'][0] }}</p>
              </div>
              <div>
                <label for="bank_name" class="block text-sm font-medium text-gray-700">Bank Name *</label>
                <input
                  id="bank_name"
                  v-model="form.bank_account.bank_name"
                  type="text"
                  required
                  class="input-field mt-1"
                  :class="{ 'border-red-500': errors['bank_account.bank_name'] }"
                />
                <p v-if="errors['bank_account.bank_name']" class="mt-1 text-sm text-red-600">{{ errors['bank_account.bank_name'][0] }}</p>
              </div>
            </div>
          </div>

          <!-- Terms and Conditions -->
          <div class="flex items-start">
            <div class="flex items-center h-5">
              <input
                id="terms"
                v-model="form.agree_terms"
                type="checkbox"
                required
                class="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
              />
            </div>
            <div class="ml-3 text-sm">
              <label for="terms" class="font-medium text-gray-700">I agree to the </label>
              <a href="#" class="text-primary-600 hover:text-primary-500">Affiliate Program Terms and Conditions</a>
            </div>
          </div>
          <p v-if="errors.agree_terms" class="text-sm text-red-600">{{ errors.agree_terms[0] }}</p>

          <!-- Commission Info -->
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 class="text-sm font-medium text-blue-800 mb-2">Commission Structure</h4>
            <ul class="text-sm text-blue-700 space-y-1">
              <li>• 10% commission on all referred sales</li>
              <li>• Payouts processed monthly</li>
              <li>• Minimum payout: $50</li>
              <li>• 30-day cookie tracking</li>
            </ul>
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
              Cancel
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="affiliateStore.isLoading || !form.agree_terms"
            >
              <span v-if="affiliateStore.isLoading">Registering...</span>
              <span v-else>Register as Affiliate</span>
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

const emit = defineEmits(['close', 'registered']);

const affiliateStore = useAffiliateStore();

const form = reactive({
  paypal_email: '',
  preferred_payment_method: 'paypal',
  bank_account: {
    account_holder: '',
    account_number: '',
    routing_number: '',
    bank_name: ''
  },
  agree_terms: false
});

const errors = ref({});

const close = () => {
  emit('close');
};

const registerAffiliate = async () => {
  errors.value = {};
  affiliateStore.clearError();

  // Prepare data based on payment method
  const submitData = {
    paypal_email: form.paypal_email,
    preferred_payment_method: form.preferred_payment_method
  };

  if (form.preferred_payment_method === 'bank_transfer') {
    submitData.bank_account = { ...form.bank_account };
  }

  try {
    await affiliateStore.registerAffiliate(submitData);
    emit('registered');
    close();
    
    // Reset form
    Object.assign(form, {
      paypal_email: '',
      preferred_payment_method: 'paypal',
      bank_account: {
        account_holder: '',
        account_number: '',
        routing_number: '',
        bank_name: ''
      },
      agree_terms: false
    });
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    }
  }
};

// Clear errors when modal opens
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    errors.value = {};
    affiliateStore.clearError();
  }
});
</script>