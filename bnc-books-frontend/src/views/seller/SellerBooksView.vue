<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Manage Books</h1>
          <p class="mt-2 text-lg text-gray-600">Add, edit, and manage your book listings</p>
        </div>
        <button
          @click="openCreateModal"
          class="mt-4 sm:mt-0 btn-primary"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add New Book
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="sellerStore.error" class="mb-6 rounded-md bg-red-50 p-4">
        <div class="text-sm text-red-700">{{ sellerStore.error }}</div>
      </div>

      <!-- Filters -->
      <div class="card p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Search</label>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search books..."
              class="input-field"
              @input="debouncedSearch"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select
              v-model="statusFilter"
              class="input-field"
              @change="applyFilters"
            >
              <option value="">All Books</option>
              <option value="true">Published</option>
              <option value="false">Unpublished</option>
            </select>
          </div>
          <div class="flex items-end">
            <button
              @click="clearFilters"
              class="btn-secondary w-full"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      <!-- Books Table -->
      <div class="card overflow-hidden">
        <!-- Loading State -->
        <div v-if="sellerStore.isLoading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
          <p class="mt-2 text-sm text-gray-600">Loading books...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="sellerStore.sellerBooks.length === 0" class="p-12 text-center">
          <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900">No books found</h3>
          <p class="mt-2 text-sm text-gray-500">Get started by adding your first book.</p>
          <div class="mt-6">
            <button
              @click="openCreateModal"
              class="btn-primary"
            >
              Add New Book
            </button>
          </div>
        </div>

        <!-- Books List -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Book
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Price & Stock
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Sales
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr 
                v-for="book in sellerStore.sellerBooks" 
                :key="book.id"
                class="hover:bg-gray-50 transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-16 w-12">
                      <img
                        :src="book.cover_image"
                        :alt="book.title"
                        class="h-16 w-12 object-cover rounded"
                        @error="handleImageError"
                      />
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ book.title }}</div>
                      <div class="text-sm text-gray-500">by {{ book.author }}</div>
                      <div class="text-sm text-gray-500">ISBN: {{ book.isbn }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">${{ book.price }}</div>
                  <div class="text-sm text-gray-500">
                    <span :class="book.stock_quantity > 0 ? 'text-green-600' : 'text-red-600'">
                      {{ book.stock_quantity }} in stock
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    :class="book.is_published ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  >
                    {{ book.is_published ? 'Published' : 'Unpublished' }}
                  </span>
                  <span 
                    v-if="book.is_featured"
                    class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
                  >
                    Featured
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div>{{ book.total_sales || 0 }} sold</div>
                  <div class="text-gray-500">${{ (book.total_revenue || 0).toFixed(2) }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex justify-end space-x-2">
                    <button
                      @click="openEditModal(book)"
                      class="text-primary-600 hover:text-primary-900"
                    >
                      Edit
                    </button>
                    <button
                      @click="openInventoryModal(book)"
                      class="text-blue-600 hover:text-blue-900"
                    >
                      Inventory
                    </button>
                    <button
                      @click="confirmDelete(book)"
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

        <!-- Pagination -->
        <div v-if="sellerStore.sellerBooks.length > 0" class="px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <p class="text-sm text-gray-700">
              Showing {{ (sellerStore.pagination.current_page - 1) * sellerStore.pagination.page_size + 1 }} to 
              {{ Math.min(sellerStore.pagination.current_page * sellerStore.pagination.page_size, sellerStore.pagination.count) }} of 
              {{ sellerStore.pagination.count }} results
            </p>
            <div class="flex space-x-2">
              <button
                @click="loadPreviousPage"
                :disabled="!sellerStore.pagination.previous"
                class="btn-secondary text-sm disabled:opacity-50"
              >
                Previous
              </button>
              <button
                @click="loadNextPage"
                :disabled="!sellerStore.pagination.next"
                class="btn-secondary text-sm disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Book Form Modal -->
    <BookFormModal
      :isOpen="showBookModal"
      :book="selectedBook"
      :mode="bookModalMode"
      @close="closeBookModal"
      @saved="handleBookSaved"
    />

    <!-- Inventory Modal -->
    <InventoryModal
      :isOpen="showInventoryModal"
      :book="selectedBook"
      @close="closeInventoryModal"
      @updated="handleInventoryUpdated"
    />
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useDebounceFn } from '@vueuse/core';
import AppLayout from '../../layouts/AppLayout.vue';
import BookFormModal from '../../components/seller/BookFormModal.vue';
import InventoryModal from '../../components/seller/InventoryModal.vue';
import { useSellerStore } from '../../stores/seller';

const sellerStore = useSellerStore();

const searchQuery = ref('');
const statusFilter = ref('');
const showBookModal = ref(false);
const showInventoryModal = ref(false);
const selectedBook = ref(null);
const bookModalMode = ref('create'); // 'create' or 'edit'

const openCreateModal = () => {
  selectedBook.value = null;
  bookModalMode.value = 'create';
  showBookModal.value = true;
};

const openEditModal = (book) => {
  selectedBook.value = { ...book };
  bookModalMode.value = 'edit';
  showBookModal.value = true;
};

const openInventoryModal = (book) => {
  selectedBook.value = { ...book };
  showInventoryModal.value = true;
};

const closeBookModal = () => {
  showBookModal.value = false;
  selectedBook.value = null;
};

const closeInventoryModal = () => {
  showInventoryModal.value = false;
  selectedBook.value = null;
};

const handleBookSaved = () => {
  sellerStore.fetchSellerBooks();
};

const handleInventoryUpdated = () => {
  sellerStore.fetchSellerBooks();
};

const confirmDelete = async (book) => {
  if (!confirm(`Are you sure you want to delete "${book.title}"? This action cannot be undone.`)) {
    return;
  }

  try {
    await sellerStore.deleteBook(book.id);
  } catch (error) {
    // Error is handled by the store
  }
};

const debouncedSearch = useDebounceFn(() => {
  sellerStore.updateBookFilters({ search: searchQuery.value, page: 1 });
  sellerStore.fetchSellerBooks();
}, 500);

const applyFilters = () => {
  sellerStore.updateBookFilters({ 
    is_published: statusFilter.value,
    page: 1 
  });
  sellerStore.fetchSellerBooks();
};

const clearFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  sellerStore.updateBookFilters({ 
    search: '',
    is_published: '',
    page: 1 
  });
  sellerStore.fetchSellerBooks();
};

const loadNextPage = () => {
  if (sellerStore.pagination.next) {
    sellerStore.updateBookFilters({ page: sellerStore.pagination.current_page + 1 });
    sellerStore.fetchSellerBooks();
  }
};

const loadPreviousPage = () => {
  if (sellerStore.pagination.previous) {
    sellerStore.updateBookFilters({ page: sellerStore.pagination.current_page - 1 });
    sellerStore.fetchSellerBooks();
  }
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};

onMounted(async () => {
  await sellerStore.fetchSellerBooks();
});
</script>