<template>
  <div v-if="bookStore.isLoading" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="animate-pulse">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="aspect-[3/4] bg-gray-200 rounded-lg"></div>
        <div class="space-y-4">
          <div class="h-8 bg-gray-200 rounded w-3/4"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          <div class="h-6 bg-gray-200 rounded w-1/4"></div>
          <div class="h-32 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="bookStore.currentBook" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Breadcrumb -->
    <nav class="flex mb-8" aria-label="Breadcrumb">
      <ol class="flex items-center space-x-4">
        <li>
          <router-link to="/books" class="text-gray-400 hover:text-gray-500">Books</router-link>
        </li>
        <li class="flex items-center">
          <svg class="flex-shrink-0 h-5 w-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
          <span class="ml-4 text-sm font-medium text-gray-500 line-clamp-1">{{ bookStore.currentBook.title }}</span>
        </li>
      </ol>
    </nav>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <!-- Book Image -->
      <div class="flex flex-col items-center">
        <div class="w-full max-w-md">
          <div class="aspect-[3/4] bg-gray-200 rounded-lg overflow-hidden shadow-lg">
            <img
              v-if="bookStore.currentBook.cover_image"
              :src="bookStore.currentBook.cover_image"
              :alt="bookStore.currentBook.title"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center bg-gray-100">
              <svg class="w-24 h-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
            </div>
          </div>
          
          <!-- Additional Images -->
          <div v-if="bookStore.currentBook.additional_images?.length" class="mt-4 grid grid-cols-4 gap-2">
            <div
              v-for="(image, index) in bookStore.currentBook.additional_images"
              :key="index"
              class="aspect-square bg-gray-200 rounded cursor-pointer hover:opacity-75 transition-opacity"
              @click="selectedImage = image"
            >
              <img :src="image" class="w-full h-full object-cover rounded" />
            </div>
          </div>
        </div>
      </div>

      <!-- Book Details -->
      <div class="space-y-6">
        <!-- Title and Author -->
        <div>
          <h1 class="text-3xl font-bold text-gray-900">{{ bookStore.currentBook.title }}</h1>
          <p class="mt-2 text-xl text-gray-600">by {{ bookStore.currentBook.author }}</p>
        </div>

        <!-- Rating and Reviews -->
        <div class="flex items-center space-x-4">
          <div class="flex items-center">
            <svg
              v-for="star in 5"
              :key="star"
              class="w-5 h-5"
              :class="star <= Math.floor(bookStore.currentBook.average_rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
          <span class="text-lg text-gray-600">
            {{ bookStore.currentBook.average_rating ? bookStore.currentBook.average_rating.toFixed(1) : 'No ratings' }}
            <span class="text-gray-400">({{ bookStore.currentBook.review_count || 0 }} reviews)</span>
          </span>
        </div>

        <!-- Price and Stock -->
        <div class="space-y-2">
          <div class="flex items-baseline space-x-2">
            <span class="text-3xl font-bold text-gray-900">${{ bookStore.currentBook.price.toFixed(2) }}</span>
            <span v-if="bookStore.currentBook.original_price > bookStore.currentBook.price" class="text-xl text-gray-500 line-through">
              ${{ bookStore.currentBook.original_price.toFixed(2) }}
            </span>
            <span v-if="bookStore.currentBook.original_price > bookStore.currentBook.price" class="text-sm font-medium text-green-600">
              Save {{ calculateDiscount(bookStore.currentBook.original_price, bookStore.currentBook.price) }}%
            </span>
          </div>
          <p class="text-sm" :class="bookStore.currentBook.stock_quantity > 0 ? 'text-green-600' : 'text-red-600'">
            {{ bookStore.currentBook.stock_quantity > 0 ? `${bookStore.currentBook.stock_quantity} in stock` : 'Out of stock' }}
          </p>
        </div>

        <!-- Book Information -->
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="font-medium text-gray-900">ISBN:</span>
            <span class="ml-2 text-gray-600">{{ bookStore.currentBook.isbn }}</span>
          </div>
          <div>
            <span class="font-medium text-gray-900">Publisher:</span>
            <span class="ml-2 text-gray-600">{{ bookStore.currentBook.publisher }}</span>
          </div>
          <div>
            <span class="font-medium text-gray-900">Published:</span>
            <span class="ml-2 text-gray-600">{{ formatDate(bookStore.currentBook.publication_date) }}</span>
          </div>
          <div>
            <span class="font-medium text-gray-900">Pages:</span>
            <span class="ml-2 text-gray-600">{{ bookStore.currentBook.pages }}</span>
          </div>
        </div>

        <!-- Categories and Genres -->
        <div class="flex flex-wrap gap-2">
          <span class="badge badge-primary">{{ bookStore.currentBook.category }}</span>
          <span
            v-for="genre in bookStore.currentBook.genres"
            :key="genre"
            class="badge badge-secondary"
          >
            {{ genre }}
          </span>
        </div>

        <!-- Description -->
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Description</h3>
          <p class="text-gray-600 leading-relaxed">{{ bookStore.currentBook.description }}</p>
        </div>

        <!-- Action Buttons -->
        <div class="flex space-x-4 pt-6">
          <div class="flex items-center space-x-2">
            <label for="quantity" class="text-sm font-medium text-gray-700">Quantity:</label>
            <select
              id="quantity"
              v-model="quantity"
              class="input-field w-20"
              :disabled="bookStore.currentBook.stock_quantity === 0"
            >
              <option
                v-for="n in Math.min(bookStore.currentBook.stock_quantity, 10)"
                :key="n"
                :value="n"
              >
                {{ n }}
              </option>
            </select>
          </div>
          
          <button
            @click="addToCart"
            :disabled="bookStore.currentBook.stock_quantity === 0 || isAddingToCart"
            class="flex-1 btn-primary text-lg py-3 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isAddingToCart">Adding to Cart...</span>
            <span v-else>Add to Cart</span>
          </button>
          
          <button
            @click="toggleWishlist"
            class="p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            :class="isInWishlist ? 'text-red-500 border-red-300 bg-red-50' : 'text-gray-400'"
          >
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path v-if="isInWishlist" fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
              <path v-else fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>

        <!-- Additional Info -->
        <div class="border-t border-gray-200 pt-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
            <div>
              <span class="font-medium text-gray-900">Language:</span>
              <span class="ml-2 text-gray-600">{{ bookStore.currentBook.language }}</span>
            </div>
            <div>
              <span class="font-medium text-gray-900">Dimensions:</span>
              <span class="ml-2 text-gray-600">{{ bookStore.currentBook.dimensions }}</span>
            </div>
            <div>
              <span class="font-medium text-gray-900">Weight:</span>
              <span class="ml-2 text-gray-600">{{ bookStore.currentBook.weight }}g</span>
            </div>
            <div>
              <span class="font-medium text-gray-900">Condition:</span>
              <span class="ml-2 text-gray-600 capitalize">{{ bookStore.currentBook.condition }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Reviews Section -->
    <BookReviews :book-id="bookId" class="mt-16" />
    <!-- Add this to the book detail template, after the book information section -->

<!-- Reviews Section -->
<section class="mt-16">
  <div class="border-t border-gray-200 pt-12">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Customer Reviews</h2>
        <div class="mt-2 flex items-center space-x-4">
          <div class="flex items-center">
            <div class="flex items-center">
              <svg
                v-for="star in 5"
                :key="star"
                class="w-5 h-5"
                :class="star <= Math.floor(bookStore.currentBook.average_rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <span class="ml-2 text-lg text-gray-900">
              {{ bookStore.currentBook.average_rating ? bookStore.currentBook.average_rating.toFixed(1) : '0.0' }}
            </span>
          </div>
          <span class="text-gray-500">•</span>
          <span class="text-gray-600">{{ bookStore.currentBook.review_count || 0 }} reviews</span>
        </div>
      </div>
      
      <button
        v-if="canWriteReview"
        @click="showReviewForm = true"
        class="btn-primary"
      >
        Write a Review
      </button>
    </div>

    <!-- Review Form -->
    <div v-if="showReviewForm" class="mb-8">
      <ReviewForm
        :book-id="bookStore.currentBook.id"
        @success="handleReviewSuccess"
        @cancel="showReviewForm = false"
      />
    </div>

    <!-- Reviews List -->
    <div v-if="reviews.length > 0" class="space-y-6">
      <ReviewCard
        v-for="review in reviews"
        :key="review.id"
        :review="review"
        @edit="editReview"
      />
    </div>

    <!-- No Reviews -->
    <div v-else class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
      </svg>
      <h3 class="mt-4 text-lg font-medium text-gray-900">No reviews yet</h3>
      <p class="mt-2 text-gray-600">Be the first to share your thoughts about this book!</p>
      <div v-if="canWriteReview" class="mt-6">
        <button @click="showReviewForm = true" class="btn-primary">
          Write the First Review
        </button>
      </div>
    </div>
  </div>
</section>
  </div>

  <!-- Error State -->
  <div v-else-if="bookStore.error" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">Book not found</h3>
      <p class="mt-1 text-sm text-gray-500">{{ bookStore.error }}</p>
      <div class="mt-6">
        <router-link to="/books" class="btn-primary">
          Browse Books
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/books'
import { useWishlistStore } from '@/stores/wishlist'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notifications'
import BookReviews from '@/components/books/BookReviews.vue'
import { useReviewStore } from '@/stores/reviews'
import ReviewForm from '@/components/reviews/ReviewForm.vue'
import ReviewCard from '@/components/reviews/ReviewCard.vue'

const route = useRoute()
const bookStore = useBookStore()
const wishlistStore = useWishlistStore()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

const bookId = computed(() => route.params.id)
const quantity = ref(1)
const isAddingToCart = ref(false)
const selectedImage = ref(null)

const isInWishlist = computed(() => {
  return wishlistStore.isInWishlist(bookStore.currentBook?.id)
})

const calculateDiscount = (original, current) => {
  return Math.round(((original - current) / original) * 100)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const addToCart = async () => {
  if (!bookStore.currentBook) return
  
  isAddingToCart.value = true
  const result = await cartStore.addToCart(bookStore.currentBook.id, quantity.value)
  if (result.success) {
    notificationStore.success(`Added ${quantity.value} ${quantity.value > 1 ? 'copies' : 'copy'} to cart`)
  }
  isAddingToCart.value = false
}

const toggleWishlist = async () => {
  if (!bookStore.currentBook) return

  if (isInWishlist.value) {
    const wishlistItem = wishlistStore.wishlist.find(item => item.book.id === bookStore.currentBook.id)
    if (wishlistItem) {
      const result = await wishlistStore.removeFromWishlist(wishlistItem.id)
      if (result.success) {
        notificationStore.success('Removed from wishlist')
      }
    }
  } else {
    const result = await wishlistStore.addToWishlist(bookStore.currentBook.id)
    if (result.success) {
      notificationStore.success('Added to wishlist')
    }
  }
}

const reviewStore = useReviewStore()
const showReviewForm = ref(false)
const editingReview = ref(null)

const reviews = computed(() => reviewStore.reviews)

const canWriteReview = computed(async () => {
  if (!bookStore.currentBook) return false
  const result = await reviewStore.canReviewBook(bookStore.currentBook.id)
  return result.success && result.data.can_review
})

const handleReviewSuccess = () => {
  showReviewForm.value = false
  editingReview.value = null
  reviewStore.fetchReviews(bookStore.currentBook.id)
}

const editReview = (review) => {
  editingReview.value = review
  showReviewForm.value = true
}

onMounted(async () => {
  await bookStore.fetchBook(bookId.value)
  await wishlistStore.fetchWishlist()
  await reviewStore.fetchReviews(bookStore.currentBook.id)
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.badge {
  @apply px-3 py-1 text-xs font-medium rounded-full;
}

.badge-primary {
  @apply bg-primary-100 text-primary-800;
}

.badge-secondary {
  @apply bg-gray-100 text-gray-800;
}
</style>