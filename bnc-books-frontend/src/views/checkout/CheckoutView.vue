<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Checkout</h1>
        <p class="mt-2 text-lg text-gray-600">Complete your purchase</p>
      </div>

      <!-- Redirect if cart is empty -->
      <div v-if="!cartStore.hasItems && !cartStore.isLoading" class="text-center py-12">
        <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900">Your cart is empty</h3>
        <p class="mt-2 text-sm text-gray-500">Add some books to your cart before checking out.</p>
        <div class="mt-6">
          <router-link to="/books" class="btn-primary">
            Browse Books
          </router-link>
        </div>
      </div>

      <div v-else class="lg:grid lg:grid-cols-12 lg:gap-x-12">
        <!-- Checkout Steps -->
        <div class="lg:col-span-8">
          <!-- Step Navigation -->
          <nav aria-label="Progress" class="mb-8">
            <ol role="list" class="border border-gray-300 rounded-md divide-y divide-gray-300 md:flex md:divide-y-0">
              <li 
                v-for="(step, stepIdx) in steps" 
                :key="step.name" 
                class="relative md:flex-1 md:flex"
              >
                <div 
                  :class="[
                    'group flex items-center w-full',
                    stepIdx <= currentStep ? 'cursor-pointer' : 'cursor-not-allowed'
                  ]"
                  @click="stepIdx <= currentStep ? goToStep(stepIdx) : null"
                >
                  <span class="px-6 py-4 flex items-center text-sm font-medium">
                    <span 
                      :class="[
                        'flex-shrink-0 w-10 h-10 flex items-center justify-center border-2 rounded-full',
                        stepIdx < currentStep 
                          ? 'border-primary-600 bg-primary-600' 
                          : stepIdx === currentStep
                            ? 'border-primary-600 bg-white'
                            : 'border-gray-300 bg-white'
                      ]"
                    >
                      <span 
                        v-if="stepIdx < currentStep"
                        class="text-white"
                      >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                      </span>
                      <span 
                        v-else
                        :class="[
                          'text-sm font-medium',
                          stepIdx === currentStep ? 'text-primary-600' : 'text-gray-500'
                        ]"
                      >
                        {{ stepIdx + 1 }}
                      </span>
                    </span>
                    <span class="ml-4 text-sm font-medium" :class="stepIdx <= currentStep ? 'text-gray-900' : 'text-gray-500'">
                      {{ step.name }}
                    </span>
                  </span>
                </div>

                <div v-if="stepIdx !== steps.length - 1" class="hidden md:block absolute top-0 right-0 h-full w-5" aria-hidden="true">
                  <svg class="h-full w-full text-gray-300" viewBox="0 0 22 80" fill="none" preserveAspectRatio="none">
                    <path d="M0 -2L20 40L0 82" vector-effect="non-scaling-stroke" stroke="currentcolor" stroke-linejoin="round" />
                  </svg>
                </div>
              </li>
            </ol>
          </nav>

          <!-- Step 1: Shipping Address -->
          <div v-if="currentStep === 0" class="card p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Shipping Address</h2>
            
            <form @submit.prevent="validateShippingAddress" class="space-y-6">
              <!-- Use Saved Addresses -->
              <div v-if="savedAddresses.length > 0">
                <label class="block text-sm font-medium text-gray-700 mb-3">Choose a saved address</label>
                <div class="grid gap-4">
                  <div 
                    v-for="address in savedAddresses" 
                    :key="address.id"
                    class="border border-gray-300 rounded-lg p-4 cursor-pointer hover:border-primary-500 transition-colors"
                    :class="{ 'border-primary-500 bg-primary-50': selectedAddressId === address.id }"
                    @click="selectSavedAddress(address)"
                  >
                    <div class="flex items-start justify-between">
                      <div>
                        <p class="font-medium text-gray-900">{{ address.first_name }} {{ address.last_name }}</p>
                        <p class="text-sm text-gray-600">{{ address.street_address }}</p>
                        <p class="text-sm text-gray-600" v-if="address.apartment">{{ address.apartment }}</p>
                        <p class="text-sm text-gray-600">{{ address.city }}, {{ address.state }} {{ address.zip_code }}</p>
                        <p class="text-sm text-gray-600">{{ address.country }}</p>
                        <p class="text-sm text-gray-600">{{ address.phone }}</p>
                      </div>
                      <div class="flex items-center space-x-2">
                        <button
                          type="button"
                          @click.stop="editAddress(address)"
                          class="text-primary-600 hover:text-primary-700 text-sm"
                        >
                          Edit
                        </button>
                        <button
                          type="button"
                          @click.stop="deleteAddress(address.id)"
                          class="text-red-600 hover:text-red-700 text-sm"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="mt-4 text-center">
                  <button
                    type="button"
                    @click="showNewAddressForm = true"
                    class="text-primary-600 hover:text-primary-700 text-sm font-medium"
                  >
                    + Add New Address
                  </button>
                </div>
              </div>

              <!-- New Address Form -->
              <div v-if="savedAddresses.length === 0 || showNewAddressForm">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label for="first_name" class="block text-sm font-medium text-gray-700">First name *</label>
                    <input
                      id="first_name"
                      v-model="shippingAddress.first_name"
                      type="text"
                      required
                      class="input-field mt-1"
                      :class="{ 'border-red-500': errors.first_name }"
                    />
                    <p v-if="errors.first_name" class="mt-1 text-sm text-red-600">{{ errors.first_name[0] }}</p>
                  </div>
                  <div>
                    <label for="last_name" class="block text-sm font-medium text-gray-700">Last name *</label>
                    <input
                      id="last_name"
                      v-model="shippingAddress.last_name"
                      type="text"
                      required
                      class="input-field mt-1"
                      :class="{ 'border-red-500': errors.last_name }"
                    />
                    <p v-if="errors.last_name" class="mt-1 text-sm text-red-600">{{ errors.last_name[0] }}</p>
                  </div>
                </div>

                <div>
                  <label for="street_address" class="block text-sm font-medium text-gray-700">Street address *</label>
                  <input
                    id="street_address"
                    v-model="shippingAddress.street_address"
                    type="text"
                    required
                    class="input-field mt-1"
                    :class="{ 'border-red-500': errors.street_address }"
                  />
                  <p v-if="errors.street_address" class="mt-1 text-sm text-red-600">{{ errors.street_address[0] }}</p>
                </div>

                <div>
                  <label for="apartment" class="block text-sm font-medium text-gray-700">Apartment, suite, etc. (optional)</label>
                  <input
                    id="apartment"
                    v-model="shippingAddress.apartment"
                    type="text"
                    class="input-field mt-1"
                  />
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label for="city" class="block text-sm font-medium text-gray-700">City *</label>
                    <input
                      id="city"
                      v-model="shippingAddress.city"
                      type="text"
                      required
                      class="input-field mt-1"
                      :class="{ 'border-red-500': errors.city }"
                    />
                    <p v-if="errors.city" class="mt-1 text-sm text-red-600">{{ errors.city[0] }}</p>
                  </div>
                  <div>
                    <label for="state" class="block text-sm font-medium text-gray-700">State *</label>
                    <input
                      id="state"
                      v-model="shippingAddress.state"
                      type="text"
                      required
                      class="input-field mt-1"
                      :class="{ 'border-red-500': errors.state }"
                    />
                    <p v-if="errors.state" class="mt-1 text-sm text-red-600">{{ errors.state[0] }}</p>
                  </div>
                  <div>
                    <label for="zip_code" class="block text-sm font-medium text-gray-700">ZIP code *</label>
                    <input
                      id="zip_code"
                      v-model="shippingAddress.zip_code"
                      type="text"
                      required
                      class="input-field mt-1"
                      :class="{ 'border-red-500': errors.zip_code }"
                    />
                    <p v-if="errors.zip_code" class="mt-1 text-sm text-red-600">{{ errors.zip_code[0] }}</p>
                  </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label for="country" class="block text-sm font-medium text-gray-700">Country *</label>
                    <select
                      id="country"
                      v-model="shippingAddress.country"
                      required
                      class="input-field mt-1"
                      :class="{ 'border-red-500': errors.country }"
                    >
                      <option value="">Select country</option>
                      <option value="US">United States</option>
                      <option value="CA">Canada</option>
                      <option value="UK">United Kingdom</option>
                      <!-- Add more countries as needed -->
                    </select>
                    <p v-if="errors.country" class="mt-1 text-sm text-red-600">{{ errors.country[0] }}</p>
                  </div>
                  <div>
                    <label for="phone" class="block text-sm font-medium text-gray-700">Phone number *</label>
                    <input
                      id="phone"
                      v-model="shippingAddress.phone"
                      type="tel"
                      required
                      class="input-field mt-1"
                      :class="{ 'border-red-500': errors.phone }"
                    />
                    <p v-if="errors.phone" class="mt-1 text-sm text-red-600">{{ errors.phone[0] }}</p>
                  </div>
                </div>

                <!-- Save Address Checkbox -->
                <div class="flex items-center">
                  <input
                    id="save_address"
                    v-model="saveShippingAddress"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="save_address" class="ml-2 block text-sm text-gray-900">
                    Save this address for future orders
                  </label>
                </div>
              </div>

              <!-- Billing Address Same as Shipping -->
              <div class="flex items-center">
                <input
                  id="billing_same"
                  v-model="billingSameAsShipping"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label for="billing_same" class="ml-2 block text-sm text-gray-900">
                  Billing address is the same as shipping address
                </label>
              </div>

              <div class="flex justify-end">
                <button
                  type="submit"
                  :disabled="isLoading"
                  class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Continue to Payment
                </button>
              </div>
            </form>
          </div>

          <!-- Step 2: Payment Method -->
          <div v-if="currentStep === 1" class="card p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Payment Method</h2>
            
            <form @submit.prevent="validatePayment" class="space-y-6">
              <!-- Payment Method Selection -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-3">Select payment method</label>
                <div class="grid gap-4">
                  <div 
                    v-for="method in paymentMethods" 
                    :key="method.id"
                    class="border border-gray-300 rounded-lg p-4 cursor-pointer hover:border-primary-500 transition-colors"
                    :class="{ 'border-primary-500 bg-primary-50': selectedPaymentMethod === method.id }"
                    @click="selectedPaymentMethod = method.id"
                  >
                    <div class="flex items-center">
                      <div class="flex-shrink-0">
                        <div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                          <component :is="method.icon" class="w-4 h-4 text-gray-600" />
                        </div>
                      </div>
                      <div class="ml-3">
                        <p class="text-sm font-medium text-gray-900">{{ method.name }}</p>
                        <p class="text-sm text-gray-500">{{ method.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Credit Card Form -->
              <div v-if="selectedPaymentMethod === 'credit_card'" class="space-y-4">
                <div>
                  <label for="card_number" class="block text-sm font-medium text-gray-700">Card number</label>
                  <input
                    id="card_number"
                    v-model="paymentDetails.card_number"
                    type="text"
                    placeholder="1234 5678 9012 3456"
                    class="input-field mt-1"
                    :class="{ 'border-red-500': errors.card_number }"
                  />
                  <p v-if="errors.card_number" class="mt-1 text-sm text-red-600">{{ errors.card_number[0] }}</p>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="expiry_date" class="block text-sm font-medium text-gray-700">Expiry date</label>
                    <input
                      id="expiry_date"
                      v-model="paymentDetails.expiry_date"
                      type="text"
                      placeholder="MM/YY"
                      class="input-field mt-1"
                      :class="{ 'border-red-500': errors.expiry_date }"
                    />
                    <p v-if="errors.expiry_date" class="mt-1 text-sm text-red-600">{{ errors.expiry_date[0] }}</p>
                  </div>
                  <div>
                    <label for="cvv" class="block text-sm font-medium text-gray-700">CVV</label>
                    <input
                      id="cvv"
                      v-model="paymentDetails.cvv"
                      type="text"
                      placeholder="123"
                      class="input-field mt-1"
                      :class="{ 'border-red-500': errors.cvv }"
                    />
                    <p v-if="errors.cvv" class="mt-1 text-sm text-red-600">{{ errors.cvv[0] }}</p>
                  </div>
                </div>

                <div>
                  <label for="card_holder" class="block text-sm font-medium text-gray-700">Cardholder name</label>
                  <input
                    id="card_holder"
                    v-model="paymentDetails.card_holder"
                    type="text"
                    placeholder="John Doe"
                    class="input-field mt-1"
                    :class="{ 'border-red-500': errors.card_holder }"
                  />
                  <p v-if="errors.card_holder" class="mt-1 text-sm text-red-600">{{ errors.card_holder[0] }}</p>
                </div>
              </div>

              <!-- Billing Address (if different from shipping) -->
              <div v-if="!billingSameAsShipping && currentStep === 1">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Billing Address</h3>
                <!-- Billing address form would go here -->
                <p class="text-sm text-gray-500">Billing address form implementation...</p>
              </div>

              <div class="flex justify-between">
                <button
                  type="button"
                  @click="currentStep = 0"
                  class="btn-secondary"
                >
                  Back to Shipping
                </button>
                <button
                  type="submit"
                  :disabled="isLoading"
                  class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Review Order
                </button>
              </div>
            </form>
          </div>

          <!-- Step 3: Review Order -->
          <div v-if="currentStep === 2" class="card p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Review Your Order</h2>
            
            <!-- Order Items -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Items</h3>
              <div class="space-y-4">
                <div 
                  v-for="item in cartStore.items" 
                  :key="item.id"
                  class="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg"
                >
                  <img
                    :src="item.book.book_image"
                    :alt="item.book.title"
                    class="w-16 h-24 object-cover rounded"
                    @error="handleImageError"
                  />
                  <div class="flex-1">
                    <h4 class="font-medium text-gray-900">{{ item.book.title }}</h4>
                    <p class="text-sm text-gray-600">by {{ item.book.author }}</p>
                    <p class="text-sm text-gray-600">Quantity: {{ item.quantity }}</p>
                  </div>
                  <div class="text-right">
                    <p class="font-medium text-gray-900">${{ (item.book.price * item.quantity).toFixed(2) }}</p>
                    <p class="text-sm text-gray-600">${{ item.book.price }} each</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Shipping Address -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Shipping Address</h3>
              <div class="p-4 border border-gray-200 rounded-lg">
                <p class="font-medium">{{ shippingAddress.first_name }} {{ shippingAddress.last_name }}</p>
                <p>{{ shippingAddress.street_address }}</p>
                <p v-if="shippingAddress.apartment">{{ shippingAddress.apartment }}</p>
                <p>{{ shippingAddress.city }}, {{ shippingAddress.state }} {{ shippingAddress.zip_code }}</p>
                <p>{{ shippingAddress.country }}</p>
                <p>{{ shippingAddress.phone }}</p>
              </div>
            </div>

            <!-- Payment Method -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Payment Method</h3>
              <div class="p-4 border border-gray-200 rounded-lg">
                <p class="font-medium">{{ getPaymentMethodName(selectedPaymentMethod) }}</p>
                <p v-if="selectedPaymentMethod === 'credit_card'" class="text-sm text-gray-600">
                  Card ending in {{ paymentDetails.card_number.slice(-4) }}
                </p>
              </div>
            </div>

            <div class="flex justify-between">
              <button
                type="button"
                @click="currentStep = 1"
                class="btn-secondary"
              >
                Back to Payment
              </button>
              <button
                @click="placeOrder"
                :disabled="isLoading"
                class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="isLoading">Placing Order...</span>
                <span v-else>Place Order</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Order Summary Sidebar -->
        <div class="mt-8 lg:mt-0 lg:col-span-4">
          <div class="card p-6 sticky top-8">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Order Summary</h2>

            <!-- Order Items Preview -->
            <div class="mb-4">
              <div v-for="item in cartStore.items.slice(0, 3)" :key="item.id" class="flex items-center space-x-3 py-2">
                <img
                  :src="item.book.book_image"
                  :alt="item.book.title"
                  class="w-12 h-16 object-cover rounded"
                  @error="handleImageError"
                />
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ item.book.title }}</p>
                  <p class="text-sm text-gray-600">Qty: {{ item.quantity }}</p>
                </div>
                <p class="text-sm font-medium text-gray-900">${{ (item.book.price * item.quantity).toFixed(2) }}</p>
              </div>
              <div v-if="cartStore.items.length > 3" class="text-center py-2">
                <p class="text-sm text-gray-600">+{{ cartStore.items.length - 3 }} more items</p>
              </div>
            </div>

            <!-- Order Totals -->
            <dl class="space-y-2 border-t border-gray-200 pt-4 text-sm">
              <div class="flex justify-between">
                <dt class="text-gray-600">Subtotal</dt>
                <dd class="font-medium text-gray-900">${{ cartStore.subtotal.toFixed(2) }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">Shipping</dt>
                <dd class="font-medium text-gray-900">
                  {{ cartStore.shippingCost === 0 ? 'Free' : `$${cartStore.shippingCost.toFixed(2)}` }}
                </dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">Taxes</dt>
                <dd class="font-medium text-gray-900">${{ cartStore.taxAmount.toFixed(2) }}</dd>
              </div>
              <div class="flex justify-between border-t border-gray-200 pt-4">
                <dt class="text-base font-medium text-gray-900">Total</dt>
                <dd class="text-base font-medium text-gray-900">${{ cartStore.totalAmount.toFixed(2) }}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AppLayout from '../../layouts/AppLayout.vue';
import { useCartStore } from '../../stores/cart';
import { useAuthStore } from '../../stores/auth';

// Icons for payment methods
const CreditCardIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
    </svg>
  `
};

const PayPalIcon = {
  template: `
    <svg viewBox="0 0 24 24" fill="currentColor">
      <path d="M7.5 14.25c-.5 0-.9.4-.9.9s.4.9.9.9.9-.4.9-.9-.4-.9-.9-.9zM20.25 9.75H3.75l1.5-3h13.5l1.5 3zM21 12.15c0-.75-.6-1.35-1.35-1.35H4.35c-.75 0-1.35.6-1.35 1.35v6.3c0 .75.6 1.35 1.35 1.35h15.3c.75 0 1.35-.6 1.35-1.35v-6.3z"/>
    </svg>
  `
};

const router = useRouter();
const cartStore = useCartStore();
const authStore = useAuthStore();

// Checkout steps
const steps = [
  { name: 'Shipping', description: 'Enter shipping address' },
  { name: 'Payment', description: 'Select payment method' },
  { name: 'Review', description: 'Review your order' }
];

const currentStep = ref(0);
const isLoading = ref(false);
const errors = ref({});

// Shipping address
const shippingAddress = reactive({
  first_name: '',
  last_name: '',
  street_address: '',
  apartment: '',
  city: '',
  state: '',
  zip_code: '',
  country: 'US',
  phone: ''
});

const savedAddresses = ref([]);
const selectedAddressId = ref(null);
const showNewAddressForm = ref(false);
const saveShippingAddress = ref(false);
const billingSameAsShipping = ref(true);

// Payment
const paymentMethods = [
  { id: 'credit_card', name: 'Credit Card', description: 'Pay with your credit card', icon: CreditCardIcon },
  { id: 'paypal', name: 'PayPal', description: 'Pay with your PayPal account', icon: PayPalIcon }
];

const selectedPaymentMethod = ref('credit_card');
const paymentDetails = reactive({
  card_number: '',
  expiry_date: '',
  cvv: '',
  card_holder: ''
});

const goToStep = (stepIndex) => {
  if (stepIndex <= currentStep.value) {
    currentStep.value = stepIndex;
  }
};

const validateShippingAddress = () => {
  errors.value = {};

  // Basic validation
  if (!shippingAddress.first_name) errors.value.first_name = ['First name is required'];
  if (!shippingAddress.last_name) errors.value.last_name = ['Last name is required'];
  if (!shippingAddress.street_address) errors.value.street_address = ['Street address is required'];
  if (!shippingAddress.city) errors.value.city = ['City is required'];
  if (!shippingAddress.state) errors.value.state = ['State is required'];
  if (!shippingAddress.zip_code) errors.value.zip_code = ['ZIP code is required'];
  if (!shippingAddress.country) errors.value.country = ['Country is required'];
  if (!shippingAddress.phone) errors.value.phone = ['Phone number is required'];

  if (Object.keys(errors.value).length === 0) {
    currentStep.value = 1;
  }
};

const validatePayment = () => {
  errors.value = {};

  if (selectedPaymentMethod.value === 'credit_card') {
    if (!paymentDetails.card_number) errors.value.card_number = ['Card number is required'];
    if (!paymentDetails.expiry_date) errors.value.expiry_date = ['Expiry date is required'];
    if (!paymentDetails.cvv) errors.value.cvv = ['CVV is required'];
    if (!paymentDetails.card_holder) errors.value.card_holder = ['Cardholder name is required'];
  }

  if (Object.keys(errors.value).length === 0) {
    currentStep.value = 2;
  }
};

const selectSavedAddress = (address) => {
  selectedAddressId.value = address.id;
  Object.assign(shippingAddress, address);
};

const editAddress = (address) => {
  // Implementation for editing address
  console.log('Edit address:', address);
};

const deleteAddress = (addressId) => {
  // Implementation for deleting address
  console.log('Delete address:', addressId);
};

const getPaymentMethodName = (methodId) => {
  const method = paymentMethods.find(m => m.id === methodId);
  return method ? method.name : 'Unknown';
};

const placeOrder = async () => {
  isLoading.value = true;
  errors.value = {};

  try {
    // Prepare order data
    const orderData = {
      shipping_address: { ...shippingAddress },
      billing_address: billingSameAsShipping.value ? { ...shippingAddress } : { ...shippingAddress }, // In a real app, this would be different
      shipping_method_id: 1, // Default shipping method
      payment_method: selectedPaymentMethod.value,
      billing_same_as_shipping: billingSameAsShipping.value
    };

    // TODO: Replace with actual API call
    // const response = await api.post('/orders/', orderData);
    
    // Simulate API call
    const response = { data: { id: 'mock-order-123' } }; // Mock response for testing
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // After successful order creation, redirect to confirmation
    await cartStore.clearCart();
    router.push({
      name: 'order-confirmation',
      query: { order_id: response.data.id } // Pass order ID for lookup
    });
  } catch (error) {
    console.error('Failed to place order:', error);
    if (error.response?.data) {
      errors.value = error.response.data;
    } else {
      errors.value = { general: ['Failed to place order. Please try again.'] };
    }
  } finally {
    isLoading.value = false;
  }
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};

// Load user's saved addresses
const loadSavedAddresses = async () => {
  // TODO: Replace with actual API call
  // For now, we'll use mock data
  savedAddresses.value = [
    {
      id: 1,
      first_name: authStore.user?.first_name || 'John',
      last_name: authStore.user?.last_name || 'Doe',
      street_address: '123 Main St',
      apartment: 'Apt 4B',
      city: 'New York',
      state: 'NY',
      zip_code: '10001',
      country: 'US',
      phone: '+1-555-0123'
    }
  ];
};

onMounted(async () => {
  await cartStore.fetchCart();
  await loadSavedAddresses();
  
  // Pre-fill shipping address with user info if available
  if (authStore.user) {
    shippingAddress.first_name = authStore.user.first_name || '';
    shippingAddress.last_name = authStore.user.last_name || '';
  }
  
  // Pre-fill with first saved address if available
  if (savedAddresses.value.length > 0) {
    selectSavedAddress(savedAddresses.value[0]);
  }
});
</script>