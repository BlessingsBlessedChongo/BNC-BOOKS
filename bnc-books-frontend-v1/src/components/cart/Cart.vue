<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Shopping Cart</h1>
      <p class="mt-2 text-lg text-gray-600">Review your items and proceed to checkout</p>
    </div>

    <div v-if="cartStore.isLoading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Loading your cart...</p>
    </div>

    <div v-else-if="cartStore.isCartEmpty" class="text-center py-12">
      <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
      </svg>
      <h3 class="mt-4 text-lg font-medium text-gray-900">Your cart is empty</h3>
      <p class="mt-2 text-gray-600">Start adding some books to your cart!</p>
      <div class="mt-6">
        <router-link to="/books" class="btn-primary text-lg px-8 py-3">
          Browse Books
        </router-link>
      </div>
    </div>

    <div v-else class="lg:grid lg:grid-cols-12 lg:gap-x-12 lg:items-start xl:gap-x-16">
      <!-- Cart Items -->
      <div class="lg:col-span-7">
        <div class="card">
          <!-- Cart Header -->
          <div class="hidden sm:flex border-b border-gray-200 py-4 px-6">
            <div class="flex-1 text-sm font-medium text-gray-900">Product</div>
            <div class="text-sm font-medium text-gray-900 text-center w-1/5">Quantity</div>
            <div class="text-sm font-medium text-gray-900 text-center w-1/5">Price</div>
            <div class="text-sm font-medium text-gray-900 text-center w-1/5">Total</div>
          </div>

          <!-- Cart Items -->
          <ul class="divide-y divide-gray-200">
            <li v-for="item in cartStore.cart" :key="item.id">
              <CartItem :item="item" />
            </li>
          </ul>

          <!-- Cart Actions -->
          <div class="border-t border-gray-200 py-6 px-6 flex justify-between items-center">
            <button
              @click="clearCart"
              class="text-sm text-gray-500 hover:text-gray-700 flex items-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
              Clear Cart
            </button>
            
            <router-link to="/books" class="btn-secondary">
              Continue Shopping
            </router-link>
          </div>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="mt-8 lg:mt-0 lg:col-span-5">
        <div class="card p-6 sticky top-8">
          <h2 class="text-lg font-medium text-gray-900 mb-4">Order Summary</h2>
          
          <div class="space-y-4">
            <div class="flex justify-between">
              <span class="text-gray-600">Subtotal</span>
              <span class="text-gray-900">${{ cartStore.cartSubtotal.toFixed(2) }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-gray-600">Shipping</span>
              <span class="text-gray-600">Calculated at checkout</span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-gray-600">Tax</span>
              <span class="text-gray-600">Calculated at checkout</span>
            </div>
            
            <div class="border-t border-gray-200 pt-4 flex justify-between">
              <span class="text-lg font-medium text-gray-900">Total</span>
              <span class="text-lg font-medium text-gray-900">${{ cartStore.cartSubtotal.toFixed(2) }}</span>
            </div>
          </div>

          <div class="mt-6">
            <router-link to="/checkout" class="w-full btn-primary text-lg py-3">
              Proceed to Checkout
            </router-link>
          </div>

          <!-- Trust Indicators -->
          <div class="mt-6 border-t border-gray-200 pt-6">
            <div class="flex items-center justify-center space-x-6 text-sm text-gray-500">
              <div class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                </svg>
                Secure Checkout
              </div>
              <div class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
                Privacy Protected
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notifications'
import CartItem from '@/components/cart/CartItem.vue'

const cartStore = useCartStore()
const notificationStore = useNotificationStore()

const clearCart = async () => {
  if (confirm('Are you sure you want to clear your cart?')) {
    const result = await cartStore.clearCart()
    if (result.success) {
      notificationStore.success('Cart cleared')
    }
  }
}

onMounted(() => {
  cartStore.fetchCart()
})
</script>