<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <!-- Payment Method Selection -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <div
        v-for="method in paymentMethods"
        :key="method.id"
        class="relative flex cursor-pointer rounded-lg border p-4 focus:outline-none"
        :class="
          form.payment_method === method.id
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300'
        "
        @click="form.payment_method = method.id"
      >
        <div class="flex items-center">
          <div class="flex items-center h-5">
            <input
              type="radio"
              :id="`payment-method-${method.id}`"
              v-model="form.payment_method"
              :value="method.id"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
            />
          </div>
          <label
            :for="`payment-method-${method.id}`"
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

    <!-- Credit Card Form (shown when credit card is selected) -->
    <div v-if="form.payment_method === 'credit_card'" class="space-y-4 border-t pt-6">
      <div>
        <label for="card_number" class="block text-sm font-medium text-gray-700">
          Card Number
        </label>
        <input
          type="text"
          id="card_number"
          v-model="form.card_number"
          placeholder="1234 5678 9012 3456"
          class="mt-1 input-field"
          :class="{ 'border-red-500': errors.card_number }"
        />
        <p v-if="errors.card_number" class="mt-2 text-sm text-red-600">{{ errors.card_number }}</p>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="expiry_date" class="block text-sm font-medium text-gray-700">
            Expiry Date
          </label>
          <input
            type="text"
            id="expiry_date"
            v-model="form.expiry_date"
            placeholder="MM/YY"
            class="mt-1 input-field"
            :class="{ 'border-red-500': errors.expiry_date }"
          />
          <p v-if="errors.expiry_date" class="mt-2 text-sm text-red-600">{{ errors.expiry_date }}</p>
        </div>

        <div>
          <label for="cvc" class="block text-sm font-medium text-gray-700">
            CVC
          </label>
          <input
            type="text"
            id="cvc"
            v-model="form.cvc"
            placeholder="123"
            class="mt-1 input-field"
            :class="{ 'border-red-500': errors.cvc }"
          />
          <p v-if="errors.cvc" class="mt-2 text-sm text-red-600">{{ errors.cvc }}</p>
        </div>
      </div>

      <div>
        <label for="card_holder" class="block text-sm font-medium text-gray-700">
          Card Holder Name
        </label>
        <input
          type="text"
          id="card_holder"
          v-model="form.card_holder"
          class="mt-1 input-field"
          :class="{ 'border-red-500': errors.card_holder }"
        />
        <p v-if="errors.card_holder" class="mt-2 text-sm text-red-600">{{ errors.card_holder }}</p>
      </div>
    </div>

    <!-- Billing Address Same as Shipping -->
    <div class="flex items-center">
      <input
        id="billing_same_as_shipping"
        v-model="form.billing_same_as_shipping"
        type="checkbox"
        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
      />
      <label for="billing_same_as_shipping" class="ml-2 block text-sm text-gray-900">
        Billing address same as shipping address
      </label>
    </div>

    <div class="flex justify-end">
      <button
        type="submit"
        class="btn-primary"
        :disabled="!form.payment_method"
      >
        Continue to Review
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { useCartStore } from '@/stores/cart'

const cartStore = useCartStore()

const paymentMethods = [
  { id: 'credit_card', name: 'Credit Card', description: 'Pay with Visa, Mastercard, or American Express' },
  { id: 'paypal', name: 'PayPal', description: 'Pay with your PayPal account' },
  { id: 'stripe', name: 'Stripe', description: 'Secure payment via Stripe' }
]

const form = reactive({
  payment_method: '',
  card_number: '',
  expiry_date: '',
  cvc: '',
  card_holder: '',
  billing_same_as_shipping: true
})

const errors = reactive({})

const validateForm = () => {
  let isValid = true
  Object.keys(errors).forEach(key => delete errors[key])

  if (!form.payment_method) {
    errors.payment_method = 'Please select a payment method'
    isValid = false
  }

  if (form.payment_method === 'credit_card') {
    if (!form.card_number) {
      errors.card_number = 'Card number is required'
      isValid = false
    }
    if (!form.expiry_date) {
      errors.expiry_date = 'Expiry date is required'
      isValid = false
    }
    if (!form.cvc) {
      errors.cvc = 'CVC is required'
      isValid = false
    }
    if (!form.card_holder) {
      errors.card_holder = 'Card holder name is required'
      isValid = false
    }
  }

  return isValid
}

const submitForm = () => {
  if (validateForm()) {
    const paymentData = {
      method: form.payment_method,
      ...(form.payment_method === 'credit_card' && {
        card_details: {
          number: form.card_number,
          expiry: form.expiry_date,
          cvc: form.cvc,
          holder: form.card_holder
        }
      }),
      billing_same_as_shipping: form.billing_same_as_shipping
    }

    cartStore.setPaymentMethod(paymentData)
  }
}
</script>