<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ pageTitle }}
            </h1>
            <p class="mt-1 text-sm text-gray-600">
              {{ searchResultsText }}
            </p>
          </div>
          
          <div class="mt-4 sm:mt-0 flex items-center space-x-3">
            <!-- Search Toggle -->
            <button
              @click="showAdvancedSearch = true"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <AdjustmentsHorizontalIcon class="h-4 w-4 mr-2" />
              Filters
              <span v-if="activeFilterCount > 0" class="ml-2 bg-teal-100 text-teal-800 text-xs px-2 py-0.5 rounded-full">
                {{ activeFilterCount }}
              </span>
            </button>

            <!-- Sort Dropdown -->
            <div class="relative">
              <button
                @click="showSortOptions = !showSortOptions"
                class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
              >
                <BarsArrowUpIcon class="h-4 w-4 mr-2" />
                {{ currentSortLabel }}
                <ChevronDownIcon class="h-4 w-4 ml-2" />
              </button>

              <!-- Sort Dropdown Menu -->
              <div
                v-if="showSortOptions"
                class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10"
              >
                <button
                  v-for="option in sortOptions"
                  :key="option.value"
                  @click="changeSort(option.value, option.order)"
                  :class="[
                    'w-full text-left px-4 py-2 text-sm hover:bg-gray-50',
                    sortBy === option.value && sortOrder === option.order ? 'text-teal-600 bg-teal-50' : 'text-gray-700'
                  ]"
                >
                  {{ option.label }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Active Filters -->
        <div v-if="activeFilterCount > 0" class="mt-4 flex flex-wrap gap-2">
          <span
            v-for="(filter, key) in activeFilters"
            :key="key"
            class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-teal-100 text-teal-800"
          >
            {{ filter }}
            <button
              @click="removeFilter(key)"
              class="ml-1 hover:bg-teal-200 rounded-full p-0.5"
            >
              <XMarkIcon class="h-3 w-3" />
            </button>
          </span>
          <button
            @click="clearAllFilters"
            class="text-xs text-gray-600 hover:text-gray-800 underline"
          >
            Clear all
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Sidebar (Desktop) -->
        <div class="hidden lg:block lg:w-64 flex-shrink-0">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-8">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Filters</h3>
            
            <!-- Quick Categories -->
            <div class="mb-6">
              <h4 class="text-sm font-medium text-gray-700 mb-3">Categories</h4>
              <div class="space-y-2">
                <button
                  v-for="category in availableCategories"
                  :key="category"
                  @click="toggleCategory(category)"
                  :class="[
                    'w-full text-left px-3 py-2 text-sm rounded-lg transition-colors',
                    bookStore.filters.category === category
                      ? 'bg-teal-100 text-teal-800 border border-teal-200'
                      : 'text-gray-700 hover:bg-gray-50 border border-transparent'
                  ]"
                >
                  {{ category }}
                </button>
              </div>
            </div>

            <!-- Quick Genres -->
            <div class="mb-6">
              <h4 class="text-sm font-medium text-gray-700 mb-3">Genres</h4>
              <select
                v-model="bookStore.filters.genre"
                @change="applyFilters"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-sm"
              >
                <option value="">All Genres</option>
                <option v-for="genre in availableGenres" :key="genre" :value="genre">
                  {{ genre }}
                </option>
              </select>
            </div>

            <!-- Stock Filter -->
            <div class="mb-6">
              <label class="flex items-center space-x-2">
                <input
                  v-model="bookStore.filters.inStock"
                  @change="applyFilters"
                  type="checkbox"
                  class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
                >
                <span class="text-sm text-gray-700">In Stock Only</span>
              </label>
            </div>

            <!-- Featured Filter -->
            <div class="mb-6">
              <label class="flex items-center space-x-2">
                <input
                  v-model="bookStore.filters.featured"
                  @change="applyFilters"
                  type="checkbox"
                  class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
                >
                <span class="text-sm text-gray-700">Featured Only</span>
              </label>
            </div>

            <!-- Clear Filters -->
            <button
              @click="clearAllFilters"
              class="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              Clear All Filters
            </button>
          </div>
        </div>

        <!-- Book Grid -->
        <div class="flex-1">
          <!-- Loading State -->
          <div v-if="bookStore.isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <BookCardSkeleton v-for="n in 8" :key="n" />
          </div>

          <!-- Books Grid -->
          <div v-else-if="filteredBooks.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <BookCard
              v-for="book in filteredBooks"
              :key="book.id"
              :book="book"
              @add-to-cart="addToCart"
              @add-to-wishlist="addToWishlist"
            />
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-12">
            <BookOpenIcon class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="mt-4 text-lg font-medium text-gray-900">No books found</h3>
            <p class="mt-2 text-sm text-gray-600">
              Try adjusting your search criteria or browse all books.
            </p>
            <button
              @click="clearAllFilters"
              class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              Browse All Books
            </button>
          </div>

          <!-- Pagination -->
          <div v-if="bookStore.pagination.totalPages > 1" class="mt-8 flex items-center justify-between">
            <div class="text-sm text-gray-700">
              Showing page {{ bookStore.pagination.currentPage }} of {{ bookStore.pagination.totalPages }}
            </div>
            <div class="flex space-x-2">
              <button
                @click="previousPage"
                :disabled="bookStore.pagination.currentPage === 1"
                class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                @click="nextPage"
                :disabled="bookStore.pagination.currentPage === bookStore.pagination.totalPages"
                class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Filter Overlay -->
    <div
      v-if="showAdvancedSearch"
      class="fixed inset-0 z-50 lg:hidden"
      @click="showAdvancedSearch = false"
    >
      <div class="absolute inset-0 bg-black bg-opacity-50"></div>
      <div class="absolute right-0 top-0 h-full w-80 bg-white overflow-y-auto">
        <AdvancedSearch
          @search="handleSearch"
          @close="showAdvancedSearch = false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookStore } from '@/stores/books'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useNotificationStore } from '@/stores/notifications'
import {
  AdjustmentsHorizontalIcon,
  BarsArrowUpIcon,
  ChevronDownIcon,
  XMarkIcon,
  BookOpenIcon
} from '@heroicons/vue/24/outline'

import BookCard from '@/components/books/BookCard.vue'
import BookCardSkeleton from '@/components/books/BookCardSkeleton.vue'
import AdvancedSearch from '@/components/search/AdvancedSearch.vue'

const route = useRoute()
const router = useRouter()
const bookStore = useBookStore()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const notificationStore = useNotificationStore()

// State
const showAdvancedSearch = ref(false)
const showSortOptions = ref(false)

// Sort options that match your store structure
const sortOptions = [
  { value: 'title', order: 'asc', label: 'Title: A to Z' },
  { value: 'title', order: 'desc', label: 'Title: Z to A' },
  { value: 'price', order: 'asc', label: 'Price: Low to High' },
  { value: 'price', order: 'desc', label: 'Price: High to Low' },
  { value: 'average_rating', order: 'desc', label: 'Highest Rated' },
  { value: 'created_at', order: 'desc', label: 'Newest First' },
  { value: 'sales_count', order: 'desc', label: 'Bestsellers' }
]

// Computed
const filteredBooks = computed(() => bookStore.filteredBooks)
const availableCategories = computed(() => bookStore.categories)
const availableGenres = computed(() => bookStore.genres)
const sortBy = computed(() => bookStore.sortBy)
const sortOrder = computed(() => bookStore.sortOrder)

const pageTitle = computed(() => {
  if (bookStore.filters.search) return `Search: "${bookStore.filters.search}"`
  if (bookStore.filters.category) return bookStore.filters.category
  if (bookStore.filters.genre) return bookStore.filters.genre
  return 'All Books'
})

const searchResultsText = computed(() => {
  const count = filteredBooks.value.length
  if (count === 0) return 'No books found'
  return `${count} book${count !== 1 ? 's' : ''} found`
})

const currentSortLabel = computed(() => {
  const option = sortOptions.find(opt => 
    opt.value === sortBy.value && opt.order === sortOrder.value
  )
  return option ? option.label : 'Sort by'
})

const activeFilterCount = computed(() => {
  let count = 0
  if (bookStore.filters.search) count++
  if (bookStore.filters.category) count++
  if (bookStore.filters.genre) count++
  if (bookStore.filters.minPrice) count++
  if (bookStore.filters.maxPrice) count++
  if (bookStore.filters.rating) count++
  if (bookStore.filters.inStock) count++
  if (bookStore.filters.featured) count++
  return count
})

const activeFilters = computed(() => {
  const filters = {}
  if (bookStore.filters.search) {
    filters.search = `"${bookStore.filters.search}"`
  }
  if (bookStore.filters.category) {
    filters.category = bookStore.filters.category
  }
  if (bookStore.filters.genre) {
    filters.genre = bookStore.filters.genre
  }
  if (bookStore.filters.minPrice || bookStore.filters.maxPrice) {
    filters.price = `$${bookStore.filters.minPrice || 0} - $${bookStore.filters.maxPrice || 200}`
  }
  if (bookStore.filters.rating) {
    filters.rating = `${bookStore.filters.rating}+ stars`
  }
  if (bookStore.filters.inStock) {
    filters.inStock = 'In Stock'
  }
  if (bookStore.filters.featured) {
    filters.featured = 'Featured'
  }
  return filters
})

// Methods
const loadBooks = async () => {
  try {
    await bookStore.fetchBooks()
  } catch (error) {
    console.error('Failed to load books:', error)
    notificationStore.showNotification({
      type: 'error',
      title: 'Error',
      message: 'Failed to load books. Please try again.'
    })
  }
}

const handleSearch = () => {
  showAdvancedSearch.value = false
  loadBooks()
}

const changeSort = (field, order) => {
  bookStore.setSorting(field, order)
  showSortOptions.value = false
  loadBooks()
}

const toggleCategory = (category) => {
  bookStore.filters.category = bookStore.filters.category === category ? '' : category
  applyFilters()
}

const applyFilters = () => {
  bookStore.setPage(1)
  loadBooks()
}

const removeFilter = (filterKey) => {
  const updates = {}
  switch (filterKey) {
    case 'search':
      updates.search = ''
      break
    case 'category':
      updates.category = ''
      break
    case 'genre':
      updates.genre = ''
      break
    case 'price':
      updates.minPrice = ''
      updates.maxPrice = ''
      break
    case 'rating':
      updates.rating = ''
      break
    case 'inStock':
      updates.inStock = false
      break
    case 'featured':
      updates.featured = false
      break
  }
  
  bookStore.updateFilters(updates)
  loadBooks()
}

const clearAllFilters = () => {
  bookStore.clearFilters()
  loadBooks()
}

const previousPage = () => {
  if (bookStore.pagination.currentPage > 1) {
    bookStore.setPage(bookStore.pagination.currentPage - 1)
    loadBooks()
  }
}

const nextPage = () => {
  if (bookStore.pagination.currentPage < bookStore.pagination.totalPages) {
    bookStore.setPage(bookStore.pagination.currentPage + 1)
    loadBooks()
  }
}

const addToCart = async (book) => {
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
      message: 'Failed to add item to cart. Please try again.'
    })
  }
}

const addToWishlist = async (book) => {
  try {
    await wishlistStore.addToWishlist(book.id)
    notificationStore.showNotification({
      type: 'success',
      title: 'Added to wishlist',
      message: `${book.title} has been added to your wishlist`
    })
  } catch (error) {
    console.error('Failed to add to wishlist:', error)
    notificationStore.showNotification({
      type: 'error',
      title: 'Error',
      message: 'Failed to add item to wishlist. Please try again.'
    })
  }
}

// Initialize data
onMounted(async () => {
  // Load books if not already loaded
  if (bookStore.books.length === 0) {
    await loadBooks()
  }
})

// Watch for route changes (if using URL parameters)
watch(() => route.query, (query) => {
  if (query.search) {
    bookStore.updateFilters({ search: query.search })
    loadBooks()
  }
})
</script>