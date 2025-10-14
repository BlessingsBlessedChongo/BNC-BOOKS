<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <!-- Search Bar -->
    <div class="mb-6">
      <label for="search" class="block text-sm font-medium text-gray-700 mb-2">Search Books</label>
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
        <input
          id="search"
          v-model="localFilters.search"
          type="text"
          placeholder="Search by title, author, or ISBN..."
          class="input-field pl-10"
          @input="debouncedSearch"
        />
      </div>
    </div>

    <!-- Filters Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <!-- Category Filter -->
      <div>
        <label for="category" class="block text-sm font-medium text-gray-700 mb-2">Category</label>
        <select
          id="category"
          v-model="localFilters.category"
          class="input-field"
          @change="applyFilters"
        >
          <option value="">All Categories</option>
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>

      <!-- Genre Filter -->
      <div>
        <label for="genre" class="block text-sm font-medium text-gray-700 mb-2">Genre</label>
        <select
          id="genre"
          v-model="localFilters.genre"
          class="input-field"
          @change="applyFilters"
        >
          <option value="">All Genres</option>
          <option v-for="genre in genres" :key="genre" :value="genre">
            {{ genre }}
          </option>
        </select>
      </div>

      <!-- Price Range -->
      <div>
        <label for="minPrice" class="block text-sm font-medium text-gray-700 mb-2">Min Price</label>
        <input
          id="minPrice"
          v-model="localFilters.minPrice"
          type="number"
          min="0"
          step="0.01"
          placeholder="0.00"
          class="input-field"
          @input="applyFilters"
        />
      </div>

      <div>
        <label for="maxPrice" class="block text-sm font-medium text-gray-700 mb-2">Max Price</label>
        <input
          id="maxPrice"
          v-model="localFilters.maxPrice"
          type="number"
          min="0"
          step="0.01"
          placeholder="100.00"
          class="input-field"
          @input="applyFilters"
        />
      </div>
    </div>

    <!-- Additional Filters -->
    <div class="flex flex-wrap items-center gap-4 mb-6">
      <!-- Rating Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Minimum Rating</label>
        <div class="flex space-x-1">
          <button
            v-for="rating in [4, 3, 2, 1]"
            :key="rating"
            @click="setRatingFilter(rating)"
            class="p-2 rounded-lg border text-sm"
            :class="localFilters.rating === rating.toString() ? 'bg-primary-50 border-primary-300 text-primary-700' : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
          >
            {{ rating }}+ ⭐
          </button>
          <button
            @click="setRatingFilter('')"
            class="p-2 rounded-lg border border-gray-300 text-sm text-gray-700 hover:bg-gray-50"
          >
            Clear
          </button>
        </div>
      </div>

      <!-- Checkbox Filters -->
      <div class="flex items-center space-x-4">
        <label class="flex items-center">
          <input
            v-model="localFilters.inStock"
            type="checkbox"
            class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            @change="applyFilters"
          />
          <span class="ml-2 text-sm text-gray-700">In Stock Only</span>
        </label>
        
        <label class="flex items-center">
          <input
            v-model="localFilters.featured"
            type="checkbox"
            class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            @change="applyFilters"
          />
          <span class="ml-2 text-sm text-gray-700">Featured Only</span>
        </label>
      </div>
    </div>

    <!-- Sort and Actions -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <!-- Sort Options -->
      <div class="flex items-center space-x-4">
        <label class="text-sm font-medium text-gray-700">Sort by:</label>
        <select
          v-model="sortBy"
          class="input-field text-sm"
          @change="applySorting"
        >
          <option value="title">Title</option>
          <option value="author">Author</option>
          <option value="price">Price</option>
          <option value="average_rating">Rating</option>
          <option value="created_at">Date Added</option>
        </select>
        
        <select
          v-model="sortOrder"
          class="input-field text-sm"
          @change="applySorting"
        >
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-2">
        <button
          @click="clearAllFilters"
          class="btn-secondary text-sm"
        >
          Clear All
        </button>
        <button
          @click="applyFilters"
          class="btn-primary text-sm"
        >
          Apply Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { useBookStore } from '@/stores/books'
import { useDebounceFn } from '@vueuse/core'

const bookStore = useBookStore()

const localFilters = reactive({
  search: '',
  category: '',
  genre: '',
  minPrice: '',
  maxPrice: '',
  rating: '',
  inStock: false,
  featured: false
})

const sortBy = ref('title')
const sortOrder = ref('asc')

const categories = computed(() => bookStore.categories)
const genres = computed(() => bookStore.genres)

// Initialize with current filters
onMounted(() => {
  Object.assign(localFilters, bookStore.filters)
  sortBy.value = bookStore.sortBy
  sortOrder.value = bookStore.sortOrder
})

// Debounced search
const debouncedSearch = useDebounceFn(() => {
  applyFilters()
}, 500)

const applyFilters = () => {
  bookStore.updateFilters(localFilters)
  bookStore.fetchBooks()
}

const applySorting = () => {
  bookStore.setSorting(sortBy.value, sortOrder.value)
  bookStore.fetchBooks()
}

const setRatingFilter = (rating) => {
  localFilters.rating = rating
  applyFilters()
}

const clearAllFilters = () => {
  bookStore.clearFilters()
  Object.assign(localFilters, bookStore.filters)
  bookStore.fetchBooks()
}
</script>