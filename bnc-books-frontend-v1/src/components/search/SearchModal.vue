<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-start justify-center min-h-screen pt-16 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        @click="$emit('close')"
      ></div>

      <!-- Search panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <!-- Search input -->
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
          </div>
          <input
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            placeholder="Search books, authors, ISBN..."
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-teal-500 focus:border-teal-500 sm:text-sm"
            @keyup.enter="performSearch"
            @input="handleInput"
          />
          <div class="absolute inset-y-0 right-0 flex items-center">
            <kbd class="inline-flex items-center border border-gray-200 rounded px-2 text-sm font-sans font-medium text-gray-400 mr-2">
              Esc
            </kbd>
          </div>
        </div>

        <!-- Recent searches -->
        <div v-if="recentSearches.length > 0 && !searchQuery" class="mt-4">
          <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Recent Searches
          </h3>
          <div class="space-y-1">
            <button
              v-for="search in recentSearches"
              :key="search.id"
              @click="loadRecentSearch(search)"
              class="w-full text-left px-2 py-1 text-sm text-gray-700 rounded hover:bg-gray-100 flex items-center justify-between"
            >
              <span>{{ search.query }}</span>
              <button
                @click.stop="removeRecentSearch(search.id)"
                class="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon class="h-4 w-4" />
              </button>
            </button>
          </div>
        </div>

        <!-- Search suggestions -->
        <div v-if="searchSuggestions.length > 0 && searchQuery" class="mt-4">
          <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Suggestions
          </h3>
          <div class="space-y-1">
            <button
              v-for="suggestion in searchSuggestions"
              :key="suggestion"
              @click="selectSuggestion(suggestion)"
              class="w-full text-left px-2 py-1 text-sm text-gray-700 rounded hover:bg-gray-100"
            >
              {{ suggestion }}
            </button>
          </div>
        </div>

        <!-- Quick filters -->
        <div class="mt-4 border-t border-gray-200 pt-4">
          <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Quick Filters
          </h3>
          <div class="grid grid-cols-2 gap-2">
            <button
              v-for="filter in quickFilters"
              :key="filter.label"
              @click="applyQuickFilter(filter)"
              class="flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <component :is="filter.icon" class="h-4 w-4 mr-2" />
              {{ filter.label }}
            </button>
          </div>
        </div>

        <!-- Action buttons -->
        <div class="mt-6 flex justify-end space-x-3">
          <button
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            Cancel
          </button>
          <button
            @click="performSearch"
            :disabled="!searchQuery"
            class="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Search
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  MagnifyingGlassIcon,
  XMarkIcon,
  StarIcon,
  FireIcon,
  BookOpenIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const emit = defineEmits(['close'])

// State
const searchQuery = ref('')
const searchInput = ref(null)
const recentSearches = ref([])

// Quick filters
const quickFilters = [
  { label: 'Featured', icon: StarIcon, filter: { featured: true } },
  { label: 'Bestsellers', icon: FireIcon, filter: { sort: 'bestsellers' } },
  { label: 'New Releases', icon: ClockIcon, filter: { sort: 'newest' } },
  { label: 'All Books', icon: BookOpenIcon, filter: {} }
]

// Search suggestions (in a real app, these would come from an API)
const searchSuggestions = ref([
  'Harry Potter',
  'Stephen King',
  'Science Fiction',
  'Self Help Books',
  'Business Strategy'
])

// Methods
const performSearch = () => {
  if (searchQuery.value.trim()) {
    // Save to recent searches
    saveToRecentSearches(searchQuery.value.trim())
    
    // Navigate to search results
    router.push({
      path: '/books',
      query: { search: searchQuery.value.trim() }
    })
    
    emit('close')
  }
}

const handleInput = () => {
  // Debounced search suggestions would go here
  // In a real app, you'd make an API call for suggestions
}

const selectSuggestion = (suggestion) => {
  searchQuery.value = suggestion
  performSearch()
}

const applyQuickFilter = (filter) => {
  router.push({
    path: '/books',
    query: filter.filter
  })
  emit('close')
}

const loadRecentSearches = () => {
  const saved = localStorage.getItem('bnc_recent_searches')
  if (saved) {
    recentSearches.value = JSON.parse(saved)
  }
}

const saveToRecentSearches = (query) => {
  const search = {
    id: Date.now(),
    query,
    timestamp: new Date().toISOString()
  }
  
  // Remove duplicates and limit to 5
  const existing = recentSearches.value.filter(s => s.query !== query)
  existing.unshift(search)
  recentSearches.value = existing.slice(0, 5)
  
  localStorage.setItem('bnc_recent_searches', JSON.stringify(recentSearches.value))
}

const removeRecentSearch = (id) => {
  recentSearches.value = recentSearches.value.filter(s => s.id !== id)
  localStorage.setItem('bnc_recent_searches', JSON.stringify(recentSearches.value))
}

const loadRecentSearch = (search) => {
  searchQuery.value = search.query
  performSearch()
}

const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    emit('close')
  }
}

// Lifecycle
onMounted(() => {
  searchInput.value.focus()
  loadRecentSearches()
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>