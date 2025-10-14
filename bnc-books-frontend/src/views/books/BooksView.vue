<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Book Catalog</h1>
        <p class="mt-2 text-lg text-gray-600">Discover your next favorite book from our extensive collection</p>
      </div>

      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Sidebar Filters -->
        <div class="lg:w-64 flex-shrink-0">
          <div class="sticky top-8">
            <BookFilters />
            
            <!-- Mobile Filter Toggle -->
            <div class="lg:hidden mt-4">
              <button 
                @click="showMobileFilters = !showMobileFilters"
                class="w-full btn-secondary flex items-center justify-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.207A1 1 0 013 6.5V4z" />
                </svg>
                {{ showMobileFilters ? 'Hide Filters' : 'Show Filters' }}
              </button>
            </div>

            <!-- Mobile Filters Overlay -->
            <div 
              v-if="showMobileFilters" 
              class="lg:hidden fixed inset-0 z-50 bg-black bg-opacity-50"
              @click="showMobileFilters = false"
            >
              <div 
                class="absolute right-0 top-0 h-full w-80 bg-white overflow-y-auto"
                @click.stop
              >
                <div class="p-4">
                  <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold">Filters</h3>
                    <button 
                      @click="showMobileFilters = false"
                      class="text-gray-400 hover:text-gray-500"
                    >
                      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  <BookFilters />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content -->
        <div class="flex-1">
          <!-- Results Header -->
          <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700" v-if="!booksStore.isLoading">
                Showing {{ booksStore.pagination.count }} results
                <span v-if="booksStore.searchQuery" class="font-medium">for "{{ booksStore.searchQuery }}"</span>
              </p>
            </div>
            
            <div class="mt-2 sm:mt-0 flex items-center space-x-4">
              <!-- View Toggle -->
              <div class="flex items-center space-x-1 border border-gray-300 rounded-lg p-1">
                <button
                  @click="viewMode = 'grid'"
                  :class="[
                    'p-2 rounded-md transition-colors',
                    viewMode === 'grid' 
                      ? 'bg-primary-100 text-primary-600' 
                      : 'text-gray-500 hover:text-gray-700'
                  ]"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                  </svg>
                </button>
                <button
                  @click="viewMode = 'list'"
                  :class="[
                    'p-2 rounded-md transition-colors',
                    viewMode === 'list' 
                      ? 'bg-primary-100 text-primary-600' 
                      : 'text-gray-500 hover:text-gray-700'
                  ]"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Active Filters -->
          <div v-if="booksStore.hasFilters" class="mb-6 flex flex-wrap gap-2">
            <span 
              v-if="booksStore.searchQuery"
              class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
            >
              Search: "{{ booksStore.searchQuery }}"
              <button 
                @click="booksStore.searchBooks('')"
                class="ml-1 hover:text-primary-900"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </span>
            
            <span 
              v-for="(value, key) in activeFilterLabels"
              :key="key"
              class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
            >
              {{ value }}
              <button 
                @click="removeFilter(key)"
                class="ml-1 hover:text-gray-900"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </span>
          </div>

          <!-- Books Grid/List -->
          <BookGrid />
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import AppLayout from '../../layouts/AppLayout.vue';
import BookFilters from '../../components/books/BookFilters.vue';
import BookGrid from '../../components/books/BookGrid.vue';
import { useBooksStore } from '../../stores/books';

const booksStore = useBooksStore();
const showMobileFilters = ref(false);
const viewMode = ref('grid'); // 'grid' or 'list'

const activeFilterLabels = computed(() => {
  const labels = {};
  const filters = booksStore.filters;

  if (filters.category) {
    labels.category = `Category: ${filters.category}`;
  }
  if (filters.min_price) {
    labels.min_price = `Min: $${filters.min_price}`;
  }
  if (filters.max_price) {
    labels.max_price = `Max: $${filters.max_price}`;
  }
  if (filters.min_rating) {
    labels.min_rating = `${filters.min_rating}+ Stars`;
  }
  if (filters.in_stock) {
    labels.in_stock = 'In Stock';
  }
  if (filters.featured) {
    labels.featured = 'Featured';
  }

  return labels;
});

const removeFilter = (filterKey) => {
  if (filterKey === 'min_price' || filterKey === 'max_price') {
    booksStore.updateFilters({ [filterKey]: '' });
  } else if (filterKey === 'in_stock' || filterKey === 'featured') {
    booksStore.updateFilters({ [filterKey]: false });
  } else {
    booksStore.updateFilters({ [filterKey]: '' });
  }
};

onMounted(async () => {
  // Load initial books if not already loaded
  if (booksStore.books.length === 0) {
    await booksStore.fetchBooks();
  }
});
</script>