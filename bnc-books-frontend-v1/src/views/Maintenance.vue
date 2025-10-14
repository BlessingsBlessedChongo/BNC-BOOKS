<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full text-center">
      <Cog6ToothIcon class="mx-auto h-24 w-24 text-gray-400 animate-spin" />
      <h1 class="mt-6 text-3xl font-bold text-gray-900">Under Maintenance</h1>
      <p class="mt-4 text-lg text-gray-600">
        BNC Books is currently undergoing scheduled maintenance. We'll be back soon!
      </p>
      <p class="mt-2 text-sm text-gray-500">
        Expected completion: {{ estimatedCompletion }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { Cog6ToothIcon } from '@heroicons/vue/24/outline'

const estimatedCompletion = new Date(Date.now() + 2 * 60 * 60 * 1000).toLocaleTimeString('en-US', {
  hour: 'numeric',
  minute: '2-digit',
  timeZoneName: 'short'
})
</script>