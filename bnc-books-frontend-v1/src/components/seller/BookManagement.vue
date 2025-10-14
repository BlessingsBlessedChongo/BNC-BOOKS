<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Book Management</h1>
          <p class="mt-2 text-lg text-gray-600">Manage your book listings and inventory</p>
        </div>
        <router-link to="/seller/books/new" class="btn-primary">
          Add New Book
        </router-link>
      </div>

      <!-- Quick Stats -->
      <div class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="card p-4 text-center">
          <div class="text-2xl font-bold text-gray-900">{{ sellerStore.bookStats.total }}</div>
          <div class="text-sm text-gray-600">Total Books</div>
        </div>
        <div class="card p-4 text-center">
          <div class="text-2xl font-bold text-green-600">{{ sellerStore.bookStats.published }}</div>
          <div class="text-sm text-gray-600">Published</div>
        </div>
        <div class="card p-4 text-center">
          <div class="text-2xl font-bold text-yellow-600">{{ sellerStore.bookStats.low_stock }}</div>
          <div class="text-sm text-gray-600">Low Stock</div>
        </div>
        <div class="card p-4 text-center">
          <div class="text-2xl font-bold text-red-600">{{ sellerStore.bookStats.out_of_stock }}</div>
          <div class="text-sm text-gray-600">Out of Stock</div>
        </div>
      </div>
    </div>

    <!-- Books Table -->
    <BookTable />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useSellerStore } from '@/stores/seller'
import BookTable from '@/components/seller/BookTable.vue'

const sellerStore = useSellerStore()

onMounted(async () => {
  await sellerStore.fetchBooks()
})
</script>