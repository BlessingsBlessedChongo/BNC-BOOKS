<template>
  <AppLayout>
    <div v-if="isLoading" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="animate-pulse">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <!-- Image Skeleton -->
          <div class="bg-gray-300 h-96 rounded-lg"></div>
          <!-- Content Skeleton -->
          <div class="space-y-4">
            <div class="h-8 bg-gray-300 rounded w-3/4"></div>
            <div class="h-4 bg-gray-300 rounded w-1/2"></div>
            <div class="h-6 bg-gray-300 rounded w-1/4"></div>
            <div class="h-32 bg-gray-300 rounded"></div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="book" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Error Message -->
      <div v-if="reviewsStore.error" class="rounded-md bg-red-50 p-4 mb-6">
        <div class="text-sm text-red-700">
          {{ reviewsStore.error }}
        </div>
      </div>

      <!-- Breadcrumb -->
      <nav class="flex mb-8" aria-label="Breadcrumb">
        <ol class="flex items-center space-x-4">
          <li>
            <router-link to="/books" class="text-gray-400 hover:text-gray-500">
              <svg class="flex-shrink-0 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span class="sr-only">Home</span>
            </router-link>
          </li>
          <li>
            <div class="flex items-center">
              <svg class="flex-shrink-0 h-5 w-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
              <router-link to="/books" class="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700">
                Books
              </router-link>
            </div>
          </li>
          <li>
            <div class="flex items-center">
              <svg class="flex-shrink-0 h-5 w-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
              <span class="ml-4 text-sm font-medium text-gray-500">{{ book.title }}</span>
            </div>
          </li>
        </ol>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Book Images -->
        <div class="space-y-4">
          <!-- Main Image -->
          <div class="bg-gray-100 rounded-lg overflow-hidden">
            <img
              :src="currentImage"
              :alt="book.title"
              class="w-full h-96 object-cover"
              @error="handleImageError"
            />
          </div>
          
          <!-- Additional Images -->
          <div v-if="book.additional_images && book.additional_images.length > 0" class="grid grid-cols-4 gap-2">
            <div 
              v-for="(image, index) in book.additional_images" 
              :key="index"
              class="bg-gray-100 rounded-md overflow-hidden cursor-pointer"
              @click="currentImage = image"
            >
              <img
                :src="image"
                :alt="`${book.title} - Image ${index + 1}`"
                class="w-full h-20 object-cover"
              />
            </div>
          </div>
        </div>

        <!-- Book Details -->
        <div class="space-y-6">
          <!-- Title and Author -->
          <div>
            <h1 class="text-3xl font-bold text-gray-900">{{ book.title }}</h1>
            <p class="mt-2 text-xl text-gray-600">by {{ book.author }}</p>
          </div>

          <!-- Rating and Reviews -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center">
              <div v-for="n in 5" :key="n" class="mr-1">
                <svg 
                  class="h-5 w-5" 
                  :class="n <= Math.floor(book.average_rating) ? 'text-yellow-400' : 'text-gray-300'"
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </div>
              <span class="ml-2 text-sm text-gray-600">
                {{ book.average_rating?.toFixed(1) || '0.0' }}
              </span>
            </div>
            <span class="text-gray-400">•</span>
            <span class="text-sm text-gray-600">{{ book.review_count || 0 }} reviews</span>
            <span class="text-gray-400">•</span>
            <span class="text-sm text-gray-600">{{ book.total_sales || 0 }} sold</span>
          </div>

          <!-- Price -->
          <div class="flex items-center space-x-4">
            <span class="text-3xl font-bold text-gray-900">${{ book.price }}</span>
            <span v-if="hasDiscount" class="text-xl text-gray-500 line-through">${{ book.original_price }}</span>
            <span v-if="hasDiscount" class="bg-red-100 text-red-800 px-2 py-1 rounded text-sm font-medium">
              Save {{ discountPercentage }}%
            </span>
          </div>

          <!-- Stock Status -->
          <div>
            <span 
              :class="book.stock_quantity > 0 ? 'text-green-600' : 'text-red-600'"
              class="text-sm font-medium"
            >
              {{ book.stock_quantity > 0 ? `${book.stock_quantity} in stock` : 'Out of stock' }}
            </span>
          </div>

          <!-- Add to Cart -->
          <div class="flex space-x-4" v-if="book.stock_quantity > 0">
            <div class="flex items-center border border-gray-300 rounded-lg">
              <button 
                @click="decrementQuantity"
                :disabled="quantity <= 1"
                class="px-4 py-2 text-gray-600 hover:text-gray-700 disabled:opacity-50"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                </svg>
              </button>
              <span class="px-4 py-2 text-lg font-medium">{{ quantity }}</span>
              <button 
                @click="incrementQuantity"
                :disabled="quantity >= book.stock_quantity"
                class="px-4 py-2 text-gray-600 hover:text-gray-700 disabled:opacity-50"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </button>
            </div>
            <button 
              @click="addToCart"
              class="flex-1 btn-primary text-lg py-3"
            >
              Add to Cart
            </button>
          </div>

          <!-- Seller Info -->
          <div class="border-t border-gray-200 pt-6">
            <h3 class="text-sm font-medium text-gray-900 mb-2">Sold by</h3>
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                <span class="text-primary-600 font-semibold text-sm">
                  {{ book.seller?.store_name?.charAt(0) || 'S' }}
                </span>
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ book.seller?.store_name || 'Unknown Seller' }}</p>
                <p class="text-sm text-gray-600">Member since {{ formatDate(book.seller?.user?.date_joined) }}</p>
              </div>
            </div>
          </div>

          <!-- Book Details -->
          <div class="border-t border-gray-200 pt-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Details</h3>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span class="font-medium text-gray-500">ISBN:</span>
                <p class="text-gray-900">{{ book.isbn }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Publisher:</span>
                <p class="text-gray-900">{{ book.publisher }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Publication Date:</span>
                <p class="text-gray-900">{{ formatDate(book.publication_date) }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Pages:</span>
                <p class="text-gray-900">{{ book.pages }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Language:</span>
                <p class="text-gray-900">{{ book.language }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Condition:</span>
                <p class="text-gray-900 capitalize">{{ book.condition }}</p>
              </div>
            </div>
          </div>

          <!-- Genres -->
          <div class="border-t border-gray-200 pt-6">
            <h3 class="text-sm font-medium text-gray-900 mb-2">Genres</h3>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="genre in book.genres" 
                :key="genre"
                class="inline-block bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
              >
                {{ genre }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Description Section -->
      <div class="mt-12 border-t border-gray-200 pt-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Description</h2>
        <div class="prose max-w-none">
          <p class="text-gray-600 leading-relaxed">{{ book.description }}</p>
        </div>
      </div>

      <!-- Reviews Section -->
      <div class="mt-12 border-t border-gray-200 pt-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Customer Reviews</h2>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Review Summary -->
          <div class="lg:col-span-1">
            <div class="card p-6 text-center">
              <div class="text-5xl font-bold text-gray-900 mb-2">
                {{ book.average_rating?.toFixed(1) || '0.0' }}
              </div>
              <div class="flex justify-center mb-2">
                <div v-for="n in 5" :key="n" class="mr-1">
                  <svg 
                    class="h-5 w-5" 
                    :class="n <= Math.floor(book.average_rating) ? 'text-yellow-400' : 'text-gray-300'"
                    fill="currentColor" 
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
              </div>
              <p class="text-sm text-gray-600">Based on {{ book.review_count || 0 }} reviews</p>
              <button 
                v-if="authStore.isAuthenticated"
                @click="showReviewForm = true"
                class="mt-4 w-full btn-primary"
              >
                Write a Review
              </button>
            </div>
          </div>

          <!-- Reviews List -->
          <div class="lg:col-span-2">
            <div v-if="reviews.length === 0" class="text-center py-8">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
              <h3 class="mt-4 text-sm font-medium text-gray-900">No reviews yet</h3>
              <p class="mt-1 text-sm text-gray-500">Be the first to review this book!</p>
            </div>
            <div v-else class="space-y-6">
              <div 
                v-for="review in reviews" 
                :key="review.id"
                class="card p-6"
              >
                <div class="flex items-start justify-between mb-4">
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                      <span class="text-primary-600 font-semibold text-sm">
                        {{ review.user.first_name?.charAt(0) }}{{ review.user.last_name?.charAt(0) }}
                      </span>
                    </div>
                    <div>
                      <p class="font-medium text-gray-900">
                        {{ review.user.first_name }} {{ review.user.last_name }}
                      </p>
                      <p class="text-sm text-gray-500">{{ formatDate(review.created_at) }}</p>
                    </div>
                  </div>
                  <div class="flex items-center">
                    <div v-for="n in 5" :key="n" class="mr-1">
                      <svg 
                        class="h-4 w-4" 
                        :class="n <= review.rating ? 'text-yellow-400' : 'text-gray-300'"
                        fill="currentColor" 
                        viewBox="0 0 20 20"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    </div>
                  </div>
                </div>
                <h4 class="font-semibold text-gray-900 mb-2">{{ review.title }}</h4>
                <p class="text-gray-600 mb-4">{{ review.comment }}</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm" v-if="review.pros || review.cons">
                  <div v-if="review.pros" class="bg-green-50 p-3 rounded-lg">
                    <span class="font-medium text-green-800">Pros:</span>
                    <p class="text-green-700 mt-1">{{ review.pros }}</p>
                  </div>
                  <div v-if="review.cons" class="bg-red-50 p-3 rounded-lg">
                    <span class="font-medium text-red-800">Cons:</span>
                    <p class="text-red-700 mt-1">{{ review.cons }}</p>
                  </div>
                </div>
                <div class="mt-4 flex items-center text-sm text-gray-500" v-if="review.verified_purchase">
                  <svg class="h-4 w-4 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                  Verified Purchase
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found State -->
    <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
      <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
      </svg>
      <h2 class="mt-4 text-2xl font-bold text-gray-900">Book not found</h2>
      <p class="mt-2 text-gray-600">The book you're looking for doesn't exist or has been removed.</p>
      <div class="mt-6">
        <router-link to="/books" class="btn-primary">
          Browse Books
        </router-link>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AppLayout from '@/layouts/AppLayout.vue';
import { useBooksStore } from '@stores/books';
import { useAuthStore } from '@stores/auth';
import { useCartStore } from '@stores/cart';
import { useReviewsStore } from '@stores/reviews';

const route = useRoute();
const booksStore = useBooksStore();
const authStore = useAuthStore();
const cartStore = useCartStore();
const reviewsStore = useReviewsStore();

const book = computed(() => booksStore.currentBook);
const isLoading = computed(() => booksStore.isLoading || reviewsStore.isLoading);
const quantity = ref(1);
const currentImage = ref('');
const showReviewForm = ref(false);
const reviews = computed(() => reviewsStore.reviews);

const hasDiscount = computed(() => {
  return book.value?.original_price && book.value.original_price > book.value.price;
});

const discountPercentage = computed(() => {
  if (!hasDiscount.value) return 0;
  return Math.round((1 - book.value.price / book.value.original_price) * 100);
});

const incrementQuantity = () => {
  if (quantity.value < book.value.stock_quantity) {
    quantity.value++;
  }
};

const decrementQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--;
  }
};

const addToCart = () => {
  if (book.value.stock_quantity > 0) {
    cartStore.addToCart(book.value, quantity.value);
    quantity.value = 1;
    console.log('Added to cart:', book.value.title, 'Quantity:', quantity.value);
  }
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/400x600?text=No+Image';
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

onMounted(async () => {
  const bookId = route.params.id;
  if (bookId) {
    await Promise.all([
      booksStore.fetchBookById(bookId),
      reviewsStore.fetchBookReviews(bookId)
    ]);
    if (booksStore.currentBook) {
      currentImage.value = booksStore.currentBook.cover_image;
    }
  }
});
</script>