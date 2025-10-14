<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Book Catalog</h1>
      <p class="mt-2 text-lg text-gray-600">Discover your next favorite book from our collection</p>
    </div>

    <!-- Search and Filters -->
    <SearchFilters class="mb-8" />

    <!-- Results Header -->
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">
          {{ bookStore.pagination.totalCount }} books found
        </h2>
        <p v-if="bookStore.filters.search" class="text-sm text-gray-600">
          Search results for "{{ bookStore.filters.search }}"
        </p>
      </div>
      
      <!-- View Toggle -->
      <div class="flex items-center space-x-2">
        <button
          @click="isGridView = true"
          class="p-2 rounded-lg"
          :class="isGridView ? 'bg-primary-100 text-primary-700' : 'text-gray-400 hover:text-gray-600'"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
          </svg>
        </button>
        <button
          @click="isGridView = false"
          class="p-2 rounded-lg"
          :class="!isGridView ? 'bg-primary-100 text-primary-700' : 'text-gray-400 hover:text-gray-600'"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="space-y-4">
      <div v-for="n in 5" :key="n" class="card p-6 animate-pulse">
        <div class="flex space-x-4">
          <div class="w-24 h-32 bg-gray-200 rounded"></div>
          <div class="flex-1 space-y-3">
            <div class="h-4 bg-gray-200 rounded w-3/4"></div>
            <div class="h-3 bg-gray-200 rounded w-1/2"></div>
            <div class="h-4 bg-gray-200 rounded w-1/4"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="books.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No books found</h3>
      <p class="mt-1 text-sm text-gray-500">Try adjusting your search or filter criteria.</p>
      <div class="mt-6">
        <button @click="clearFilters" class="btn-primary">
          Clear Filters
        </button>
      </div>
    </div>

    <!-- Books Grid View -->
    <div v-else-if="isGridView">
      <BookGrid />
    </div>

    <!-- Books List View -->
    <div v-else class="space-y-4">
      <div
        v-for="book in books"
        :key="book.id"
        class="card p-6 hover:shadow-md transition-shadow duration-300"
      >
        <div class="flex space-x-6">
          <!-- Book Image -->
          <div class="w-24 h-32 flex-shrink-0">
            <div class="w-full h-full bg-gray-200 rounded-lg overflow-hidden">
              <img
                v-if="book.cover_image"
                :src="book.cover_image"
                :alt="book.title"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center bg-gray-100">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
              </div>
            </div>
          </div>

          <!-- Book Details -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between">
              <div class="flex-1 min-w-0">
                <h3 class="text-lg font-semibold text-gray-900 truncate">
                  {{ book.title }}
                </h3>
                <p class="text-sm text-gray-600 mt-1">by {{ book.author }}</p>
                
                <div class="mt-2 flex items-center space-x-4">
                  <div class="flex items-center">
                    <svg
                      v-for="star in 5"
                      :key="star"
                      class="w-4 h-4"
                      :class="star <= Math.floor(book.average_rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  </div>
                  <span class="text-sm text-gray-600">
                    {{ book.average_rating ? book.average_rating.toFixed(1) : 'No ratings' }}
                    ({{ book.review_count || 0 }})
                  </span>
                </div>

                <p class="mt-2 text-sm text-gray-600 line-clamp-2">
                  {{ book.description }}
                </p>
              </div>

              <div class="ml-4 flex-shrink-0 flex flex-col items-end space-y-2">
                <div class="text-right">
                  <span class="text-xl font-bold text-gray-900">${{ book.price.toFixed(2) }}</span>
                  <span v-if="book.original_price > book.price" class="ml-2 text-sm text-gray-500 line-through">
                    ${{ book.original_price.toFixed(2) }}
                  </span>
                </div>
                <span class="text-sm text-gray-500">{{ book.stock_quantity }} in stock</span>
                
                <div class="flex space-x-2">
                  <button
                    @click="viewDetails(book)"
                    class="btn-secondary text-sm py-1 px-3"
                  >
                    View
                  </button>
                  <button
                    @click="addToCart(book)"
                    :disabled="book.stock_quantity === 0"
                    class="btn-primary text-sm py-1 px-3 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>

            <div class="mt-3 flex flex-wrap gap-2">
              <span class="badge badge-primary">{{ book.category }}</span>
              <span
                v-for="genre in book.genres"
                :key="genre"
                class="badge badge-secondary"
              >
                {{ genre }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="!isLoading && books.length > 0" class="mt-8 flex items-center justify-between">
      <div class="text-sm text-gray-700">
        Showing <span class="font-medium">{{ (pagination.currentPage - 1) * pagination.pageSize + 1 }}</span> to
        <span class="font-medium">{{ Math.min(pagination.currentPage * pagination.pageSize, pagination.totalCount) }}</span> of
        <span class="font-medium">{{ pagination.totalCount }}</span> results
      </div>
      
      <div class="flex space-x-2">
        <button
          @click="previousPage"
          :disabled="pagination.currentPage === 1"
          class="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <button
          @click="nextPage"
          :disabled="pagination.currentPage === pagination.totalPages"
          class="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Featured Books Section -->
    <section v-if="!bookStore.filters.search && !bookStore.filters.category && !isLoading" class="mt-16">
      <div class="border-t border-gray-200 pt-12">
        <div class="text-center mb-8">
          <h2 class="text-2xl font-bold text-gray-900">Featured Books</h2>
          <p class="mt-2 text-gray-600">Handpicked selections from our collection</p>
        </div>
        <FeaturedBooks />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBookStore } from '@/stores/books'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notifications'
import SearchFilters from '@/components/books/SearchFilters.vue'
import BookGrid from '@/components/books/BookGrid.vue'
import FeaturedBooks from '@/components/books/FeaturedBooks.vue'

const router = useRouter()
const bookStore = useBookStore()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

const isGridView = ref(true)

const books = computed(() => bookStore.books)
const isLoading = computed(() => bookStore.isLoading)
const pagination = computed(() => bookStore.pagination)

const viewDetails = (book) => {
  router.push(`/books/${book.id}`)
}

const addToCart = async (book) => {
  const result = await cartStore.addToCart(book.id, 1)
  if (result.success) {
    notificationStore.success('Added to cart')
  }
}

const previousPage = () => {
  if (pagination.value.currentPage > 1) {
    bookStore.setPage(pagination.value.currentPage - 1)
    bookStore.fetchBooks()
  }
}

const nextPage = () => {
  if (pagination.value.currentPage < pagination.value.totalPages) {
    bookStore.setPage(pagination.value.currentPage + 1)
    bookStore.fetchBooks()
  }
}

const clearFilters = () => {
  bookStore.clearFilters()
  bookStore.fetchBooks()
}

onMounted(() => {
  bookStore.fetchBooks()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.badge {
  @apply px-2 py-1 text-xs font-medium rounded-full;
}

.badge-primary {
  @apply bg-primary-100 text-primary-800;
}

.badge-secondary {
  @apply bg-gray-100 text-gray-800;
}
</style>