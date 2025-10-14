<template>
  <!-- Cart Sidebar Overlay -->
  <div 
    v-if="isOpen"
    class="fixed inset-0 z-50 overflow-hidden"
    aria-labelledby="slide-over-title"
    role="dialog"
    aria-modal="true"
  >
    <!-- Background overlay -->
    <div 
      class="absolute inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
      @click="closeCart"
    ></div>

    <div class="fixed inset-y-0 right-0 pl-10 max-w-full flex">
      <!-- Cart Panel -->
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
                  @click="closeCart"
                >
                  <span class="sr-only">Close panel</span>
                  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Cart Items -->
            <div class="mt-8">
              <div class="flow-root">
                <!-- Loading State -->
                <div v-if="cartStore.isLoading" class="text-center py-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                  <p class="mt-2 text-sm text-gray-600">Loading cart...</p>
                </div>

                <!-- Empty Cart -->
                <div v-else-if="!cartStore.hasItems" class="text-center py-8">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <h3 class="mt-2 text-sm font-medium text-gray-900">Your cart is empty</h3>
                  <p class="mt-1 text-sm text-gray-500">Start adding some books to your cart!</p>
                  <div class="mt-6">
                    <button
                      type="button"
                      class="btn-primary"
                      @click="closeCart"
                    >
                      Continue Shopping
                    </button>
                  </div>
                </div>

                <!-- Cart Items List -->
                <ul v-else role="list" class="-my-6 divide-y divide-gray-200">
                  <li v-for="item in cartStore.items" :key="item.id" class="py-6 flex">
                    <!-- Book Image -->
                    <div class="flex-shrink-0 w-24 h-24 border border-gray-200 rounded-md overflow-hidden">
                      <img
                        :src="item.book.cover_image"
                        :alt="item.book.title"
                        class="w-full h-full object-center object-cover"
                        @error="handleImageError"
                      />
                    </div>

                    <div class="ml-4 flex-1 flex flex-col">
                      <div>
                        <div class="flex justify-between text-base font-medium text-gray-900">
                          <h3 class="text-sm line-clamp-2">
                            {{ item.book.title }}
                          </h3>
                          <p class="ml-4">${{ (item.book.price * item.quantity).toFixed(2) }}</p>
                        </div>
                        <p class="mt-1 text-sm text-gray-500">by {{ item.book.author }}</p>
                      </div>
                      <div class="flex-1 flex items-end justify-between text-sm">
                        <!-- Quantity Selector -->
                        <div class="flex items-center border border-gray-300 rounded">
                          <button
                            @click="updateQuantity(item, item.quantity - 1)"
                            :disabled="item.quantity <= 1"
                            class="px-2 py-1 text-gray-600 hover:text-gray-700 disabled:opacity-50"
                          >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                            </svg>
                          </button>
                          <span class="px-3 py-1 text-sm">{{ item.quantity }}</span>
                          <button
                            @click="updateQuantity(item, item.quantity + 1)"
                            :disabled="item.quantity >= item.book.stock_quantity"
                            class="px-2 py-1 text-gray-600 hover:text-gray-700 disabled:opacity-50"
                          >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                            </svg>
                          </button>
                        </div>

                        <!-- Remove Button -->
                        <button
                          type="button"
                          @click="removeItem(item)"
                          class="font-medium text-primary-600 hover:text-primary-500"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div v-if="cartStore.hasItems" class="border-t border-gray-200 py-6 px-4 sm:px-6">
            <!-- Error Message -->
            <div v-if="cartStore.error" class="mb-4 rounded-md bg-red-50 p-4">
              <div class="text-sm text-red-700">{{ cartStore.error }}</div>
            </div>

            <!-- Order Summary -->
            <div class="space-y-4">
              <div class="flex justify-between text-base font-medium text-gray-900">
                <p>Subtotal</p>
                <p>${{ cartStore.subtotal.toFixed(2) }}</p>
              </div>
              <div class="flex justify-between text-sm text-gray-600">
                <p>Shipping</p>
                <p>{{ cartStore.shippingCost === 0 ? 'Free' : `$${cartStore.shippingCost.toFixed(2)}` }}</p>
              </div>
              <div class="flex justify-between text-sm text-gray-600">
                <p>Taxes</p>
                <p>${{ cartStore.taxAmount.toFixed(2) }}</p>
              </div>
              <div class="flex justify-between text-lg font-bold text-gray-900 border-t border-gray-200 pt-4">
                <p>Total</p>
                <p>${{ cartStore.totalAmount.toFixed(2) }}</p>
              </div>

              <!-- Free Shipping Progress -->
              <div v-if="cartStore.subtotal < 50" class="bg-gray-50 rounded-lg p-3">
                <div class="flex items-center justify-between text-sm text-gray-600 mb-1">
                  <span>Free shipping on orders over $50</span>
                  <span>${{ (50 - cartStore.subtotal).toFixed(2) }} to go</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-primary-600 h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${Math.min((cartStore.subtotal / 50) * 100, 100)}%` }"
                  ></div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="mt-6 space-y-3">
                <router-link
                  to="/cart"
                  class="w-full flex justify-center items-center px-6 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-primary-600 hover:bg-primary-700"
                  @click.native="closeCart"
                >
                  View Full Cart
                </router-link>
                <router-link
                  to="/checkout"
                  class="w-full flex justify-center items-center px-6 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-primary-600 bg-primary-100 hover:bg-primary-200"
                  @click.native="closeCart"
                >
                  Proceed to Checkout
                </router-link>
              </div>
            </div>

            <div class="mt-6 flex justify-center text-sm text-center text-gray-500">
              <p>
                or
                <button
                  type="button"
                  class="text-primary-600 font-medium hover:text-primary-500"
                  @click="closeCart"
                >
                  Continue Shopping<span aria-hidden="true"> &rarr;</span>
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { watch } from 'vue';
import { useCartStore } from '../../stores/cart';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['close']);

const cartStore = useCartStore();

const closeCart = () => {
  emit('close');
};

const updateQuantity = async (item, newQuantity) => {
  await cartStore.updateCartItem(item.id, newQuantity);
};

const removeItem = async (item) => {
  await cartStore.removeFromCart(item.id);
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};

// Fetch cart when sidebar opens
watch(() => props.isOpen, async (isOpen) => {
  if (isOpen) {
    await cartStore.fetchCart();
  }
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>