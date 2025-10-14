<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Manage Orders</h1>
        <p class="mt-2 text-lg text-gray-600">Process and fulfill customer orders</p>
      </div>

      <!-- Error Message -->
      <div v-if="sellerStore.error" class="mb-6 rounded-md bg-red-50 p-4">
        <div class="text-sm text-red-700">{{ sellerStore.error }}</div>
      </div>

      <!-- Filters -->
      <div class="card p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select
              v-model="statusFilter"
              class="input-field"
              @change="applyFilters"
            >
              <option value="">All Orders</option>
              <option value="pending">Pending</option>
              <option value="processing">Processing</option>
              <option value="shipped">Shipped</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
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

      <!-- Orders Table -->
      <div class="card overflow-hidden">
        <!-- Loading State -->
        <div v-if="sellerStore.isLoading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
          <p class="mt-2 text-sm text-gray-600">Loading orders...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="sellerStore.sellerOrders.length === 0" class="p-12 text-center">
          <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900">No orders found</h3>
          <p class="mt-2 text-sm text-gray-500">Orders from your books will appear here.</p>
        </div>

        <!-- Orders List -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Order
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Customer
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Items
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr 
                v-for="order in sellerStore.sellerOrders" 
                :key="order.id"
                class="hover:bg-gray-50 transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ order.order_number }}</div>
                  <div class="text-sm text-gray-500">{{ formatDate(order.created_at) }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">
                    {{ order.shipping_address.first_name }} {{ order.shipping_address.last_name }}
                  </div>
                  <div class="text-sm text-gray-500">{{ order.shipping_address.city }}, {{ order.shipping_address.state }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-sm text-gray-900">{{ getOrderItemsCount(order) }} items</div>
                  <div class="text-sm text-gray-500 truncate max-w-xs">
                    {{ getOrderItemsTitles(order) }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${{ order.total_amount }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusBadgeClass(order.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize">
                    {{ order.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex justify-end space-x-2">
                    <button
                      @click="openOrderDetails(order)"
                      class="text-primary-600 hover:text-primary-900"
                    >
                      View
                    </button>
                    <button
                      v-if="canUpdateOrder(order)"
                      @click="openStatusModal(order)"
                      class="text-blue-600 hover:text-blue-900"
                    >
                      Update
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Order Details Modal -->
    <OrderDetailsModal
      :isOpen="showOrderDetailsModal"
      :order="selectedOrder"
      @close="closeOrderDetailsModal"
    />

    <!-- Update Status Modal -->
    <OrderStatusModal
      :isOpen="showStatusModal"
      :order="selectedOrder"
      @close="closeStatusModal"
      @updated="handleOrderUpdated"
    />
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import AppLayout from '../../layouts/AppLayout.vue';
import OrderDetailsModal from '../../components/seller/OrderDetailsModal.vue';
import OrderStatusModal from '../../components/seller/OrderStatusModal.vue';
import { useSellerStore } from '../../stores/seller';

const sellerStore = useSellerStore();

const statusFilter = ref('');
const showOrderDetailsModal = ref(false);
const showStatusModal = ref(false);
const selectedOrder = ref(null);

const openOrderDetails = (order) => {
  selectedOrder.value = order;
  showOrderDetailsModal.value = true;
};

const closeOrderDetailsModal = () => {
  showOrderDetailsModal.value = false;
  selectedOrder.value = null;
};

const openStatusModal = (order) => {
  selectedOrder.value = order;
  showStatusModal.value = true;
};

const closeStatusModal = () => {
  showStatusModal.value = false;
  selectedOrder.value = null;
};

const handleOrderUpdated = () => {
  sellerStore.fetchSellerOrders();
};

const getOrderItemsCount = (order) => {
  return order.items.reduce((total, item) => total + item.quantity, 0);
};

const getOrderItemsTitles = (order) => {
  return order.items.map(item => item.book.title).join(', ');
};

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

const canUpdateOrder = (order) => {
  return ['pending', 'processing'].includes(order.status);
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

const applyFilters = () => {
  sellerStore.updateOrderFilters({ 
    status: statusFilter.value
  });
  sellerStore.fetchSellerOrders();
};

const clearFilters = () => {
  statusFilter.value = '';
  sellerStore.updateOrderFilters({ 
    status: ''
  });
  sellerStore.fetchSellerOrders();
};

onMounted(async () => {
  await sellerStore.fetchSellerOrders();
});
</script>