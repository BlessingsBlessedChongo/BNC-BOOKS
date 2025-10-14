<template>
  <div class="card p-6 mb-6">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <!-- Search -->
      <div class="flex-1 max-w-md">
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <input
            v-model="localFilters.search"
            type="text"
            placeholder="Search orders..."
            class="input-field pl-10"
            @input="debouncedApplyFilters"
          />
        </div>
      </div>

      <!-- Filters -->
      <div class="flex flex-wrap items-center gap-4">
        <!-- Status Filter -->
        <select
          v-model="localFilters.status"
          class="input-field text-sm"
          @change="applyFilters"
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="processing">Processing</option>
          <option value="shipped">Shipped</option>
          <option value="delivered">Delivered</option>
          <option value="cancelled">Cancelled</option>
        </select>

        <!-- Date Range -->
        <div class="flex items-center space-x-2">
          <input
            v-model="localFilters.date_from"
            type="date"
            class="input-field text-sm"
            @change="applyFilters"
          />
          <span class="text-gray-500">to</span>
          <input
            v-model="localFilters.date_to"
            type="date"
            class="input-field text-sm"
            @change="applyFilters"
          />
        </div>

        <!-- Clear Filters -->
        <button
          @click="clearFilters"
          class="btn-secondary text-sm"
        >
          Clear
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { useOrderStore } from '@/stores/orders'

const orderStore = useOrderStore()

const localFilters = reactive({
  status: '',
  date_from: '',
  date_to: '',
  search: ''
})

// Initialize with current filters
onMounted(() => {
  Object.assign(localFilters, orderStore.filters)
})

// Debounced search
const debouncedApplyFilters = useDebounceFn(() => {
  applyFilters()
}, 500)

const applyFilters = () => {
  orderStore.updateFilters(localFilters)
}

const clearFilters = () => {
  orderStore.clearFilters()
  Object.assign(localFilters, orderStore.filters)
}
</script>