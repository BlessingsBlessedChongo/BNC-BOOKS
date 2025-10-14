<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-gray-900">Checkout</h1>
      <p class="mt-2 text-lg text-gray-600">Complete your purchase</p>
    </div>

    <!-- Checkout Steps -->
    <div class="mb-8">
      <CheckoutSteps :steps="steps" />
    </div>

    <div class="lg:grid lg:grid-cols-12 lg:gap-x-12 lg:items-start xl:gap-x-16">
      <!-- Checkout Form -->
      <div class="lg:col-span-7">
        <!-- Shipping Address -->
        <section v-if="currentStep === 1" class="card p-6 mb-8">
          <h2 class="text-lg font-medium text-gray-900 mb-6">Shipping Information</h2>
          <AddressForm
            :address="cartStore.shippingAddress"
            :is-loading="isLoading"
            submit-button-text="Continue to Shipping"
            @submit="saveShippingAddress"
          />
        </section>

        <!-- Shipping Method -->
        <section v-if="currentStep === 2" class="card p-6 mb-8">
          <h2 class="text-lg font-medium text-gray-900 mb-6">Shipping Method</h2>
          <ShippingMethod
            :shipping-methods="shippingMethods"
            :selected-method="cartStore.shippingMethod"
            @select="selectShippingMethod"
          />
          <div class="mt-6 flex justify-between">
            <button @click="previousStep" class="btn-secondary">
              Back
            </button>
            <button @click="nextStep" class="btn-primary" :disabled="!cartStore.shippingMethod">
              Continue to Payment
            </button>
          </div>
        </section>

        <!-- Payment Method -->
        <section v-if="currentStep === 3" class="card p-6 mb-8">
          <h2 class="text-lg font-medium text-gray-900 mb-6">Payment Information</h2>
          <PaymentMethod
            :payment-method="cartStore.paymentMethod"
            @submit="savePaymentMethod"
          />
          <div class="mt-6 flex justify-between">
            <button @click="previousStep" class="btn-secondary">
              Back
            </button>
          </div>
        </section>

        <!-- Order Review -->
        <section v-if="currentStep === 4" class="card p-6 mb-8">
          <h2 class="text-lg font-medium text-gray-900 mb-6">Order Review</h2>
          <OrderReview
            :order-data="orderData"
            @submit="placeOrder"
            :is-loading="isLoading"
          />
          <div class="mt-6 flex justify-between">
            <button @click="previousStep" class="btn-secondary">
              Back
            </button>
          </div>
        </section>
      </div>

      <!-- Order Summary -->
      <div class="lg:col-span-5">
        <div class="card p-6 sticky top-8">
          <h2 class="text-lg font-medium text-gray-900 mb-4">Order Summary</h2>
          
          <!-- Cart Items -->
          <div class="flow-root">
            <ul class="-my-4 divide-y divide-gray-200">
              <li
                v-for="item in cartStore.cart"
                :key="item.id"
                class="flex items-center py-4"
              >
                <div class="flex-shrink-0 w-16 h-20 border border-gray-200 rounded-md overflow-hidden">
                  <img
                    :src="item.book.cover_image || '/placeholder-book.jpg'"
                    :alt="item.book.title"
                    class="w-full h-full object-center object-cover"
                  />
                </div>
                <div class="ml-4 flex-1">
                  <div class="flex justify-between text-base font-medium text-gray-900">
                    <h3 class="text-sm line-clamp-2">{{ item.book.title }}</h3>
                    <p class="ml-4">${{ (item.book.price * item.quantity).toFixed(2) }}</p>
                  </div>
                  <p class="mt-1 text-sm text-gray-500">Qty: {{ item.quantity }}</p>
                </div>
              </li>
            </ul>
          </div>

          <!-- Order Totals -->
          <div class="border-t border-gray-200 pt-4 mt-4">
            <div class="flex justify-between text-sm text-gray-600">
              <span>Subtotal</span>
              <span>${{ cartStore.cartSubtotal.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-sm text-gray-600 mt-2">
              <span>Shipping</span>
              <span v-if="cartStore.shippingMethod">
                ${{ cartStore.shippingCost.toFixed(2) }}
              </span>
              <span v-else class="text-gray-400">-</span>
            </div>
            <div class="flex justify-between text-sm text-gray-600 mt-2">
              <span>Tax</span>
              <span>${{ cartStore.taxAmount.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-base font-medium text-gray-900 mt-4 pt-4 border-t border-gray-200">
              <span>Total</span>
              <span>${{ cartStore.cartTotal.toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notifications'
import CheckoutSteps from '@/components/checkout/CheckoutSteps.vue'
import AddressForm from '@/components/checkout/AddressForm.vue'
import ShippingMethod from '@/components/checkout/ShippingMethod.vue'
import PaymentMethod from '@/components/checkout/PaymentMethod.vue'
import OrderReview from '@/components/checkout/OrderReview.vue'

const router = useRouter()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

const currentStep = ref(1)
const isLoading = ref(false)
const shippingMethods = ref([])

const steps = computed(() => [
  { name: 'Shipping', status: getStepStatus(1) },
  { name: 'Delivery', status: getStepStatus(2) },
  { name: 'Payment', status: getStepStatus(3) },
  { name: 'Review', status: getStepStatus(4) }
])

const orderData = computed(() => ({
  items: cartStore.cart,
  shipping_address: cartStore.shippingAddress,
  billing_address: cartStore.billingAddress,
  shipping_method: cartStore.shippingMethod,
  payment_method: cartStore.paymentMethod,
  subtotal: cartStore.cartSubtotal,
  shipping_cost: cartStore.shippingCost,
  tax_amount: cartStore.taxAmount,
  total: cartStore.cartTotal
}))

const getStepStatus = (step) => {
  if (step < currentStep.value) return 'complete'
  if (step === currentStep.value) return 'current'
  return 'upcoming'
}

const nextStep = () => {
  if (currentStep.value < 4) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const saveShippingAddress = async (address) => {
  isLoading.value = true
  cartStore.setShippingAddress(address)
  
  // If billing address is not set, use shipping address
  if (!cartStore.billingAddress) {
    cartStore.setBillingAddress(address)
  }
  
  // Load shipping methods
  const result = await cartStore.fetchShippingMethods()
  if (result.success) {
    shippingMethods.value = result.data
  }
  
  isLoading.value = false
  nextStep()
}

const selectShippingMethod = (method) => {
  cartStore.setShippingMethod(method)
}

const savePaymentMethod = async (paymentMethod) => {
  cartStore.setPaymentMethod(paymentMethod)
  nextStep()
}

const placeOrder = async () => {
  isLoading.value = true
  
  const orderData = {
    shipping_address: cartStore.shippingAddress,
    billing_address: cartStore.billingAddress,
    shipping_method_id: cartStore.shippingMethod?.id,
    payment_method: cartStore.paymentMethod
  }
  
  const result = await cartStore.createOrder(orderData)
  
  if (result.success) {
    notificationStore.success('Order placed successfully!')
    router.push(`/orders/${result.data.id}`)
  } else {
    notificationStore.error(result.error || 'Failed to place order')
  }
  
  isLoading.value = false
}

// Redirect if cart is empty
onMounted(() => {
  if (cartStore.isCartEmpty) {
    notificationStore.warning('Your cart is empty')
    router.push('/books')
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>