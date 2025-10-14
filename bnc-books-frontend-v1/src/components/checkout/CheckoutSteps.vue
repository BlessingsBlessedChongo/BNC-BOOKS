<template>
  <nav aria-label="Progress">
    <ol class="flex items-center">
      <li
        v-for="(step, index) in steps"
        :key="step.name"
        :class="[
          'relative',
          index !== steps.length - 1 ? 'pr-8 sm:pr-20' : '',
        ]"
      >
        <!-- Step Connector -->
        <div
          v-if="index !== steps.length - 1"
          class="absolute inset-0 flex items-center"
          aria-hidden="true"
        >
          <div
            class="h-0.5 w-full"
            :class="
              step.status === 'complete'
                ? 'bg-primary-600'
                : step.status === 'current'
                ? 'bg-primary-200'
                : 'bg-gray-200'
            "
          />
        </div>

        <!-- Step -->
        <div class="relative flex items-center group">
          <span
            class="h-9 flex items-center"
            :aria-current="step.status === 'current' ? 'step' : undefined"
          >
            <span
              class="relative z-10 w-8 h-8 flex items-center justify-center rounded-full transition-colors duration-200"
              :class="
                step.status === 'complete'
                  ? 'bg-primary-600 hover:bg-primary-900'
                  : step.status === 'current'
                  ? 'bg-primary-600 border-2 border-primary-600'
                  : 'bg-gray-200 hover:bg-gray-300'
              "
            >
              <template v-if="step.status === 'complete'">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </template>
              <template v-else-if="step.status === 'current'">
                <span class="h-2.5 w-2.5 bg-white rounded-full" />
              </template>
              <template v-else>
                <span class="h-2.5 w-2.5 bg-transparent rounded-full group-hover:bg-gray-500" />
              </template>
            </span>
          </span>
          <span
            class="ml-3 text-sm font-medium transition-colors duration-200"
            :class="
              step.status === 'complete' || step.status === 'current'
                ? 'text-primary-600'
                : 'text-gray-500'
            "
          >
            {{ step.name }}
          </span>
        </div>
      </li>
    </ol>
  </nav>
</template>

<script setup>
defineProps({
  steps: {
    type: Array,
    required: true,
    validator: (steps) => {
      return steps.every(step => 
        ['name', 'status'].every(prop => prop in step) &&
        ['complete', 'current', 'upcoming'].includes(step.status)
      )
    }
  }
})
</script>