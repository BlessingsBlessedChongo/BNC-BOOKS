<template>
  <div class="card p-6">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Request Payout</h3>
    
    <!-- Available Balance -->
    <div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm font-medium text-green-800">Available for Payout</p>
          <p class="text-2xl font-bold text-green-900">${{ availableBalance.toFixed(2) }}</p>
        </div>
        <div class="text-right">
          <p class="text-sm text-green-700">Minimum: ${{ minimumPayout }}</p>
          <p class="text-xs text-green-600">Next payout: {{ nextPayoutDate }}</p>
        </div>
      </div>
    </div>

    <!-- Payout Form -->
    <form @submit.prevent="requestPayout" class="space-y-4">
      <div>
        <label for="payout_amount" class="block text-sm font-medium text-gray-700 mb-1">
          Payout Amount
        </label>
        <div class="relative rounded-md shadow-sm">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span class="text-gray-500 sm:text-sm">$</span>
          </div>
          <input
            id="payout_amount"
            v-model="payoutForm.amount"
            type="number"
            step="0.01"
            :min="minimumPayout"
            :max="availableBalance"
            class="input-field pl-7"
            :class="{ 'border-red-500': errors.amount }"
            placeholder="0.00"
          />
        </div>
        <p v-if="errors.amount" class="mt-2 text-sm text-red-600">{{ errors.amount }}</p>
        <p class="mt-1 text-sm text-gray-500">
          Enter amount between ${{ minimumPayout }} and ${{ availableBalance.toFixed(2) }}
        </p>
      </div>

      <!-- Payment Method -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Payment Method
        </label>
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div
            v-for="method in paymentMethods"
            :key="method.id"
            class="relative flex cursor-pointer rounded-lg border p-4 focus:outline-none"
            :class="
              payoutForm.payment_method === method.id
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300'
            "
            @click="payoutForm.payment_method = method.id"
          >
            <div class="flex items-center">
              <div class="flex items-center h-5">
                <input
                  type="radio"
                  :id="`method-${method.id}`"
                  v-model="payoutForm.payment_method"
                  :value="method.id"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
                />
              </div>
              <label
                :for="`method-${method.id}`"
                class="ml-3 flex flex-col cursor-pointer"
              >
                <span class="block text-sm font-medium text-gray-900">
                  {{ method.name }}
                </span>
                <span class="block text-sm text-gray-500">
                  {{ method.description }}
                </span>
              </label>
            </div>
          </div>
        </div>
        <p v-if="errors.payment_method" class="mt-2 text-sm text-red-600">{{ errors.payment_method }}</p>
      </div>

      <!-- Account Details -->
      <div v-if="payoutForm.payment_method === 'paypal'">
        <label for="paypal_email" class="block text-sm font-medium text-gray-700 mb-1">
          PayPal Email
        </label>
        <input
          id="paypal_email"
          v-model="payoutForm.paypal_email"
          type="email"
          class="input-field"
          :class="{ 'border-red-500': errors.paypal_email }"
          placeholder="your-email@example.com"
        />
        <p v-if="errors.paypal_email" class="mt-2 text-sm text-red-600">{{ errors.paypal_email }}</p>
      </div>

      <div v-if="payoutForm.payment_method === 'bank'">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label for="account_holder" class="block text-sm font-medium text-gray-700 mb-1">
              Account Holder Name
            </label>
            <input
              id="account_holder"
              v-model="payoutForm.account_holder"
              type="text"
              class="input-field"
              :class="{ 'border-red-500': errors.account_holder }"
            />
            <p v-if="errors.account_holder" class="mt-2 text-sm text-red-600">{{ errors.account_holder }}</p>
          </div>

          <div>
            <label for="account_number" class="block text-sm font-medium text-gray-700 mb-1">
              Account Number
            </label>
            <input
              id="account_number"
              v-model="payoutForm.account_number"
              type="text"
              class="input-field"
              :class="{ 'border-red-500': errors.account_number }"
            />
            <p v-if="errors.account_number" class="mt-2 text-sm text-red-600">{{ errors.account_number }}</p>
          </div>

          <div>
            <label for="routing_number" class="block text-sm font-medium text-gray-700 mb-1">
              Routing Number
            </label>
            <input
              id="routing_number"
              v-model="payoutForm.routing_number"
              type="text"
              class="input-field"
              :class="{ 'border-red-500': errors.routing_number }"
            />
            <p v-if="errors.routing_number" class="mt-2 text-sm text-red-600">{{ errors.routing_number }}</p>
          </div>

          <div>
            <label for="bank_name" class="block text-sm font-medium text-gray-700 mb-1">
              Bank Name
            </label>
            <input
              id="bank_name"
              v-model="payoutForm.bank_name"
              type="text"
              class="input-field"
              :class="{ 'border-red-500': errors.bank_name }"
            />
            <p v-if="errors.bank_name" class="mt-2 text-sm text-red-600">{{ errors.bank_name }}</p>
          </div>
        </div>
      </div>

      <!-- Terms Agreement -->
      <div class="flex items-center">
        <input
          id="agree_terms"
          v-model="payoutForm.agree_terms"
          type="checkbox"
          class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
        />
        <label for="agree_terms" class="ml-2 block text-sm text-gray-900">
          I agree to the 
          <a href="#" class="text-primary-600 hover:text-primary-500">payout terms and conditions</a>
        </label>
      </div>
      <p v-if="errors.agree_terms" class="mt-2 text-sm text-red-600">{{ errors.agree_terms }}</p>

      <!-- Submit Button -->
      <div class="flex justify-end pt-4">
        <button
          type="submit"
          :disabled="affiliateStore.isLoading || availableBalance < minimumPayout"
          class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="affiliateStore.isLoading">Processing...</span>
          <span v-else>Request Payout</span>
        </button>
      </div>
    </form>

    <!-- Payout History -->
    <div v-if="payoutHistory.length > 0" class="border-t border-gray-200 pt-6 mt-6">
      <h4 class="text-md font-medium text-gray-900 mb-3">Recent Payouts</h4>
      <div class="space-y-2">
        <div
          v-for="payout in payoutHistory"
          :key="payout.id"
          class="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
        >
          <div>
            <p class="text-sm font-medium text-gray-900">
              ${{ payout.amount.toFixed(2) }}
            </p>
            <p class="text-xs text-gray-500">
              {{ formatDate(payout.created_at) }} • 
              <span class="capitalize">{{ payout.status }}</span>
            </p>
          </div>
          <span class="badge" :class="getPayoutStatusBadge(payout.status)">
            {{ payout.status }}
          </span>
        </div>
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

const payoutHistory = ref([])

const payoutForm = reactive({
  amount: '',
  payment_method: '',
  paypal_email: '',
  account_holder: '',
  account_number: '',
  routing_number: '',
  bank_name: '',
  agree_terms: false
})

const errors = reactive({})

const availableBalance = computed(() => affiliateStore.commissionStats.available_amount)
const minimumPayout = 50 // Minimum payout amount
const nextPayoutDate = computed(() => {
  const nextDate = new Date()
  nextDate.setDate(1)
  nextDate.setMonth(nextDate.getMonth() + 1)
  return nextDate.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
})

const paymentMethods = [
  { id: 'paypal', name: 'PayPal', description: 'Fast and secure payments' },
  { id: 'bank', name: 'Bank Transfer', description: 'Direct to your bank account' }
]

const validateForm = () => {
  let isValid = true
  Object.keys(errors).forEach(key => delete errors[key])

  const amount = parseFloat(payoutForm.amount)
  if (!amount || amount < minimumPayout || amount > availableBalance.value) {
    errors.amount = `Amount must be between $${minimumPayout} and $${availableBalance.value.toFixed(2)}`
    isValid = false
  }

  if (!payoutForm.payment_method) {
    errors.payment_method = 'Please select a payment method'
    isValid = false
  }

  if (payoutForm.payment_method === 'paypal' && !payoutForm.paypal_email) {
    errors.paypal_email = 'PayPal email is required'
    isValid = false
  }

  if (payoutForm.payment_method === 'bank') {
    if (!payoutForm.account_holder) {
      errors.account_holder = 'Account holder name is required'
      isValid = false
    }
    if (!payoutForm.account_number) {
      errors.account_number = 'Account number is required'
      isValid = false
    }
    if (!payoutForm.routing_number) {
      errors.routing_number = 'Routing number is required'
      isValid = false
    }
    if (!payoutForm.bank_name) {
      errors.bank_name = 'Bank name is required'
      isValid = false
    }
  }

  if (!payoutForm.agree_terms) {
    errors.agree_terms = 'You must agree to the terms and conditions'
    isValid = false
  }

  return isValid
}

const requestPayout = async () => {
  if (!validateForm()) return

  const result = await affiliateStore.requestPayout(parseFloat(payoutForm.amount))
  if (result.success) {
    notificationStore.success('Payout request submitted successfully!')
    // Reset form
    Object.keys(payoutForm).forEach(key => {
      if (typeof payoutForm[key] === 'boolean') {
        payoutForm[key] = false
      } else {
        payoutForm[key] = ''
      }
    })
    // Refresh commissions to update available balance
    await affiliateStore.fetchCommissions()
  } else {
    notificationStore.error(result.error || 'Failed to submit payout request')
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getPayoutStatusBadge = (status) => {
  const statusClasses = {
    pending: 'badge-warning',
    processing: 'badge-info',
    completed: 'badge-success',
    failed: 'badge-error'
  }
  return statusClasses[status] || 'badge-secondary'
}
</script>

<style scoped>
.badge {
  @apply inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium;
}

.badge-warning {
  @apply bg-yellow-100 text-yellow-800;
}

.badge-info {
  @apply bg-blue-100 text-blue-800;
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