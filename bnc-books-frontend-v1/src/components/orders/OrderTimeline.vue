<template>
  <div class="flex items-center justify-between">
    <div
      v-for="(step, index) in timelineSteps"
      :key="step.status"
      class="flex flex-col items-center flex-1"
    >
      <!-- Step Circle -->
      <div
        class="w-8 h-8 rounded-full flex items-center justify-center transition-colors duration-200"
        :class="step.completed ? 'bg-primary-600 text-white' : step.current ? 'bg-primary-100 text-primary-600 border-2 border-primary-600' : 'bg-gray-200 text-gray-400'"
      >
        <template v-if="step.completed">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
        </template>
        <template v-else>
          {{ index + 1 }}
        </template>
      </div>

      <!-- Step Label -->
      <div class="mt-2 text-center">
        <p class="text-xs font-medium" :class="step.completed || step.current ? 'text-primary-600' : 'text-gray-500'">
          {{ step.label }}
        </p>
        <p v-if="step.date" class="text-xs text-gray-400 mt-1">
          {{ formatDate(step.date) }}
        </p>
      </div>

      <!-- Connector Line -->
      <div
        v-if="index < timelineSteps.length - 1"
        class="flex-1 h-0.5 mt-4 -mb-4"
        :class="step.completed ? 'bg-primary-600' : 'bg-gray-200'"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

const timelineSteps = computed(() => {
  const steps = [
    { status: 'pending', label: 'Order Placed', date: props.order.created_at },
    { status: 'processing', label: 'Processing', date: props.order.processing_at },
    { status: 'shipped', label: 'Shipped', date: props.order.shipped_at },
    { status: 'delivered', label: 'Delivered', date: props.order.delivered_at }
  ]

  let currentStepFound = false

  return steps.map(step => {
    const completed = isStepCompleted(step.status)
    const current = !currentStepFound && !completed && isStepRelevant(step.status)
    
    if (current) {
      currentStepFound = true
    }

    return {
      ...step,
      completed,
      current
    }
  })
})

const isStepCompleted = (stepStatus) => {
  const statusOrder = ['pending', 'processing', 'shipped', 'delivered']
  const currentStatusIndex = statusOrder.indexOf(props.order.status)
  const stepIndex = statusOrder.indexOf(stepStatus)
  
  return stepIndex <= currentStatusIndex
}

const isStepRelevant = (stepStatus) => {
  const statusOrder = ['pending', 'processing', 'shipped', 'delivered']
  const currentStatusIndex = statusOrder.indexOf(props.order.status)
  const stepIndex = statusOrder.indexOf(stepStatus)
  
  return stepIndex === currentStatusIndex
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}
</script>