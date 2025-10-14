<template>
  <div class="card">
    <!-- Table Header -->
    <div class="px-6 py-4 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-medium text-gray-900">Your Books</h3>
        <div class="flex items-center space-x-4">
          <!-- Search -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <input
              v-model="localFilters.search"
              type="text"
              placeholder="Search books..."
              class="input-field pl-10 text-sm"
              @input="debouncedApplyFilters"
            />
          </div>

          <!-- Filters -->
          <select
            v-model="localFilters.status"
            class="input-field text-sm"
            @change="applyFilters"
          >
            <option value="">All Status</option>
            <option value="published">Published</option>
            <option value="draft">Draft</option>
          </select>

          <select
            v-model="localFilters.category"
            class="input-field text-sm"
            @change="applyFilters"
          >
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>

          <label class="flex items-center text-sm text-gray-700">
            <input
              v-model="localFilters.low_stock"
              type="checkbox"
              class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              @change="applyFilters"
            />
            <span class="ml-2">Low Stock</span>
          </label>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="sellerStore.isLoading" class="p-8 text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-2 text-sm text-gray-600">Loading books...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredBooks.length === 0" class="p-8 text-center">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No books found</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by creating your first book listing.</p>
      <div class="mt-6">
        <router-link to="/seller/books/new" class="btn-primary">
          Add New Book
        </router-link>
      </div>
    </div>

    <!-- Books Table -->
    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Book
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Price
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Stock
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Sales
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="book in filteredBooks"
            :key="book.id"
            class="hover:bg-gray-50 transition-colors duration-150"
          >
            <!-- Book Info -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10">
                  <img
                    :src="book.cover_image || '/placeholder-book.jpg'"
                    :alt="book.title"
                    class="h-10 w-10 object-cover rounded"
                  />
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900 line-clamp-1">
                    {{ book.title }}
                  </div>
                  <div class="text-sm text-gray-500">by {{ book.author }}</div>
                </div>
              </div>
            </td>

            <!-- Price -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              ${{ book.price.toFixed(2) }}
              <span
                v-if="book.original_price > book.price"
                class="text-xs text-gray-500 line-through ml-1"
              >
                ${{ book.original_price.toFixed(2) }}
              </span>
            </td>

            <!-- Stock -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ book.stock_quantity }}</div>
              <div
                v-if="book.stock_quantity === 0"
                class="text-xs text-red-600"
              >
                Out of Stock
              </div>
              <div
                v-else-if="book.stock_quantity < 10"
                class="text-xs text-yellow-600"
              >
                Low Stock
              </div>
            </td>

            <!-- Status -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                :class="book.is_published ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
              >
                {{ book.is_published ? 'Published' : 'Draft' }}
              </span>
              <span
                v-if="book.is_featured"
                class="ml-1 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-800"
              >
                Featured
              </span>
            </td>

            <!-- Sales -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              <div>{{ book.total_sales || 0 }} sold</div>
              <div class="text-xs text-gray-500">
                ${{ (book.total_revenue || 0).toFixed(2) }}
              </div>
            </td>

            <!-- Actions -->
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <div class="flex items-center space-x-2">
                <router-link
                  :to="`/seller/books/${book.id}/edit`"
                  class="text-primary-600 hover:text-primary-900"
                >
                  Edit
                </router-link>
                <button
                  @click="updateInventory(book)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  Stock
                </button>
                <button
                  @click="togglePublish(book)"
                  class="text-green-600 hover:text-green-900"
                >
                  {{ book.is_published ? 'Unpublish' : 'Publish' }}
                </button>
                <button
                  @click="deleteBook(book)"
                  class="text-red-600 hover:text-red-900"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Inventory Update Modal -->
    <InventoryModal
      :book="selectedBook"
      :is-open="showInventoryModal"
      @close="showInventoryModal = false"
      @update="handleInventoryUpdate"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { useSellerStore } from '@/stores/seller'
import { useNotificationStore } from '@/stores/notifications'
import InventoryModal from './InventoryModal.vue'

const sellerStore = useSellerStore()
const notificationStore = useNotificationStore()

const selectedBook = ref(null)
const showInventoryModal = ref(false)

const localFilters = reactive({
  search: '',
  status: '',
  category: '',
  low_stock: false
})

const filteredBooks = computed(() => sellerStore.filteredBooks)

const categories = computed(() => {
  const categories = new Set()
  sellerStore.books.forEach(book => {
    if (book.category) categories.add(book.category)
  })
  return Array.from(categories).sort()
})

// Initialize with current filters
onMounted(() => {
  Object.assign(localFilters, sellerStore.filters)
})

// Debounced search
const debouncedApplyFilters = useDebounceFn(() => {
  applyFilters()
}, 500)

const applyFilters = () => {
  sellerStore.updateFilters(localFilters)
}

const updateInventory = (book) => {
  selectedBook.value = book
  showInventoryModal.value = true
}

const togglePublish = async (book) => {
  const newStatus = !book.is_published
  const result = await sellerStore.updateBook(book.id, {
    is_published: newStatus
  })

  if (result.success) {
    notificationStore.success(
      `Book ${newStatus ? 'published' : 'unpublished'} successfully`
    )
  } else {
    notificationStore.error(result.error || 'Failed to update book status')
  }
}

const deleteBook = async (book) => {
  if (!confirm(`Are you sure you want to delete "${book.title}"?`)) return

  const result = await sellerStore.deleteBook(book.id)
  if (result.success) {
    notificationStore.success('Book deleted successfully')
  } else {
    notificationStore.error(result.error || 'Failed to delete book')
  }
}

const handleInventoryUpdate = async (stockData) => {
  const result = await sellerStore.updateInventory(selectedBook.value.id, stockData)
  if (result.success) {
    notificationStore.success('Inventory updated successfully')
    showInventoryModal.value = false
  } else {
    notificationStore.error(result.error || 'Failed to update inventory')
  }
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>