<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-900">Your Orders</h1>
        <p class="mt-1 text-sm text-gray-600">View and manage your book orders</p>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="rounded-md bg-red-50 p-4 mb-6">
        <div class="text-sm text-red-700">
          {{ error }}
        </div>
      </div>

      <!-- Orders List -->
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <h2 class="text-lg font-semibold text-gray-900">Order History</h2>
            <div class="mt-2 sm:mt-0">
              <select 
                v-model="statusFilter"
                class="input-field text-sm"
              >
                <option value="">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="processing">Processing</option>
                <option value="shipped">Shipped</option>
                <option value="delivered">Delivered</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
          <p class="mt-2 text-sm text-gray-600">Loading orders...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="orders.length === 0" class="p-8 text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No orders</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by placing your first order.</p>
          <div class="mt-6">
            <router-link to="/books" class="btn-primary">
              Browse Books
            </router-link>
          </div>
        </div>

        <!-- Orders List -->
        <div v-else class="divide-y divide-gray-200">
          <div 
            v-for="order in filteredOrders" 
            :key="order.id"
            class="p-6 hover:bg-gray-50 transition-colors"
          >
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-medium text-primary-600">
                    {{ order.order_number }}
                  </h3>
                  <span :class="getStatusBadgeClass(order.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize">
                    {{ order.status }}
                  </span>
                </div>
                <p class="mt-1 text-sm text-gray-600">
                  Placed on {{ formatDate(order.created_at) }}
                </p>
                <div class="mt-2 flex items-center text-sm text-gray-500">
                  <span class="mr-4">{{ order.items.length }} item(s)</span>
                  <span class="font-semibold text-gray-900">${{ order.total_amount }}</span>
                </div>
              </div>
              <div class="mt-4 sm:mt-0 sm:ml-6">
                <router-link 
                  :to="`/orders/${order.id}`"
                  class="btn-secondary text-sm"
                >
                  View Details
                </router-link>
              </div>
            </div>

            <!-- Order Items Preview -->
            <div class="mt-4 border-t border-gray-200 pt-4">
              <div class="flex space-x-4 overflow-x-auto">
                <div 
                  v-for="item in order.items.slice(0, 3)" 
                  :key="item.id"
                  class="flex-shrink-0"
                >
                  <div class="flex items-center space-x-3">
                    <img 
                      :src="item.book.cover_image" 
                      :alt="item.book.title"
                      class="h-16 w-12 object-cover rounded"
                    />
                    <div class="min-w-0 flex-1">
                      <p class="text-sm font-medium text-gray-900 truncate">
                        {{ item.book.title }}
                      </p>
                      <p class="text-sm text-gray-500">Qty: {{ item.quantity }}</p>
                    </div>
                  </div>
                </div>
                <div v-if="order.items.length > 3" class="flex-shrink-0 flex items-center">
                  <span class="text-sm text-gray-500">
                    +{{ order.items.length - 3 }} more
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="orders.length > 0" class="px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <p class="text-sm text-gray-700">
              Showing <span class="font-medium">{{ filteredOrders.length }}</span> of <span class="font-medium">{{ orders.length }}</span> orders
            </p>
            <div class="flex space-x-2">
              <button 
                :disabled="currentPage === 1"
                @click="currentPage--"
                class="btn-secondary text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button 
                :disabled="currentPage * pageSize >= orders.length"
                @click="currentPage++"
                class="btn-secondary text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import AppLayout from '@/layouts/AppLayout.vue';
import api from '@/utils/api';

const isLoading = ref(false);
const error = ref(''); // Added for error display
const statusFilter = ref('');
const currentPage = ref(1);
const pageSize = ref(10);

// Mock data - to be replaced with API calls
const orders = ref([
  {
    id: 1001,
    order_number: 'BNC-2024-1001',
    status: 'pending',
    total_amount: 33.57,
    created_at: '2024-01-15T10:30:00Z',
    items: [
      {
        id: 1,
        book: {
          id: 1,
          title: 'Harry Potter and the Philosopher\'s Stone',
          cover_image: 'http://localhost:8000/media/book_covers/harry_potter.jpg'
        },
        quantity: 2
      }
    ]
  }
]);

const filteredOrders = computed(() => {
  let filtered = orders.value;
  
  if (statusFilter.value) {
    filtered = filtered.filter(order => order.status === statusFilter.value);
  }
  
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  
  return filtered.slice(start, end);
});

const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    processing: 'bg-blue-100 text-blue-800',
    shipped: 'bg-purple-100 text-purple-800',
    delivered: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800'
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const loadOrders = async () => {
  isLoading.value = true;
  error.value = ''; // Clear previous errors
  try {
    // TODO: Replace with actual API call
    // const response = await api.get('/orders/');
    // orders.value = response.data.results;
    await new Promise(resolve => setTimeout(resolve, 1000)); // Mock delay
  } catch (err) {
    console.error('Failed to load orders:', err);
    error.value = err.response?.data?.error || 'Failed to load orders. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadOrders();
});
</script>