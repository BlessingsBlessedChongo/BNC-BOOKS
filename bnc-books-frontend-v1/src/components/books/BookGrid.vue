<template>
  <div>
    <!-- Loading State -->
    <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div v-for="n in 8" :key="n" class="card animate-pulse">
        <div class="aspect-[3/4] bg-gray-200 rounded-t-lg"></div>
        <div class="p-4 space-y-3">
          <div class="h-4 bg-gray-200 rounded w-3/4"></div>
          <div class="h-3 bg-gray-200 rounded w-1/2"></div>
          <div class="h-4 bg-gray-200 rounded w-1/4"></div>
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

    <!-- Books Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <BookCard
        v-for="book in books"
        :key="book.id"
        :book="book"
      />
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
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useBookStore } from '@/stores/books'
import BookCard from './BookCard.vue'

const bookStore = useBookStore()

const books = computed(() => bookStore.books)
const isLoading = computed(() => bookStore.isLoading)
const pagination = computed(() => bookStore.pagination)

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
</script>