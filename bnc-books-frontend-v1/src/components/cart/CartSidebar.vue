<template>
  <div>
    <!-- Cart Toggle Button -->
    <button
      @click="isOpen = true"
      class="relative p-2 text-gray-400 hover:text-gray-500"
    >
      <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
      </svg>
      <span
        v-if="cartStore.cartCount > 0"
        class="absolute -top-1 -right-1 bg-primary-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
      >
        {{ cartStore.cartCount }}
      </span>
    </button>

    <!-- Cart Sidebar -->
    <div
      v-if="isOpen"
      class="fixed inset-0 overflow-hidden z-50"
      aria-labelledby="slide-over-title"
      role="dialog"
      aria-modal="true"
    >
      <div class="absolute inset-0 overflow-hidden">
        <!-- Background overlay -->
        <div
          class="absolute inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          @click="isOpen = false"
        ></div>

        <div class="fixed inset-y-0 right-0 pl-10 max-w-full flex">
          <div class="w-screen max-w-md">
            <div class="h-full flex flex-col bg-white shadow-xl">
              <!-- Header -->
              <div class="flex-1 py-6 overflow-y-auto px-4 sm:px-6">
                <div class="flex items-start justify-between">
                  <h2 class="text-lg font-medium text-gray-900" id="slide-over-title">
                    Shopping cart
                  </h2>
                  <div class="ml-3 h-7 flex items-center">
                    <button
                      type="button"
                      class="-m-2 p-2 text-gray-400 hover:text-gray-500"
                      @click="isOpen = false"
                    >
                      <span class="sr-only">Close panel</span>
                      <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- Cart Items -->
                <div class="mt-8">
                  <div class="flow-root">
                    <ul v-if="!cartStore.isCartEmpty" class="-my-6 divide-y divide-gray-200">
                      <li
                        v-for="item in cartStore.cart"
                        :key="item.id"
                        class="py-6 flex"
                      >
                        <!-- Book Image -->
                        <div class="flex-shrink-0 w-24 h-24 border border-gray-200 rounded-md overflow-hidden">
                          <img
                            :src="item.book.cover_image || '/placeholder-book.jpg'"
                            :alt="item.book.title"
                            class="w-full h-full object-center object-cover"
                          />
                        </div>

                        <!-- Item Details -->
                        <div class="ml-4 flex-1 flex flex-col">
                          <div>
                            <div class="flex justify-between text-base font-medium text-gray-900">
                              <h3 class="text-sm line-clamp-2">
                                {{ item.book.title }}
                              </h3>
                              <p class="ml-4">${{ (item.book.price * item.quantity).toFixed(2) }}</p>
                            </div>
                            <p class="mt-1 text-sm text-gray-500">
                              by {{ item.book.author }}
                            </p>
                          </div>
                          <div class="flex-1 flex items-end justify-between text-sm">
                            <!-- Quantity Selector -->
                            <div class="flex items-center border rounded">
                              <button
                                @click="updateQuantity(item, item.quantity - 1)"
                                :disabled="item.quantity <= 1"
                                class="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-50"
                              >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path>
                                </svg>
                              </button>
                              <span class="px-2 py-1 text-sm w-8 text-center">
                                {{ item.quantity }}
                              </span>
                              <button
                                @click="updateQuantity(item, item.quantity + 1)"
                                :disabled="item.quantity >= item.book.stock_quantity"
                                class="p-1 text-gray-500 hover:text-gray-700 disabled:opacity-50"
                              >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                                </svg>
                              </button>
                            </div>

                            <!-- Remove Button -->
                            <button
                              @click="removeItem(item)"
                              type="button"
                              class="font-medium text-primary-600 hover:text-primary-500"
                            >
                              Remove
                            </button>
                          </div>
                        </div>
                      </li>
                    </ul>

                    <!-- Empty Cart -->
                    <div v-else class="text-center py-12">
                      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
                      </svg>
                      <h3 class="mt-2 text-sm font-medium text-gray-900">Your cart is empty</h3>
                      <p class="mt-1 text-sm text-gray-500">Start adding some books to your cart!</p>
                      <div class="mt-6">
                        <button
                          @click="goToBooks"
                          class="btn-primary text-sm"
                        >
                          Continue Shopping
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Footer -->
              <div v-if="!cartStore.isCartEmpty" class="border-t border-gray-200 py-6 px-4 sm:px-6">
                <div class="flex justify-between text-base font-medium text-gray-900">
                  <p>Subtotal</p>
                  <p>${{ cartStore.cartSubtotal.toFixed(2) }}</p>
                </div>
                <p class="mt-0.5 text-sm text-gray-500">
                  Shipping and taxes calculated at checkout.
                </p>
                <div class="mt-6">
                  <button
                    @click="goToCheckout"
                    class="w-full btn-primary text-lg py-3"
                  >
                    Checkout
                  </button>
                </div>
                <div class="mt-6 flex justify-center text-sm text-center text-gray-500">
                  <p>
                    or
                    <button
                      type="button"
                      class="text-primary-600 font-medium hover:text-primary-500"
                      @click="isOpen = false"
                    >
                      Continue Shopping
                      <span aria-hidden="true"> &rarr;</span>
                    </button>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notifications'

const router = useRouter()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

const isOpen = ref(false)

const updateQuantity = async (item, newQuantity) => {
  if (newQuantity < 1 || newQuantity > item.book.stock_quantity) return
  
  const result = await cartStore.updateCartItem(item.id, newQuantity)
  if (result.success) {
    notificationStore.success('Cart updated')
  }
}

const removeItem = async (item) => {
  const result = await cartStore.removeFromCart(item.id)
  if (result.success) {
    notificationStore.success('Item removed from cart')
  }
}

const goToBooks = () => {
  isOpen.value = false
  router.push('/books')
}

const goToCheckout = () => {
  isOpen.value = false
  router.push('/checkout')
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>