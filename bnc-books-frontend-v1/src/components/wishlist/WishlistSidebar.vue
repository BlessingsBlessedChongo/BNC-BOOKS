<template>
  <!-- Wishlist Toggle Button -->
  <button
    v-if="!isOpen"
    @click="openSidebar"
    class="relative inline-flex items-center p-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
  >
    <HeartIcon class="h-5 w-5" />
    <span
      v-if="wishlistCount > 0"
      class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
    >
      {{ wishlistCount > 99 ? '99+' : wishlistCount }}
    </span>
  </button>

  <!-- Sidebar Overlay -->
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50"
    @click="closeSidebar"
  >
    <div class="absolute inset-0 bg-black bg-opacity-50 transition-opacity"></div>
    
    <!-- Sidebar Panel -->
    <div
      class="absolute right-0 top-0 h-full w-96 bg-white shadow-xl transform transition-transform"
      @click.stop
    >
      <!-- Header -->
      <div class="flex items-center justify-between p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">
          My Wishlist ({{ wishlistCount }})
        </h2>
        <button
          @click="closeSidebar"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Wishlist Items -->
      <div class="flex-1 overflow-y-auto">
        <div v-if="wishlistItems.length > 0" class="p-4 space-y-4">
          <div
            v-for="item in wishlistItems"
            :key="item.id"
            class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <!-- Book Cover -->
            <img
              :src="item.book.cover_image"
              :alt="item.book.title"
              class="w-16 h-20 object-cover rounded flex-shrink-0"
            >

            <!-- Book Details -->
            <div class="flex-1 min-w-0">
              <h3 class="text-sm font-medium text-gray-900 truncate">
                {{ item.book.title }}
              </h3>
              <p class="text-xs text-gray-600 mt-1">
                by {{ item.book.author }}
              </p>
              <div class="mt-2 flex items-center justify-between">
                <span class="text-sm font-semibold text-gray-900">
                  ${{ item.book.price }}
                </span>
                <span
                  :class="[
                    'text-xs px-2 py-1 rounded-full',
                    item.book.stock_quantity > 0
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  ]"
                >
                  {{ item.book.stock_quantity > 0 ? 'In Stock' : 'Out of Stock' }}
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex flex-col space-y-2">
              <button
                @click="addToCart(item.book)"
                :disabled="item.book.stock_quantity === 0"
                class="p-1 text-teal-600 hover:text-teal-700 disabled:opacity-50 disabled:cursor-not-allowed"
                title="Add to Cart"
              >
                <ShoppingCartIcon class="h-4 w-4" />
              </button>
              <button
                @click="removeFromWishlist(item.id)"
                class="p-1 text-gray-400 hover:text-red-600"
                title="Remove from Wishlist"
              >
                <TrashIcon class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="p-8 text-center">
          <HeartIcon class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-4 text-sm font-medium text-gray-900">Your wishlist is empty</h3>
          <p class="mt-2 text-sm text-gray-600">
            Books you save will appear here.
          </p>
          <button
            @click="browseBooks"
            class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            Browse Books
          </button>
        </div>
      </div>

      <!-- Footer Actions -->
      <div v-if="wishlistItems.length > 0" class="border-t border-gray-200 p-4 space-y-3">
        <button
          @click="addAllToCart"
          :disabled="addingAllToCart || !hasInStockItems"
          class="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ShoppingCartIcon class="h-4 w-4 mr-2" />
          {{ addingAllToCart ? 'Adding...' : `Add All (${inStockCount}) to Cart` }}
        </button>
        
        <div class="flex space-x-2">
          <button
            @click="viewFullWishlist"
            class="flex-1 inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            View All
          </button>
          <button
            @click="shareWishlist"
            class="flex-1 inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            <ShareIcon class="h-4 w-4 mr-2" />
            Share
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWishlistStore } from '@/stores/wishlist'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notifications'
import {
  HeartIcon,
  XMarkIcon,
  ShoppingCartIcon,
  TrashIcon,
  ShareIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const wishlistStore = useWishlistStore()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

// State
const isOpen = ref(false)
const addingAllToCart = ref(false)

// Computed
const wishlistItems = computed(() => wishlistStore.wishlistItems.slice(0, 10)) // Show first 10 items
const wishlistCount = computed(() => wishlistStore.wishlistItems.length)
const hasInStockItems = computed(() => wishlistStore.wishlistItems.some(item => item.book.stock_quantity > 0))
const inStockCount = computed(() => wishlistStore.wishlistItems.filter(item => item.book.stock_quantity > 0).length)

// Methods
const openSidebar = () => {
  isOpen.value = true
}

const closeSidebar = () => {
  isOpen.value = false
}

const loadWishlist = async () => {
  try {
    await wishlistStore.fetchWishlist()
  } catch (error) {
    console.error('Failed to load wishlist:', error)
  }
}

const addToCart = async (book) => {
  try {
    await cartStore.addToCart(book.id, 1)
    closeSidebar()
    notificationStore.addNotification({
      type: 'success',
      title: 'Added to cart',
      message: `${book.title} has been added to your cart`
    })
  } catch (error) {
    console.error('Failed to add to cart:', error)
    notificationStore.addNotification({
      type: 'error',
      title: 'Error',
      message: 'Failed to add item to cart'
    })
  }
}

const addAllToCart = async () => {
  addingAllToCart.value = true
  try {
    const inStockItems = wishlistStore.wishlistItems.filter(item => item.book.stock_quantity > 0)
    
    for (const item of inStockItems) {
      await cartStore.addToCart(item.book.id, 1)
    }
    
    closeSidebar()
    notificationStore.addNotification({
      type: 'success',
      title: 'Items added to cart',
      message: `${inStockItems.length} items have been added to your cart`
    })
  } catch (error) {
    console.error('Failed to add all to cart:', error)
    notificationStore.addNotification({
      type: 'error',
      title: 'Error',
      message: 'Failed to add some items to cart'
    })
  } finally {
    addingAllToCart.value = false
  }
}

const removeFromWishlist = async (wishlistItemId) => {
  try {
    await wishlistStore.removeFromWishlist(wishlistItemId)
    notificationStore.addNotification({
      type: 'success',
      title: 'Removed from wishlist',
      message: 'Item has been removed from your wishlist'
    })
  } catch (error) {
    console.error('Failed to remove from wishlist:', error)
    notificationStore.addNotification({
      type: 'error',
      title: 'Error',
      message: 'Failed to remove item from wishlist'
    })
  }
}

const viewFullWishlist = () => {
  closeSidebar()
  router.push('/wishlist')
}

const shareWishlist = () => {
  // Implementation for sharing wishlist
  closeSidebar()
  // This would open a share modal or copy link to clipboard
  notificationStore.addNotification({
    type: 'info',
    title: 'Share Feature',
    message: 'Wishlist sharing will be implemented in the next update'
  })
}

const browseBooks = () => {
  closeSidebar()
  router.push('/books')
}

// Load wishlist when component is mounted
onMounted(() => {
  loadWishlist()
})
</script>