<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
    <!-- Book Image -->
    <div class="relative">
      <img
        :src="book.cover_image || '/images/placeholder-book.jpg'"
        :alt="book.title"
        class="w-full h-48 object-cover"
        @error="handleImageError"
      />
      
      <!-- Wishlist Button -->
      <button
        @click="toggleWishlist"
        class="absolute top-2 right-2 p-2 bg-white rounded-full shadow-sm hover:bg-gray-50 transition-colors"
        :class="{ 'text-red-500': isInWishlist }"
      >
        <HeartIcon class="h-5 w-5" :class="{ 'fill-current': isInWishlist }" />
      </button>
      
      <!-- Stock Badge -->
      <div
        v-if="book.stock_quantity === 0"
        class="absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded"
      >
        Out of Stock
      </div>
      <div
        v-else-if="book.stock_quantity < 10"
        class="absolute top-2 left-2 bg-orange-500 text-white text-xs px-2 py-1 rounded"
      >
        Low Stock
      </div>
    </div>

    <!-- Book Content -->
    <div class="p-4">
      <!-- Title and Author -->
      <h3 class="text-lg font-semibold text-gray-900 mb-1 line-clamp-2">
        <router-link :to="`/books/${book.id}`" class="hover:text-teal-600">
          {{ book.title }}
        </router-link>
      </h3>
      <p class="text-sm text-gray-600 mb-2">by {{ book.author }}</p>

      <!-- Rating -->
      <div class="flex items-center mb-3">
        <div class="flex items-center">
          <StarIcon
            v-for="star in 5"
            :key="star"
            :class="[
              'h-4 w-4',
              star <= Math.floor(book.average_rating) 
                ? 'text-yellow-400 fill-current' 
                : star <= book.average_rating
                ? 'text-yellow-400 fill-current opacity-50'
                : 'text-gray-300'
            ]"
          />
        </div>
        <span class="ml-1 text-sm text-gray-600">
          {{ book.average_rating?.toFixed(1) || '0.0' }} ({{ book.review_count || 0 }})
        </span>
      </div>

      <!-- Price -->
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center space-x-2">
          <span class="text-xl font-bold text-gray-900">
            ${{ book.price }}
          </span>
          <span
            v-if="book.original_price && book.original_price > book.price"
            class="text-sm text-gray-500 line-through"
          >
            ${{ book.original_price }}
          </span>
        </div>
        
        <!-- Discount Badge -->
        <span
          v-if="book.original_price && book.original_price > book.price"
          class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full"
        >
          -{{ calculateDiscount(book.original_price, book.price) }}%
        </span>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-2">
        <button
          @click="addToCart"
          :disabled="book.stock_quantity === 0 || addingToCart"
          class="flex-1 bg-teal-600 text-white py-2 px-4 rounded-lg hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
        </button>
        
        <button
          @click="quickView"
          class="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500 transition-colors"
        >
          <EyeIcon class="h-5 w-5 text-gray-600" />
        </button>
      </div>

      <!-- Additional Info -->
      <div class="mt-3 flex items-center justify-between text-xs text-gray-500">
        <span>{{ book.category }}</span>
        <span v-if="book.stock_quantity > 0">{{ book.stock_quantity }} in stock</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { HeartIcon, StarIcon, EyeIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  book: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['add-to-cart', 'add-to-wishlist'])

const router = useRouter()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()

// State
const addingToCart = ref(false)

// Computed
const isInWishlist = computed(() => 
  wishlistStore.isInWishlist(props.book.id)
)

// Methods
const addToCart = async () => {
  addingToCart.value = true
  try {
    await cartStore.addToCart(props.book.id, 1)
    emit('add-to-cart', props.book)
  } catch (error) {
    console.error('Failed to add to cart:', error)
  } finally {
    addingToCart.value = false
  }
}

const toggleWishlist = async () => {
  try {
    if (isInWishlist.value) {
      await wishlistStore.removeFromWishlistByBookId(props.book.id)
    } else {
      await wishlistStore.addToWishlist(props.book.id)
    }
    emit('add-to-wishlist', props.book)
  } catch (error) {
    console.error('Failed to toggle wishlist:', error)
  }
}

const quickView = () => {
  // In a real app, this would open a quick view modal
  router.push(`/books/${props.book.id}`)
}

const handleImageError = (event) => {
  event.target.src = '/images/placeholder-book.jpg'
}

const calculateDiscount = (original, current) => {
  return Math.round(((original - current) / original) * 100)
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