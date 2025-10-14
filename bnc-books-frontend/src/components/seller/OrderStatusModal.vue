<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Update Order Status</h3>
          <button @click="close" class="text-gray-400 hover:text-gray-500">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Order Info -->
        <div v-if="order" class="mb-6 p-4 bg-gray-50 rounded-lg">
          <p class="font-medium text-gray-900">{{ order.order_number }}</p>
          <p class="text-sm text-gray-600">Current status: 
            <span :class="getStatusBadgeClass(order.status)" class="ml-1 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium capitalize">
              {{ order.status }}
            </span>
          </p>
        </div>

        <!-- Status Form -->
        <form @submit.prevent="updateStatus" class="space-y-6">
          <!-- New Status -->
          <div>
            <label for="status" class="block text-sm font-medium text-gray-700">New Status</label>
            <select
              id="status"
              v-model="form.status"
              required
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.status }"
            >
              <option value="">Select status</option>
              <option value="processing">Processing</option>
              <option value="shipped">Shipped</option>
            </select>
            <p v-if="errors.status" class="mt-1 text-sm text-red-600">{{ errors.status[0] }}</p>
          </div>

          <!-- Tracking Number (for shipped status) -->
          <div v-if="form.status === 'shipped'">
            <label for="tracking_number" class="block text-sm font-medium text-gray-700">Tracking Number</label>
            <input
              id="tracking_number"
              v-model="form.tracking_number"
              type="text"
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.tracking_number }"
              placeholder="Enter tracking number"
            />
            <p v-if="errors.tracking_number" class="mt-1 text-sm text-red-600">{{ errors.tracking_number[0] }}</p>
          </div>

          <!-- Error Message -->
          <div v-if="sellerStore.error" class="rounded-md bg-red-50 p-4">
            <div class="text-sm text-red-700">{{ sellerStore.error }}</div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="close"
              class="btn-secondary"
              :disabled="sellerStore.isLoading"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="sellerStore.isLoading"
            >
              <span v-if="sellerStore.isLoading">Updating...</span>
              <span v-else>Update Status</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';
import { useSellerStore } from '../../stores/seller';

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

const emit = defineEmits(['close', 'updated']);

const sellerStore = useSellerStore();

const form = reactive({
  status: '',
  tracking_number: ''
});

const errors = ref({});

const close = () => {
  emit('close');
};

const updateStatus = async () => {
  errors.value = {};
  sellerStore.clearError();

  try {
    await sellerStore.updateOrderStatus(props.order.id, form);
    emit('updated');
    close();
    
    // Reset form
    Object.assign(form, {
      status: '',
      tracking_number: ''
    });
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    }
  }
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

// Initialize form when modal opens
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    errors.value = {};
    sellerStore.clearError();
    
    // Set next available status based on current status
    if (props.order) {
      if (props.order.status === 'pending') {
        form.status = 'processing';
      } else if (props.order.status === 'processing') {
        form.status = 'shipped';
      }
    }
  }
});
</script>