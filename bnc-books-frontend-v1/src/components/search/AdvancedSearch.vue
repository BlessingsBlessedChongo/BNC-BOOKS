<template>
  <div class="advanced-search bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <!-- Search Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold text-gray-900">Advanced Search</h2>
      <button 
        @click="$emit('close')"
        class="text-gray-400 hover:text-gray-600 transition-colors"
      >
        <XMarkIcon class="h-6 w-6" />
      </button>
    </div>

    <!-- Search Form -->
    <form @submit.prevent="performSearch" class="space-y-6">
      <!-- Keywords Search -->
      <div>
        <label for="keywords" class="block text-sm font-medium text-gray-700 mb-2">
          Keywords
        </label>
        <div class="relative">
          <input
            id="keywords"
            v-model="localFilters.search"
            type="text"
            placeholder="Search by title, author, or ISBN..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
          >
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
        </div>
      </div>

      <!-- Price Range -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Price Range
        </label>
        <div class="space-y-4">
          <div class="flex items-center justify-between text-sm text-gray-600">
            <span>${{ localFilters.minPrice || 0 }}</span>
            <span>${{ localFilters.maxPrice || 200 }}</span>
          </div>
          <div class="relative">
            <input
              v-model.number="localFilters.minPrice"
              type="range"
              min="0"
              max="200"
              step="5"
              class="absolute w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider-track"
            >
            <input
              v-model.number="localFilters.maxPrice"
              type="range"
              min="0"
              max="200"
              step="5"
              class="absolute w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider-track"
            >
          </div>
        </div>
      </div>

      <!-- Categories -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Categories
        </label>
        <div class="grid grid-cols-2 gap-2 max-h-32 overflow-y-auto">
          <label
            v-for="category in availableCategories"
            :key="category"
            class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:bg-gray-50 p-2 rounded"
          >
            <input
              v-model="localFilters.category"
              :value="category"
              type="radio"
              name="category"
              class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
            >
            <span>{{ category }}</span>
          </label>
        </div>
      </div>

      <!-- Genres -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Genres
        </label>
        <select
          v-model="localFilters.genre"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
        >
          <option value="">All Genres</option>
          <option v-for="genre in availableGenres" :key="genre" :value="genre">
            {{ genre }}
          </option>
        </select>
      </div>

      <!-- Stock & Featured -->
      <div class="grid grid-cols-2 gap-4">
        <label class="flex items-center space-x-2">
          <input
            v-model="localFilters.inStock"
            type="checkbox"
            class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
          >
          <span class="text-sm text-gray-700">In Stock Only</span>
        </label>
        <label class="flex items-center space-x-2">
          <input
            v-model="localFilters.featured"
            type="checkbox"
            class="rounded border-gray-300 text-teal-600 focus:ring-teal-500"
          >
          <span class="text-sm text-gray-700">Featured Only</span>
        </label>
      </div>

      <!-- Rating -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Minimum Rating
        </label>
        <div class="flex items-center space-x-2">
          <div class="flex">
            <button
              v-for="star in 5"
              :key="star"
              @click="localFilters.rating = star"
              class="p-1 focus:outline-none"
            >
              <StarIcon
                :class="[
                  'h-6 w-6',
                  star <= (localFilters.rating || 0) 
                    ? 'text-yellow-400 fill-current' 
                    : 'text-gray-300'
                ]"
              />
            </button>
          </div>
          <span class="text-sm text-gray-600 ml-2">
            {{ localFilters.rating || 0 }}+ stars
          </span>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-3 pt-4 border-t border-gray-200">
        <button
          type="button"
          @click="resetFilters"
          class="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
        >
          Reset
        </button>
        <button
          type="submit"
          class="flex-1 px-4 py-2 text-sm font-medium text-white bg-teal-600 border border-transparent rounded-lg hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
        >
          Apply Filters
        </button>
      </div>
    </form>

    <!-- Recent Searches -->
    <div v-if="recentSearches.length > 0" class="mt-6 pt-6 border-t border-gray-200">
      <h3 class="text-sm font-medium text-gray-700 mb-3">Recent Searches</h3>
      <div class="space-y-2">
        <button
          v-for="search in recentSearches"
          :key="search.id"
          @click="loadRecentSearch(search)"
          class="w-full text-left px-3 py-2 text-sm text-gray-600 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          {{ search.query }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useBookStore } from '@/stores/books'
import { MagnifyingGlassIcon, XMarkIcon, StarIcon } from '@heroicons/vue/24/outline'

const emit = defineEmits(['search', 'close'])
const bookStore = useBookStore()

// Local filters state that matches your store structure
const localFilters = ref({
  search: '',
  category: '',
  genre: '',
  minPrice: '',
  maxPrice: '',
  rating: '',
  inStock: false,
  featured: false
})

// Available options
const availableCategories = computed(() => bookStore.categories)
const availableGenres = computed(() => bookStore.genres)
const recentSearches = ref([])

// Load initial data and sync with store
onMounted(async () => {
  // Sync with current store filters
  localFilters.value = { ...bookStore.filters }
  loadRecentSearches()
})

// Watch for store filter changes
watch(() => bookStore.filters, (newFilters) => {
  localFilters.value = { ...newFilters }
}, { deep: true })

// Load recent searches from localStorage
const loadRecentSearches = () => {
  const saved = localStorage.getItem('bnc_recent_searches')
  if (saved) {
    recentSearches.value = JSON.parse(saved)
  }
}

// Save search to recent searches
const saveToRecentSearches = (searchParams) => {
  const search = {
    id: Date.now(),
    query: generateSearchQuery(searchParams),
    params: searchParams,
    timestamp: new Date().toISOString()
  }
  
  const existing = recentSearches.value.filter(s => s.query !== search.query)
  existing.unshift(search)
  recentSearches.value = existing.slice(0, 5)
  localStorage.setItem('bnc_recent_searches', JSON.stringify(recentSearches.value))
}

// Generate search query string
const generateSearchQuery = (params) => {
  const parts = []
  if (params.search) parts.push(params.search)
  if (params.minPrice || params.maxPrice) {
    parts.push(`$${params.minPrice || 0}-$${params.maxPrice || 200}`)
  }
  if (params.rating) parts.push(`${params.rating}+ stars`)
  if (params.category) parts.push(params.category)
  if (params.genre) parts.push(params.genre)
  if (params.inStock) parts.push('In Stock')
  if (params.featured) parts.push('Featured')
  return parts.join(' • ') || 'All books'
}

// Reset all filters
const resetFilters = () => {
  localFilters.value = {
    search: '',
    category: '',
    genre: '',
    minPrice: '',
    maxPrice: '',
    rating: '',
    inStock: false,
    featured: false
  }
}

// Load recent search
const loadRecentSearch = (search) => {
  localFilters.value = { ...search.params }
  performSearch()
}

// Perform search
const performSearch = async () => {
  try {
    // Save to recent searches
    saveToRecentSearches({ ...localFilters.value })
    
    // Update store filters and fetch books
    await bookStore.updateFilters({ ...localFilters.value })
    await bookStore.fetchBooks()
    
    // Emit search event
    emit('search', { ...localFilters.value })
    emit('close')
  } catch (error) {
    console.error('Search failed:', error)
  }
}
</script>

<style scoped>
.slider-track {
  background: linear-gradient(to right, #e5e7eb 0%, #e5e7eb 100%);
}

.slider-track::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #14b8a6;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.slider-track::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #14b8a6;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>