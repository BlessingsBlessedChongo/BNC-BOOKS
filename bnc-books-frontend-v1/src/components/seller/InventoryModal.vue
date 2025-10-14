<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 overflow-y-auto z-50"
    aria-labelledby="modal-title"
    role="dialog"
    aria-modal="true"
  >
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        aria-hidden="true"
        @click="$emit('close')"
      ></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <div class="sm:flex sm:items-start">
          <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 sm:mx-0 sm:h-10 sm:w-10">
            <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
            </svg>
          </div>
          <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
              Update Inventory - {{ book.title }}
            </h3>
            <div class="mt-4">
              <form @submit.prevent="updateStock">
                <div class="space-y-4">
                  <!-- Current Stock -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700">
                      Current Stock
                    </label>
                    <p class="mt-1 text-sm text-gray-500">
                      {{ book.stock_quantity }} units available
                    </p>
                  </div>

                  <!-- Stock Adjustment -->
                  <div>
                    <label for="adjustment_type" class="block text-sm font-medium text-gray-700">
                      Adjustment Type
                    </label>
                    <select
                      id="adjustment_type"
                      v-model="form.adjustment_type"
                      class="mt-1 input-field"
                    >
                      <option value="set">Set to specific quantity</option>
                      <option value="add">Add to current stock</option>
                      <option value="subtract">Subtract from current stock</option>
                    </select>
                  </div>

                  <!-- Quantity -->
                  <div>
                    <label for="quantity" class="block text-sm font-medium text-gray-700">
                      Quantity
                    </label>
                    <input
                      type="number"
                      id="quantity"
                      v-model="form.quantity"
                      min="0"
                      class="mt-1 input-field"
                      :class="{ 'border-red-500': errors.quantity }"
                    />
                    <p v-if="errors.quantity" class="mt-2 text-sm text-red-600">{{ errors.quantity }}</p>
                    <p class="mt-1 text-sm text-gray-500">
                      New stock will be: {{ calculatedQuantity }}
                    </p>
                  </div>

                  <!-- Reason -->
                  <div>
                    <label for="reason" class="block text-sm font-medium text-gray-700">
                      Reason (Optional)
                    </label>
                    <select
                      id="reason"
                      v-model="form.reason"
                      class="mt-1 input-field"
                    >
                      <option value="">Select a reason</option>
                      <option value="restock">Restock</option>
                      <option value="sale">Sale</option>
                      <option value="damaged">Damaged/Lost</option>
                      <option value="return">Customer Return</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <!-- Notes -->
                  <div v-if="form.reason === 'other'">
                    <label for="notes" class="block text-sm font-medium text-gray-700">
                      Notes
                    </label>
                    <textarea
                      id="notes"
                      v-model="form.notes"
                      rows="3"
                      class="mt-1 input-field"
                      placeholder="Additional details about this inventory adjustment..."
                    ></textarea>
                  </div>
                </div>

                <div class="mt-6 flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="$emit('close')"
                    class="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    :disabled="sellerStore.isLoading"
                    class="btn-primary"
                  >
                    <span v-if="sellerStore.isLoading">Updating...</span>
                    <span v-else>Update Stock</span>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useSellerStore } from '@/stores/seller'

const props = defineProps({
  book: {
    type: Object,
    default: null
  },
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'update'])

const sellerStore = useSellerStore()

const form = reactive({
  adjustment_type: 'set',
  quantity: 0,
  reason: '',
  notes: ''
})

const errors = reactive({})

const calculatedQuantity = computed(() => {
  if (!props.book) return 0

  const currentStock = props.book.stock_quantity
  const adjustment = parseInt(form.quantity) || 0

  switch (form.adjustment_type) {
    case 'set':
      return adjustment
    case 'add':
      return currentStock + adjustment
    case 'subtract':
      return Math.max(0, currentStock - adjustment)
    default:
      return currentStock
  }
})

const validateForm = () => {
  let isValid = true
  errors.quantity = ''

  const quantity = parseInt(form.quantity)
  if (isNaN(quantity) || quantity < 0) {
    errors.quantity = 'Please enter a valid quantity'
    isValid = false
  }

  if (form.adjustment_type === 'subtract' && quantity > props.book.stock_quantity) {
    errors.quantity = 'Cannot subtract more than current stock'
    isValid = false
  }

  return isValid
}

const updateStock = () => {
  if (!validateForm()) return

  const stockData = {
    stock_quantity: calculatedQuantity.value,
    adjustment_type: form.adjustment_type,
    adjustment_amount: parseInt(form.quantity),
    reason: form.reason,
    notes: form.notes
  }

  emit('update', stockData)
}
</script>