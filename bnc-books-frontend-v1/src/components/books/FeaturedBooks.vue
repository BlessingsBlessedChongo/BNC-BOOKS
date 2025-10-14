<template>
  <div class="relative">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <BookCard
        v-for="book in featuredBooks"
        :key="book.id"
        :book="book"
      />
    </div>
    
    <!-- Loading State -->
    <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="n in 4" :key="n" class="card animate-pulse">
        <div class="aspect-[3/4] bg-gray-200 rounded-t-lg"></div>
        <div class="p-4 space-y-3">
          <div class="h-4 bg-gray-200 rounded w-3/4"></div>
          <div class="h-3 bg-gray-200 rounded w-1/2"></div>
          <div class="h-4 bg-gray-200 rounded w-1/4"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from '@/stores/books'
import BookCard from './BookCard.vue'

const bookStore = useBookStore()
const featuredBooks = ref([])
const isLoading = ref(false)

onMounted(async () => {
  isLoading.value = true
  const result = await bookStore.fetchFeaturedBooks()
  if (result.success) {
    featuredBooks.value = result.data
  }
  isLoading.value = false
})
</script>