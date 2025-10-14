<template>
  <div>
    <!-- Loading State -->
    <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div v-for="n in 8" :key="n" class="card animate-pulse">
        <div class="h-64 bg-gray-300 rounded-t-lg"></div>
        <div class="p-4 space-y-3">
          <div class="h-4 bg-gray-300 rounded w-3/4"></div>
          <div class="h-3 bg-gray-300 rounded w-1/2"></div>
          <div class="h-3 bg-gray-300 rounded w-1/4"></div>
          <div class="h-6 bg-gray-300 rounded w-1/3"></div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!hasBooks" class="text-center py-12">
      <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
      </svg>
      <h3 class="mt-4 text-lg font-medium text-gray-900">No books found</h3>
      <p class="mt-2 text-sm text-gray-500">
        {{ booksStore.hasFilters ? 'Try adjusting your filters or search terms.' : 'No books are available at the moment.' }}
      </p>
      <div class="mt-6" v-if="booksStore.hasFilters">
        <button 
          @click="booksStore.clearFilters()"
          class="btn-primary"
        >
          Clear Filters
        </button>
      </div>
    </div>

    <!-- Books Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <BookCard 
        v-for="book in books" 
        :key="book.id" 
        :book="book"
        class="h-full"
      />
    </div>

    <!-- Pagination -->
    <div v-if="hasBooks && pagination.total_pages > 1" class="mt-12 flex items-center justify-between">
      <div class="flex-1 flex justify-between items-center sm:hidden">
        <button
          @click="booksStore.loadPreviousPage()"
          :disabled="!pagination.previous"
          class="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <span class="text-sm text-gray-700">
          Page {{ pagination.current_page }} of {{ pagination.total_pages }}
        </span>
        <button
          @click="booksStore.loadNextPage()"
          :disabled="!pagination.next"
          class="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
      
      <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700">
            Showing <span class="font-medium">{{ (pagination.current_page - 1) * pagination.page_size + 1 }}</span> to 
            <span class="font-medium">{{ Math.min(pagination.current_page * pagination.page_size, pagination.count) }}</span> of 
            <span class="font-medium">{{ pagination.count }}</span> results
          </p>
        </div>
        <div>
          <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
            <button
              @click="booksStore.loadPreviousPage()"
              :disabled="!pagination.previous"
              class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span class="sr-only">Previous</span>
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            
            <!-- Page Numbers -->
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="booksStore.goToPage(page)"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                page === pagination.current_page
                  ? 'z-10 bg-primary-50 border-primary-500 text-primary-600'
                  : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
              ]"
            >
              {{ page }}
            </button>
            
            <button
              @click="booksStore.loadNextPage()"
              :disabled="!pagination.next"
              class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span class="sr-only">Next</span>
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useBooksStore } from '../../stores/books';
import BookCard from './BookCard.vue';

const booksStore = useBooksStore();

const books = computed(() => booksStore.books);
const isLoading = computed(() => booksStore.isLoading);
const hasBooks = computed(() => booksStore.hasBooks());
const pagination = computed(() => booksStore.pagination);

const visiblePages = computed(() => {
  const current = pagination.value.current_page;
  const total = pagination.value.total_pages;
  const delta = 2;
  const range = [];
  const rangeWithDots = [];

  for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
    range.push(i);
  }

  if (current - delta > 2) {
    rangeWithDots.push(1, '...');
  } else {
    rangeWithDots.push(1);
  }

  rangeWithDots.push(...range);

  if (current + delta < total - 1) {
    rangeWithDots.push('...', total);
  } else if (total > 1) {
    rangeWithDots.push(total);
  }

  return rangeWithDots;
});
</script>