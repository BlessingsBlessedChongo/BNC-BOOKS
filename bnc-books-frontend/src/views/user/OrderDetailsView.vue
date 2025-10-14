<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="ordersStore.isLoading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading order details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="!order" class="text-center py-12">
        <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h2 class="mt-4 text-2xl font-bold text-gray-900">Order not found</h2>
        <p class="mt-2 text-gray-600">The order you're looking for doesn't exist or you don't have permission to view it.</p>
        <div class="mt-6">
          <router-link to="/orders" class="btn-primary">
            Back to Orders
          </router-link>
        </div>
      </div>

      <!-- Order Details -->
      <div v-else class="space-y-8">
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Order #{{ order.order_number }}</h1>
            <p class="mt-1 text-sm text-gray-600">Placed on {{ formatDate(order.created_at) }}</p>
          </div>
          <div class="mt-4 sm:mt-0 flex items-center space-x-4">
            <span :class="getStatusBadgeClass(order.status)" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium capitalize">
              {{ order.status }}
            </span>
            <button
              v-if="canCancelOrder"
              @click="cancelOrder"
              :disabled="ordersStore.isLoading"
              class="btn-secondary text-sm disabled:opacity-50"
            >
              Cancel Order
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="ordersStore.error" class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Error</h3>
              <div class="mt-1 text-sm text-red-700">
                <p>{{ ordersStore.error }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Items -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Items</h2>
          </div>
          <div class="p-6">
            <div class="space-y-6">
              <div 
                v-for="item in order.items" 
                :key="item.id"
                class="flex items-start space-x-4"
              >
                <img
                  :src="item.book.cover_image"
                  :alt="item.book.title"
                  class="w-20 h-28 object-cover rounded-lg"
                  @error="handleImageError"
                />
                <div class="flex-1 min-w-0">
                  <h3 class="text-lg font-medium text-gray-900">
                    {{ item.book.title }}
                  </h3>
                  <p class="text-sm text-gray-600">by {{ item.book.author }}</p>
                  <p class="text-sm text-gray-600">ISBN: {{ item.book.isbn }}</p>
                  <p class="text-sm text-gray-600">Condition: {{ item.book.condition }}</p>
                  
                  <!-- Review Button -->
                  <div class="mt-3">
                    <button
                      v-if="!item.has_reviewed && order.status === 'delivered'"
                      @click="openReviewModal(item)"
                      class="text-primary-600 hover:text-primary-700 text-sm font-medium"
                    >
                      Write a Review
                    </button>
                    <span v-else-if="item.has_reviewed" class="text-green-600 text-sm font-medium">
                      ✓ Reviewed
                    </span>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-lg font-semibold text-gray-900">${{ item.total_price }}</p>
                  <p class="text-sm text-gray-600">${{ item.unit_price }} × {{ item.quantity }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Shipping Address -->
          <div class="card">
            <div class="px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-medium text-gray-900">Shipping Address</h2>
            </div>
            <div class="p-6">
              <div class="space-y-2 text-sm">
                <p class="font-medium text-gray-900">{{ order.shipping_address.first_name }} {{ order.shipping_address.last_name }}</p>
                <p class="text-gray-600">{{ order.shipping_address.street_address }}</p>
                <p v-if="order.shipping_address.apartment" class="text-gray-600">{{ order.shipping_address.apartment }}</p>
                <p class="text-gray-600">{{ order.shipping_address.city }}, {{ order.shipping_address.state }} {{ order.shipping_address.zip_code }}</p>
                <p class="text-gray-600">{{ order.shipping_address.country }}</p>
                <p class="text-gray-600">{{ order.shipping_address.phone }}</p>
              </div>
            </div>
          </div>

          <!-- Billing Address -->
          <div class="card">
            <div class="px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-medium text-gray-900">Billing Address</h2>
            </div>
            <div class="p-6">
              <div class="space-y-2 text-sm">
                <p class="font-medium text-gray-900">{{ order.billing_address.first_name }} {{ order.billing_address.last_name }}</p>
                <p class="text-gray-600">{{ order.billing_address.street_address }}</p>
                <p class="text-gray-600">{{ order.billing_address.city }}, {{ order.billing_address.state }} {{ order.billing_address.zip_code }}</p>
                <p class="text-gray-600">{{ order.billing_address.country }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Totals -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Order Summary</h2>
          </div>
          <div class="p-6">
            <dl class="space-y-3">
              <div class="flex justify-between">
                <dt class="text-gray-600">Subtotal</dt>
                <dd class="font-medium text-gray-900">${{ order.subtotal }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">Shipping</dt>
                <dd class="font-medium text-gray-900">${{ order.shipping_cost }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">Tax</dt>
                <dd class="font-medium text-gray-900">${{ order.tax_amount }}</dd>
              </div>
              <div class="flex justify-between border-t border-gray-200 pt-3">
                <dt class="text-lg font-medium text-gray-900">Total</dt>
                <dd class="text-lg font-bold text-gray-900">${{ order.total_amount }}</dd>
              </div>
            </dl>
          </div>
        </div>

        <!-- Shipping Information -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Shipping Information</h2>
          </div>
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-900">{{ order.shipping_method.name }}</p>
                <p class="text-sm text-gray-600">{{ order.shipping_method.delivery_days }}</p>
                <p class="text-sm text-gray-600" v-if="order.tracking_number">
                  Tracking: {{ order.tracking_number }}
                </p>
              </div>
              <div class="text-right">
                <p class="font-medium text-gray-900">${{ order.shipping_method.price }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Timeline -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Order Timeline</h2>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-gray-900">Order Placed</p>
                  <p class="text-sm text-gray-600">{{ formatDate(order.created_at) }}</p>
                </div>
              </div>

              <div v-if="order.processing_at" class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-gray-900">Processing</p>
                  <p class="text-sm text-gray-600">{{ formatDate(order.processing_at) }}</p>
                </div>
              </div>

              <div v-if="order.shipped_at" class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-gray-900">Shipped</p>
                  <p class="text-sm text-gray-600">{{ formatDate(order.shipped_at) }}</p>
                </div>
              </div>

              <div v-if="order.delivered_at" class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-gray-900">Delivered</p>
                  <p class="text-sm text-gray-600">{{ formatDate(order.delivered_at) }}</p>
                </div>
              </div>

              <div v-if="order.cancelled_at" class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-gray-900">Cancelled</p>
                  <p class="text-sm text-gray-600">{{ formatDate(order.cancelled_at) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Return Request -->
        <div v-if="canRequestReturn" class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Return Request</h2>
          </div>
          <div class="p-6">
            <button
              @click="openReturnModal"
              class="btn-secondary"
            >
              Request Return
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Review Modal -->
    <ReviewModal 
      :isOpen="showReviewModal"
      :book="selectedBook"
      :orderItem="selectedOrderItem"
      @close="closeReviewModal"
      @submitted="handleReviewSubmitted"
    />

    <!-- Return Modal -->
    <ReturnModal 
      :isOpen="showReturnModal"
      :order="order"
      @close="closeReturnModal"
      @submitted="handleReturnSubmitted"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppLayout from '../../layouts/AppLayout.vue';
import ReviewModal from '../../components/reviews/ReviewModal.vue';
import ReturnModal from '../../components/orders/ReturnModal.vue';
import { useOrdersStore } from '../../stores/orders';

const route = useRoute();
const router = useRouter();
const ordersStore = useOrdersStore();

const order = computed(() => ordersStore.currentOrder);
const showReviewModal = ref(false);
const showReturnModal = ref(false);
const selectedBook = ref(null);
const selectedOrderItem = ref(null);

const canCancelOrder = computed(() => {
  return order.value && order.value.status === 'pending';
});

const canRequestReturn = computed(() => {
  return order.value && 
         order.value.status === 'delivered' && 
         !order.value.return_requested;
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
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};

const openReviewModal = (orderItem) => {
  selectedBook.value = orderItem.book;
  selectedOrderItem.value = orderItem;
  showReviewModal.value = true;
};

const closeReviewModal = () => {
  showReviewModal.value = false;
  selectedBook.value = null;
  selectedOrderItem.value = null;
};

const openReturnModal = () => {
  showReturnModal.value = true;
};

const closeReturnModal = () => {
  showReturnModal.value = false;
};

const handleReviewSubmitted = () => {
  // Refresh order data to update review status
  ordersStore.fetchOrderById(route.params.id);
};

const handleReturnSubmitted = () => {
  // Refresh order data to update return status
  ordersStore.fetchOrderById(route.params.id);
};

const cancelOrder = async () => {
  if (!confirm('Are you sure you want to cancel this order?')) return;
  
  try {
    await ordersStore.cancelOrder(order.value.id);
  } catch (error) {
    // Error is handled by the store
  }
};

onMounted(async () => {
  const orderId = route.params.id;
  if (orderId) {
    await ordersStore.fetchOrderById(orderId);
  }
});
</script>