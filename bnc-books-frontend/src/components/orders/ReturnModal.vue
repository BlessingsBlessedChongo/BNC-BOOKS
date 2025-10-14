<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Request Return</h3>
          <button @click="close" class="text-gray-400 hover:text-gray-500">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Order Info -->
        <div v-if="order" class="mb-6 p-4 bg-gray-50 rounded-lg">
          <p class="font-medium text-gray-900">Order #{{ order.order_number }}</p>
          <p class="text-sm text-gray-600">Placed on {{ formatDate(order.created_at) }}</p>
        </div>

        <!-- Return Form -->
        <form @submit.prevent="submitReturn" class="space-y-6">
          <!-- Reason -->
          <div>
            <label for="reason" class="block text-sm font-medium text-gray-700">Reason for return</label>
            <select
              id="reason"
              v-model="form.reason"
              required
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.reason }"
            >
              <option value="">Select a reason</option>
              <option value="damaged">Item arrived damaged</option>
              <option value="wrong_item">Wrong item was sent</option>
              <option value="not_as_described">Item not as described</option>
              <option value="changed_mind">Changed my mind</option>
              <option value="other">Other</option>
            </select>
            <p v-if="errors.reason" class="mt-1 text-sm text-red-600">{{ errors.reason[0] }}</p>
          </div>

          <!-- Comments -->
          <div>
            <label for="comments" class="block text-sm font-medium text-gray-700">Additional comments</label>
            <textarea
              id="comments"
              v-model="form.comments"
              rows="3"
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.comments }"
              placeholder="Please provide any additional details about your return..."
            ></textarea>
            <p v-if="errors.comments" class="mt-1 text-sm text-red-600">{{ errors.comments[0] }}</p>
          </div>

          <!-- Items to Return -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Items to return</label>
            <div class="space-y-3">
              <div 
                v-for="item in order.items" 
                :key="item.id"
                class="flex items-center justify-between p-3 border border-gray-200 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <input
                    :id="`item-${item.id}`"
                    v-model="form.return_items"
                    :value="{ order_item: item.id, quantity: 1, reason: form.reason }"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <img
                    :src="item.book.cover_image"
                    :alt="item.book.title"
                    class="w-12 h-16 object-cover rounded"
                    @error="handleImageError"
                  />
                  <div>
                    <label :for="`item-${item.id}`" class="font-medium text-gray-900 cursor-pointer">
                      {{ item.book.title }}
                    </label>
                    <p class="text-sm text-gray-600">Qty: {{ item.quantity }}</p>
                  </div>
                </div>
              </div>
            </div>
            <p v-if="errors.return_items" class="mt-1 text-sm text-red-600">{{ errors.return_items[0] }}</p>
          </div>

          <!-- Error Message -->
          <div v-if="ordersStore.error" class="rounded-md bg-red-50 p-4">
            <div class="text-sm text-red-700">{{ ordersStore.error }}</div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="close"
              class="btn-secondary"
              :disabled="ordersStore.isLoading"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="ordersStore.isLoading || form.return_items.length === 0"
            >
              <span v-if="ordersStore.isLoading">Submitting...</span>
              <span v-else>Submit Return Request</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';
import { useOrdersStore } from '../../stores/orders';

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

const emit = defineEmits(['close', 'submitted']);

const ordersStore = useOrdersStore();

const form = reactive({
  reason: '',
  comments: '',
  return_items: []
});

const errors = ref({});

const close = () => {
  emit('close');
};

const submitReturn = async () => {
  errors.value = {};
  ordersStore.clearError();

  try {
    await ordersStore.requestReturn(props.order.id, form);
    emit('submitted');
    close();
    
    // Reset form
    Object.assign(form, {
      reason: '',
      comments: '',
      return_items: []
    });
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    }
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};

// Clear errors when modal opens
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    errors.value = {};
    ordersStore.clearError();
  }
});
</script>