<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Update Inventory</h3>
          <button @click="close" class="text-gray-400 hover:text-gray-500">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Book Info -->
        <div v-if="book" class="flex items-center space-x-4 mb-6 p-4 bg-gray-50 rounded-lg">
          <img
            :src="book.cover_image"
            :alt="book.title"
            class="w-16 h-20 object-cover rounded"
            @error="handleImageError"
          />
          <div>
            <h4 class="font-medium text-gray-900">{{ book.title }}</h4>
            <p class="text-sm text-gray-600">Current stock: {{ book.stock_quantity }}</p>
          </div>
        </div>

        <!-- Inventory Form -->
        <form @submit.prevent="updateInventory" class="space-y-6">
          <!-- Adjustment Type -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Adjustment Type</label>
            <div class="grid grid-cols-2 gap-4">
              <button
                type="button"
                @click="form.adjustment_type = 'set'"
                :class="[
                  'p-3 border rounded-lg text-center transition-colors',
                  form.adjustment_type === 'set'
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                ]"
              >
                Set Quantity
              </button>
              <button
                type="button"
                @click="form.adjustment_type = 'add'"
                :class="[
                  'p-3 border rounded-lg text-center transition-colors',
                  form.adjustment_type === 'add'
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-300 text-gray-700 hover:bg-gray-50'
                ]"
              >
                Add Stock
              </button>
            </div>
          </div>

          <!-- Quantity -->
          <div>
            <label for="adjustment_amount" class="block text-sm font-medium text-gray-700">
              {{ form.adjustment_type === 'set' ? 'Set Quantity To' : 'Add Quantity' }}
            </label>
            <input
              id="adjustment_amount"
              v-model="form.adjustment_amount"
              type="number"
              :min="form.adjustment_type === 'set' ? 0 : 1"
              required
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.adjustment_amount }"
            />
            <p v-if="errors.adjustment_amount" class="mt-1 text-sm text-red-600">{{ errors.adjustment_amount[0] }}</p>
            
            <div v-if="form.adjustment_type === 'set'" class="mt-2 text-sm text-gray-600">
              Current stock: {{ book?.stock_quantity || 0 }}
            </div>
            <div v-if="form.adjustment_type === 'add'" class="mt-2 text-sm text-gray-600">
              New total: {{ (book?.stock_quantity || 0) + (parseInt(form.adjustment_amount) || 0) }}
            </div>
          </div>

          <!-- Reason -->
          <div>
            <label for="reason" class="block text-sm font-medium text-gray-700">Reason</label>
            <select
              id="reason"
              v-model="form.reason"
              required
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.reason }"
            >
              <option value="">Select a reason</option>
              <option value="restock">Restock</option>
              <option value="damaged">Damaged Items</option>
              <option value="lost">Lost Items</option>
              <option value="sold">Sold Items</option>
              <option value="other">Other</option>
            </select>
            <p v-if="errors.reason" class="mt-1 text-sm text-red-600">{{ errors.reason[0] }}</p>
          </div>

          <!-- Notes -->
          <div>
            <label for="notes" class="block text-sm font-medium text-gray-700">Notes (Optional)</label>
            <textarea
              id="notes"
              v-model="form.notes"
              rows="2"
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.notes }"
              placeholder="Additional information about this inventory adjustment..."
            ></textarea>
            <p v-if="errors.notes" class="mt-1 text-sm text-red-600">{{ errors.notes[0] }}</p>
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
              <span v-else>Update Inventory</span>
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
  book: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close', 'updated']);

const sellerStore = useSellerStore();

const form = reactive({
  stock_quantity: 0,
  adjustment_type: 'set', // 'set' or 'add'
  adjustment_amount: 0,
  reason: '',
  notes: ''
});

const errors = ref({});

const close = () => {
  emit('close');
};

const updateInventory = async () => {
  errors.value = {};
  sellerStore.clearError();

  try {
    await sellerStore.updateInventory(props.book.id, form);
    emit('updated');
    close();
    
    // Reset form
    Object.assign(form, {
      stock_quantity: 0,
      adjustment_type: 'set',
      adjustment_amount: 0,
      reason: '',
      notes: ''
    });
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    }
  }
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};

// Initialize form when modal opens
watch(() => props.isOpen, (isOpen) => {
  if (isOpen && props.book) {
    errors.value = {};
    sellerStore.clearError();
    form.stock_quantity = props.book.stock_quantity;
    form.adjustment_amount = props.book.stock_quantity;
  }
});
</script>