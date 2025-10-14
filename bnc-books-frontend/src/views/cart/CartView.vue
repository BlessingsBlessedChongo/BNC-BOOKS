<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Shopping Cart</h1>
        <p class="mt-2 text-lg text-gray-600">Review your items and proceed to checkout</p>
      </div>

      <!-- Error Message -->
      <div v-if="cartStore.error" class="mb-6 rounded-md bg-red-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error</h3>
            <div class="mt-1 text-sm text-red-700">
              <p>{{ cartStore.error }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="lg:grid lg:grid-cols-12 lg:gap-x-12 lg:items-start">
        <!-- Cart Items -->
        <div class="lg:col-span-7">
          <!-- Loading State -->
          <div v-if="cartStore.isLoading" class="card p-8 text-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            <p class="mt-2 text-sm text-gray-600">Loading your cart...</p>
          </div>

          <!-- Empty Cart -->
          <div v-else-if="!cartStore.hasItems" class="card p-12 text-center">
            <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">Your cart is empty</h3>
            <p class="mt-2 text-sm text-gray-500">Start adding some books to your cart!</p>
            <div class="mt-6">
              <router-link to="/books" class="btn-primary">
                Browse Books
              </router-link>
            </div>
          </div>

          <!-- Cart Items List -->
          <div v-else class="card overflow-hidden">
            <ul role="list" class="divide-y divide-gray-200">
              <li v-for="item in cartStore.items" :key="item.id" class="p-6">
                <div class="flex flex-col sm:flex-row sm:items-center">
                  <!-- Book Image -->
                  <div class="flex-shrink-0 w-32 h-48 border border-gray-200 rounded-md overflow-hidden">
                    <img
                      :src="item.book.cover_image"
                      :alt="item.book.title"
                      class="w-full h-full object-center object-cover"
                      @error="handleImageError"
                    />
                  </div>

                  <!-- Book Details -->
                  <div class="flex-1 mt-4 sm:mt-0 sm:ml-6">
                    <div class="flex items-start justify-between">
                      <div class="flex-1 min-w-0">
                        <h3 class="text-lg font-medium text-gray-900">
                          <router-link 
                            :to="`/books/${item.book.id}`"
                            class="hover:text-primary-600 transition-colors"
                          >
                            {{ item.book.title }}
                          </router-link>
                        </h3>
                        <p class="mt-1 text-sm text-gray-600">by {{ item.book.author }}</p>
                        
                        <!-- Book Info -->
                        <div class="mt-2 flex flex-wrap gap-4 text-sm text-gray-500">
                          <span>ISBN: {{ item.book.isbn }}</span>
                          <span>Condition: {{ item.book.condition }}</span>
                          <span 
                            :class="item.book.stock_quantity > 0 ? 'text-green-600' : 'text-red-600'"
                            class="font-medium"
                          >
                            {{ item.book.stock_quantity > 0 ? 'In Stock' : 'Out of Stock' }}
                          </span>
                        </div>

                        <!-- Seller Info -->
                        <div class="mt-2 flex items-center text-sm text-gray-500">
                          <span>Sold by: </span>
                          <span class="ml-1 font-medium text-gray-700">
                            {{ item.book.seller?.store_name || 'Unknown Seller' }}
                          </span>
                        </div>
                      </div>

                      <!-- Price -->
                      <div class="ml-4 text-right">
                        <p class="text-lg font-bold text-gray-900">
                          ${{ (item.book.price * item.quantity).toFixed(2) }}
                        </p>
                        <p class="text-sm text-gray-600">${{ item.book.price }} each</p>
                      </div>
                    </div>

                    <!-- Quantity Controls -->
                    <div class="mt-6 flex items-center justify-between">
                      <div class="flex items-center space-x-4">
                        <label for="quantity" class="text-sm font-medium text-gray-700">Quantity:</label>
                        <div class="flex items-center border border-gray-300 rounded-lg">
                          <button
                            @click="updateQuantity(item, item.quantity - 1)"
                            :disabled="item.quantity <= 1"
                            class="px-3 py-2 text-gray-600 hover:text-gray-700 disabled:opacity-50 transition-colors"
                          >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                            </svg>
                          </button>
                          <span class="px-4 py-2 text-lg font-medium w-12 text-center">
                            {{ item.quantity }}
                          </span>
                          <button
                            @click="updateQuantity(item, item.quantity + 1)"
                            :disabled="item.quantity >= item.book.stock_quantity"
                            class="px-3 py-2 text-gray-600 hover:text-gray-700 disabled:opacity-50 transition-colors"
                          >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                            </svg>
                          </button>
                        </div>
                      </div>

                      <!-- Remove Button -->
                      <button
                        @click="removeItem(item)"
                        class="flex items-center text-sm font-medium text-red-600 hover:text-red-500 transition-colors"
                      >
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              </li>
            </ul>
          </div>

          <!-- Continue Shopping -->
          <div class="mt-6">
            <router-link to="/books" class="btn-secondary">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Continue Shopping
            </router-link>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="mt-16 lg:mt-0 lg:col-span-5">
          <div class="card p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Order Summary</h2>

            <div class="flow-root">
              <dl class="-my-4 text-sm divide-y divide-gray-200">
                <div class="py-4 flex items-center justify-between">
                  <dt class="text-gray-600">Subtotal</dt>
                  <dd class="font-medium text-gray-900">${{ cartStore.subtotal.toFixed(2) }}</dd>
                </div>
                <div class="py-4 flex items-center justify-between">
                  <dt class="text-gray-600">Shipping</dt>
                  <dd class="font-medium text-gray-900">
                    {{ cartStore.shippingCost === 0 ? 'Free' : `$${cartStore.shippingCost.toFixed(2)}` }}
                  </dd>
                </div>
                <div class="py-4 flex items-center justify-between">
                  <dt class="text-gray-600">Taxes</dt>
                  <dd class="font-medium text-gray-900">${{ cartStore.taxAmount.toFixed(2) }}</dd>
                </div>
                <div class="py-4 flex items-center justify-between">
                  <dt class="text-base font-medium text-gray-900">Order total</dt>
                  <dd class="text-base font-medium text-gray-900">${{ cartStore.totalAmount.toFixed(2) }}</dd>
                </div>
              </dl>
            </div>

            <!-- Free Shipping Progress -->
            <div v-if="cartStore.subtotal < 50" class="mt-6 bg-gray-50 rounded-lg p-4">
              <div class="flex items-center justify-between text-sm text-gray-600 mb-2">
                <span class="font-medium">Free shipping on orders over $50</span>
                <span>${{ (50 - cartStore.subtotal).toFixed(2) }} to go</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${Math.min((cartStore.subtotal / 50) * 100, 100)}%` }"
                ></div>
              </div>
            </div>

            <!-- Checkout Button -->
            <div class="mt-6">
              <router-link
                to="/checkout"
                class="w-full flex justify-center items-center px-6 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-primary-600 hover:bg-primary-700 transition-colors"
              >
                Proceed to Checkout
              </router-link>
            </div>

            <!-- Security Badges -->
            <div class="mt-6 text-center">
              <div class="flex justify-center items-center space-x-4 text-gray-400">
                <svg class="h-8 w-8" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                </svg>
                <span class="text-xs text-gray-500">Secure checkout</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { onMounted } from 'vue';
import AppLayout from '../../layouts/AppLayout.vue';
import { useCartStore } from '../../stores/cart';

const cartStore = useCartStore();

const updateQuantity = async (item, newQuantity) => {
  await cartStore.updateCartItem(item.id, newQuantity);
};

const removeItem = async (item) => {
  await cartStore.removeFromCart(item.id);
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/150x200?text=No+Image';
};

onMounted(async () => {
  await cartStore.fetchCart();
});
</script>