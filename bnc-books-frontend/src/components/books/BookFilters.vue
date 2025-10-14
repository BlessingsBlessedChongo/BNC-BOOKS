<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-gray-900">Filters</h3>
      <button 
        @click="clearAllFilters"
        class="text-sm text-primary-600 hover:text-primary-700 font-medium"
        :disabled="!hasActiveFilters"
      >
        Clear All
      </button>
    </div>

    <!-- Search -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Search</label>
      <div class="relative">
        <input
          v-model="localSearchQuery"
          type="text"
          placeholder="Search books, authors, ISBN..."
          class="input-field pl-10"
          @input="debouncedSearch"
        />
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Category Filter -->
    <div class="mb-6" v-if="categories.length > 0">
      <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
      <select 
        v-model="localFilters.category"
        class="input-field"
        @change="applyFilters"
      >
        <option value="">All Categories</option>
        <option 
          v-for="category in categories" 
          :key="category"
          :value="category"
        >
          {{ category }}
        </option>
      </select>
    </div>

    <!-- Price Range -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <input
            v-model="localFilters.min_price"
            type="number"
            placeholder="Min"
            min="0"
            step="0.01"
            class="input-field"
            @change="applyFilters"
          />
        </div>
        <div>
          <input
            v-model="localFilters.max_price"
            type="number"
            placeholder="Max"
            min="0"
            step="0.01"
            class="input-field"
            @change="applyFilters"
          />
        </div>
      </div>
    </div>

    <!-- Rating Filter -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">Minimum Rating</label>
      <select 
        v-model="localFilters.min_rating"
        class="input-field"
        @change="applyFilters"
      >
        <option value="">Any Rating</option>
        <option value="4">4 Stars & Up</option>
        <option value="3">3 Stars & Up</option>
        <option value="2">2 Stars & Up</option>
        <option value="1">1 Star & Up</option>
      </select>
    </div>

    <!-- Stock Filter -->
    <div class="mb-6">
      <label class="flex items-center">
        <input
          v-model="localFilters.in_stock"
          type="checkbox"
          class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          @change="applyFilters"
        />
        <span class="ml-2 text-sm text-gray-700">In Stock Only</span>
      </label>
    </div>

    <!-- Featured Filter -->
    <div class="mb-6">
      <label class="flex items-center">
        <input
          v-model="localFilters.featured"
          type="checkbox"
          class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          @change="applyFilters"
        />
        <span class="ml-2 text-sm text-gray-700">Featured Books Only</span>
      </label>
    </div>

    <!-- Sort Options -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
      <select 
        v-model="localFilters.ordering"
        class="input-field"
        @change="applyFilters"
      >
        <option value="title">Title A-Z</option>
        <option value="-title">Title Z-A</option>
        <option value="price">Price: Low to High</option>
        <option value="-price">Price: High to Low</option>
        <option value="-average_rating">Highest Rated</option>
        <option value="-created_at">Newest First</option>
        <option value="created_at">Oldest First</option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue';
import { useBooksStore } from '../../stores/books';
import { useDebounceFn } from '@vueuse/core';

const booksStore = useBooksStore();

const localSearchQuery = ref(booksStore.searchQuery);
const localFilters = reactive({ ...booksStore.filters });

const categories = computed(() => booksStore.categories);
const hasActiveFilters = computed(() => booksStore.hasFilters());

// Debounced search function
const debouncedSearch = useDebounceFn(() => {
  booksStore.searchBooks(localSearchQuery.value);
}, 500);

const applyFilters = () => {
  booksStore.updateFilters({ ...localFilters });
};

const clearAllFilters = () => {
  localSearchQuery.value = '';
  Object.keys(localFilters).forEach(key => {
    if (key !== 'page_size' && key !== 'ordering') {
      localFilters[key] = key === 'in_stock' || key === 'featured' ? false : '';
    }
  });
  booksStore.clearFilters();
};

// Sync local filters with store filters
watch(
  () => booksStore.filters,
  (newFilters) => {
    Object.keys(localFilters).forEach(key => {
      localFilters[key] = newFilters[key];
    });
  },
  { deep: true }
);

watch(
  () => booksStore.searchQuery,
  (newQuery) => {
    localSearchQuery.value = newQuery;
  }
);

onMounted(async () => {
  if (categories.value.length === 0) {
    await booksStore.fetchCategories();
  }
});
</script>