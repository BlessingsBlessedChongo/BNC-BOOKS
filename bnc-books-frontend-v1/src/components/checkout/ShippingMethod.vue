<template>
  <div class="space-y-4">
    <div
      v-for="method in shippingMethods"
      :key="method.id"
      class="relative flex cursor-pointer rounded-lg border p-4 focus:outline-none"
      :class="
        selectedMethod?.id === method.id
          ? 'border-primary-500 bg-primary-50'
          : 'border-gray-300'
      "
      @click="$emit('select', method)"
    >
      <div class="flex items-center">
        <div class="flex items-center h-5">
          <input
            type="radio"
            :id="`shipping-method-${method.id}`"
            :checked="selectedMethod?.id === method.id"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
          />
        </div>
        <label
          :for="`shipping-method-${method.id}`"
          class="ml-3 flex flex-col cursor-pointer"
        >
          <span class="block text-sm font-medium text-gray-900">
            {{ method.name }}
          </span>
          <span class="block text-sm text-gray-500">
            {{ method.description }}
          </span>
          <span class="block text-sm font-medium text-gray-900 mt-1">
            ${{ method.price.toFixed(2) }}
          </span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  shippingMethods: {
    type: Array,
    default: () => []
  },
  selectedMethod: {
    type: Object,
    default: null
  }
})

defineEmits(['select'])
</script>