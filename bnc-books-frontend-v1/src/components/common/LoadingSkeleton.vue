<template>
  <div :class="['animate-pulse', containerClass]">
    <!-- Book Card Skeleton -->
    <div v-if="type === 'book-card'" class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div class="bg-gray-200 h-48 w-full"></div>
      <div class="p-4 space-y-3">
        <div class="h-4 bg-gray-200 rounded w-3/4"></div>
        <div class="h-3 bg-gray-200 rounded w-1/2"></div>
        <div class="flex items-center space-x-1">
          <div class="h-4 w-16 bg-gray-200 rounded"></div>
        </div>
        <div class="h-5 bg-gray-200 rounded w-1/4"></div>
        <div class="flex space-x-2 pt-2">
          <div class="h-9 bg-gray-200 rounded flex-1"></div>
          <div class="h-9 w-9 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>

    <!-- Book List Skeleton -->
    <div v-else-if="type === 'book-list'" class="space-y-4">
      <div v-for="n in count" :key="n" class="flex space-x-4 p-4 bg-white rounded-lg border border-gray-200">
        <div class="flex-shrink-0">
          <div class="w-20 h-28 bg-gray-200 rounded"></div>
        </div>
        <div class="flex-1 space-y-2">
          <div class="h-5 bg-gray-200 rounded w-3/4"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          <div class="h-4 bg-gray-200 rounded w-1/4"></div>
          <div class="flex space-x-2 pt-2">
            <div class="h-8 bg-gray-200 rounded w-24"></div>
            <div class="h-8 bg-gray-200 rounded w-8"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Table Skeleton -->
    <div v-else-if="type === 'table'" class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
      <div class="p-4 border-b border-gray-200">
        <div class="h-6 bg-gray-200 rounded w-1/4"></div>
      </div>
      <div class="divide-y divide-gray-200">
        <div v-for="n in count" :key="n" class="p-4">
          <div class="flex items-center justify-between">
            <div class="space-y-2 flex-1">
              <div class="h-4 bg-gray-200 rounded w-1/2"></div>
              <div class="h-3 bg-gray-200 rounded w-1/4"></div>
            </div>
            <div class="h-8 bg-gray-200 rounded w-20"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Profile Skeleton -->
    <div v-else-if="type === 'profile'" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div class="flex items-center space-x-4">
        <div class="w-16 h-16 bg-gray-200 rounded-full"></div>
        <div class="space-y-2 flex-1">
          <div class="h-5 bg-gray-200 rounded w-1/3"></div>
          <div class="h-4 bg-gray-200 rounded w-1/4"></div>
        </div>
      </div>
      <div class="mt-6 space-y-4">
        <div v-for="n in 3" :key="n" class="space-y-2">
          <div class="h-4 bg-gray-200 rounded w-1/6"></div>
          <div class="h-10 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>

    <!-- Text Skeleton -->
    <div v-else-if="type === 'text'" class="space-y-2">
      <div v-for="n in count" :key="n" :class="['bg-gray-200 rounded', heightClass]"></div>
    </div>

    <!-- Custom Skeleton -->
    <div v-else class="bg-gray-200 rounded" :style="{ width, height }"></div>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'text', // 'book-card', 'book-list', 'table', 'profile', 'text'
    validator: (value) => ['book-card', 'book-list', 'table', 'profile', 'text', 'custom'].includes(value)
  },
  count: {
    type: Number,
    default: 1
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '1rem'
  },
  containerClass: {
    type: String,
    default: ''
  },
  heightClass: {
    type: String,
    default: 'h-4'
  }
})
</script>