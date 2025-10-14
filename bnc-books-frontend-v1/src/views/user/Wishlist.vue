<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-900">My Wishlist</h1>
        <p class="mt-2 text-sm text-gray-600">
          {{ wishlistItems.length }} item{{ wishlistItems.length !== 1 ? 's' : '' }} in your wishlist
        </p>
      </div>

      <!-- Wishlist Content -->
      <div v-if="wishlistItems.length > 0" class="bg-white rounded-lg shadow-sm border border-gray-200">
        <!-- Wishlist Actions -->
        <div class="p-6 border-b border-gray-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex items-center space-x-4">
            <button
              @click="addAllToCart"
              :disabled="addingAllToCart || !hasInStockItems"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ShoppingCartIcon class="h-4 w-4 mr-2" />
              {{ addingAllToCart ? 'Adding...' : `Add All (${inStockCount}) to Cart` }}
            </button>
            
            <button
              @click="shareWishlist"
              class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <ShareIcon class="h-4 w-4 mr-2" />
              Share Wishlist
            </button>
          </div>

          <button
            @click="clearWishlist"
            class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500 sm:self-start"
          >
            <TrashIcon class="h-4 w-4 mr-2" />
            Clear All
          </button>
        </div>

        <!-- Wishlist Items -->
        <div class="divide-y divide-gray-200">
          <div
            v-for="item in wishlistItems"
            :key="item.id"
            class="p-6 hover:bg-gray-50 transition-colors"
          >
            <div class="flex flex-col sm:flex-row sm:items-start gap-4">
              <!-- Book Image -->
              <div class="flex-shrink-0">
                <img
                  :src="item.book.cover_image || '/images/placeholder-book.jpg'"
                  :alt="item.book.title"
                  class="w-20 h-28 object-cover rounded-lg shadow-sm"
                  @error="handleImageError"
                />
              </div>

              <!-- Book Details -->
              <div class="flex-1 min-w-0">
                <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2">
                  <div class="flex-1">
                    <h3 class="text-lg font-medium text-gray-900 hover:text-teal-600">
                      <router-link :to="`/books/${item.book.id}`">
                        {{ item.book.title }}
                      </router-link>
                    </h3>
                    <p class="text-sm text-gray-600 mt-1">
                      by {{ item.book.author }}
                    </p>
                    
                    <!-- Price & Stock -->
                    <div class="mt-2 flex items-center space-x-4">
                      <span class="text-lg font-semibold text-gray-900">
                        ${{ item.book.price }}
                      </span>
                      <span
                        :class="[
                          'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                          item.book.stock_quantity > 0 
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        ]"
                      >
                        {{ item.book.stock_quantity > 0 ? 'In Stock' : 'Out of Stock' }}
                      </span>
                    </div>

                    <!-- Price Drop Alert -->
                    <div
                      v-if="item.original_price && item.original_price > item.book.price"
                      class="mt-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
                    >
                      <ArrowDownIcon class="h-3 w-3 mr-1" />
                      Price dropped from ${{ item.original_price }}
                    </div>
                  </div>

                  <!-- Actions -->
                  <div class="flex items-center space-x-3 sm:self-start">
                    <button
                      @click="addToCart(item.book)"
                      :disabled="item.book.stock_quantity === 0 || addingToCart[item.id]"
                      class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <ShoppingCartIcon class="h-4 w-4 mr-1" />
                      {{ addingToCart[item.id] ? 'Adding...' : 'Add to Cart' }}
                    </button>
                    
                    <button
                      @click="removeFromWishlist(item.id)"
                      class="inline-flex items-center p-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
                    >
                      <TrashIcon class="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <!-- Additional Info -->
                <div class="mt-4 flex flex-wrap items-center gap-4 text-sm text-gray-600">
                  <div class="flex items-center">
                    <StarIcon class="h-4 w-4 text-yellow-400 mr-1" />
                    <span>{{ item.book.average_rating?.toFixed(1) || '0.0' }}</span>
                    <span class="mx-1">•</span>
                    <span>{{ item.book.review_count || 0 }} reviews</span>
                  </div>
                  
                  <div class="flex items-center">
                    <ClockIcon class="h-4 w-4 text-gray-400 mr-1" />
                    <span>Added {{ formatDate(item.created_at) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
        <HeartIcon class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-4 text-lg font-medium text-gray-900">Your wishlist is empty</h3>
        <p class="mt-2 text-sm text-gray-600">
          Start adding books you'd like to save for later.
        </p>
        <div class="mt-6">
          <router-link
            to="/books"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            <MagnifyingGlassIcon class="h-4 w-4 mr-2" />
            Browse Books
          </router-link>
        </div>
      </div>

      <!-- Share Modal -->
      <WishlistShareModal
        v-if="showShareModal"
        :wishlist="wishlistItems"
        @close="showShareModal = false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useWishlistStore } from '@/stores/wishlist'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notifications'
import {
  HeartIcon,
  ShoppingCartIcon,
  ShareIcon,
  TrashIcon,
  ArrowDownIcon,
  ClockIcon,
  MagnifyingGlassIcon,
  StarIcon
} from '@heroicons/vue/24/outline'

import WishlistShareModal from '@/components/wishlist/WishlistShareModal.vue'

const wishlistStore = useWishlistStore()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

// State
const addingAllToCart = ref(false)
const showShareModal = ref(false)
const addingToCart = ref({})

// Computed
const wishlistItems = computed(() => wishlistStore.wishlistItems)
const hasInStockItems = computed(() => wishlistStore.wishlistItems.some(item => item.book.stock_quantity > 0))
const inStockCount = computed(() => wishlistStore.wishlistItems.filter(item => item.book.stock_quantity > 0).length)

// Methods
const loadWishlist = async () => {
  try {
    await wishlistStore.fetchWishlist()
  } catch (error) {
    console.error('Failed to load wishlist:', error)
    notificationStore.showNotification({
      type: 'error',
      title: 'Error',
      message: 'Failed to load your wishlist'
    })
  }
}

const addToCart = async (book) => {
  addingToCart.value[book.id] = true
  try {
    await cartStore.addToCart(book.id, 1)
    notificationStore.showNotification({
      type: 'success',
      title: 'Added to cart',
      message: `${book.title} has been added to your cart`,
      action: {
        label: 'View Cart',
        url: '/cart'
      }
    })
  } catch (error) {
    console.error('Failed to add to cart:', error)
    notificationStore.showNotification({
      type: 'error',
      title: 'Error',
      message: 'Failed to add item to cart'
    })
  } finally {
    addingToCart.value[book.id] = false
  }
}

const addAllToCart = async () => {
  addingAllToCart.value = true
  try {
    const inStockItems = wishlistItems.value.filter(item => item.book.stock_quantity > 0)
    
    for (const item of inStockItems) {
      await cartStore.addToCart(item.book.id, 1)
    }
    
    notificationStore.showNotification({
      type: 'success',
      title: 'Items added to cart',
      message: `${inStockItems.length} items have been added to your cart`,
      action: {
        label: 'View Cart',
        url: '/cart'
      }
    })
  } catch (error) {
    console.error('Failed to add all to cart:', error)
    notificationStore.showNotification({
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
    notificationStore.showNotification({
      type: 'success',
      title: 'Removed from wishlist',
      message: 'Item has been removed from your wishlist'
    })
  } catch (error) {
    console.error('Failed to remove from wishlist:', error)
    notificationStore.showNotification({
      type: 'error',
      title: 'Error',
      message: 'Failed to remove item from wishlist'
    })
  }
}

const clearWishlist = async () => {
  if (!confirm('Are you sure you want to clear your entire wishlist?')) {
    return
  }

  try {
    await wishlistStore.clearWishlist()
    notificationStore.showNotification({
      type: 'success',
      title: 'Wishlist cleared',
      message: 'All items have been removed from your wishlist'
    })
  } catch (error) {
    console.error('Failed to clear wishlist:', error)
    notificationStore.showNotification({
      type: 'error',
      title: 'Error',
      message: 'Failed to clear wishlist'
    })
  }
}

const shareWishlist = () => {
  showShareModal.value = true
}

const handleImageError = (event) => {
  event.target.src = '/images/placeholder-book.jpg'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 1) return 'today'
  if (diffDays === 2) return 'yesterday'
  if (diffDays <= 7) return `${diffDays - 1} days ago`
  if (diffDays <= 30) return `${Math.floor(diffDays / 7)} weeks ago`
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

// Lifecycle
onMounted(() => {
  loadWishlist()
})
</script>