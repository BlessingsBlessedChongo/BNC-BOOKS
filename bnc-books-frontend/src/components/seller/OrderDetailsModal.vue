<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Order Details - {{ order?.order_number }}</h3>
          <button @click="close" class="text-gray-400 hover:text-gray-500">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div v-if="order" class="space-y-6 max-h-96 overflow-y-auto pr-2">
          <!-- Order Items -->
          <div>
            <h4 class="text-md font-medium text-gray-900 mb-3">Items</h4>
            <div class="space-y-3">
              <div 
                v-for="item in order.items" 
                :key="item.id"
                class="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <img
                    :src="item.book.cover_image"
                    :alt="item.book.title"
                    class="w-12 h-16 object-cover rounded"
                    @error="handleImageError"
                  />
                  <div>
                    <p class="font-medium text-gray-900">{{ item.book.title }}</p>
                    <p class="text-sm text-gray-600">by {{ item.book.author }}</p>
                    <p class="text-sm text-gray-600">Qty: {{ item.quantity }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="font-medium text-gray-900">${{ item.total_price }}</p>
                  <p class="text-sm text-gray-600">${{ item.unit_price }} each</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Shipping Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 class="text-md font-medium text-gray-900 mb-3">Shipping Address</h4>
              <div class="p-3 border border-gray-200 rounded-lg">
                <p class="font-medium">{{ order.shipping_address.first_name }} {{ order.shipping_address.last_name }}</p>
                <p class="text-sm text-gray-600">{{ order.shipping_address.street_address }}</p>
                <p v-if="order.shipping_address.apartment" class="text-sm text-gray-600">{{ order.shipping_address.apartment }}</p>
                <p class="text-sm text-gray-600">{{ order.shipping_address.city }}, {{ order.shipping_address.state }} {{ order.shipping_address.zip_code }}</p>
                <p class="text-sm text-gray-600">{{ order.shipping_address.country }}</p>
                <p class="text-sm text-gray-600">{{ order.shipping_address.phone }}</p>
              </div>
            </div>

            <div>
              <h4 class="text-md font-medium text-gray-900 mb-3">Shipping Method</h4>
              <div class="p-3 border border-gray-200 rounded-lg">
                <p class="font-medium">{{ order.shipping_method.name }}</p>
                <p class="text-sm text-gray-600">{{ order.shipping_method.delivery_days }}</p>
                <p class="text-sm text-gray-600">${{ order.shipping_method.price }}</p>
                <p v-if="order.tracking_number" class="text-sm text-blue-600 font-medium">
                  Tracking: {{ order.tracking_number }}
                </p>
              </div>
            </div>
          </div>

          <!-- Order Timeline -->
          <div>
            <h4 class="text-md font-medium text-gray-900 mb-3">Order Timeline</h4>
            <div class="space-y-2">
              <div class="flex items-center space-x-3 text-sm">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <span class="text-gray-600">Order placed</span>
                <span class="text-gray-400">{{ formatDate(order.created_at) }}</span>
              </div>
              <div v-if="order.processing_at" class="flex items-center space-x-3 text-sm">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <span class="text-gray-600">Processing started</span>
                <span class="text-gray-400">{{ formatDate(order.processing_at) }}</span>
              </div>
              <div v-if="order.shipped_at" class="flex items-center space-x-3 text-sm">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <span class="text-gray-600">Shipped</span>
                <span class="text-gray-400">{{ formatDate(order.shipped_at) }}</span>
              </div>
              <div v-if="order.delivered_at" class="flex items-center space-x-3 text-sm">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <span class="text-gray-600">Delivered</span>
                <span class="text-gray-400">{{ formatDate(order.delivered_at) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 mt-6">
          <button
            @click="close"
            class="btn-secondary"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  order: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};
</script>