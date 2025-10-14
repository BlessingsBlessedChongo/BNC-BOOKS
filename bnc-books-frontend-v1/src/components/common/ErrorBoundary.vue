<template>
  <div v-if="hasError" class="min-h-screen bg-gray-50 flex items-center justify-center px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 text-center">
      <div>
        <ExclamationTriangleIcon class="mx-auto h-24 w-24 text-red-500" />
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
          Something went wrong
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          {{ errorMessage }}
        </p>
        <div class="mt-6 space-y-4">
          <button
            @click="tryAgain"
            class="w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
          >
            Try Again
          </button>
          <button
            @click="goHome"
            class="w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
          >
            Go Home
          </button>
          <button
            v-if="showDetails"
            @click="showErrorDetails = !showErrorDetails"
            class="w-full flex justify-center py-2 px-4 border border-gray-300 text-sm font-medium rounded-lg text-gray-600 bg-white hover:bg-gray-50"
          >
            {{ showErrorDetails ? 'Hide Details' : 'Show Details' }}
          </button>
        </div>
        
        <!-- Error Details -->
        <div v-if="showErrorDetails && errorDetails" class="mt-4 p-4 bg-red-50 rounded-lg text-left">
          <h4 class="text-sm font-medium text-red-800 mb-2">Error Details:</h4>
          <pre class="text-xs text-red-700 overflow-auto">{{ errorDetails }}</pre>
        </div>
      </div>
    </div>
  </div>
  <slot v-else />
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  fallback: {
    type: Function,
    default: null
  },
  showDetails: {
    type: Boolean,
    default: process.env.NODE_ENV === 'development'
  }
})

const router = useRouter()

// State
const hasError = ref(false)
const error = ref(null)
const showErrorDetails = ref(false)

// Computed
const errorMessage = ref('An unexpected error occurred. Please try again.')
const errorDetails = ref('')

// Error handler
onErrorCaptured((err, instance, info) => {
  error.value = err
  hasError.value = true
  
  // Set user-friendly error message
  if (err.response?.data?.message) {
    errorMessage.value = err.response.data.message
  } else if (err.message) {
    errorMessage.value = err.message
  }
  
  // Prepare error details for development
  if (props.showDetails) {
    errorDetails.value = JSON.stringify({
      error: err.toString(),
      info,
      stack: err.stack,
      url: window.location.href,
      timestamp: new Date().toISOString()
    }, null, 2)
  }
  
  // Log to error reporting service
  logError(err, info)
  
  // Prevent the error from propagating further
  return false
})

// Methods
const tryAgain = () => {
  hasError.value = false
  error.value = null
  showErrorDetails.value = false
  window.location.reload()
}

const goHome = () => {
  router.push('/')
}

const logError = (error, info) => {
  // In production, send to your error reporting service
  console.error('Error caught by boundary:', error)
  console.error('Error info:', info)
  
  // Example: Send to Sentry, LogRocket, etc.
  if (window.Sentry) {
    window.Sentry.captureException(error, { extra: { info } })
  }
}

// Global error handler for unhandled errors
const handleGlobalError = (event) => {
  // Only handle errors that haven't been caught by Vue
  if (event.error && !event.error._isVueError) {
    hasError.value = true
    error.value = event.error
    errorMessage.value = 'A critical error occurred. Please refresh the page.'
    
    logError(event.error, { type: 'unhandled' })
  }
}

const handleUnhandledRejection = (event) => {
  hasError.value = true
  error.value = event.reason
  errorMessage.value = 'A promise was rejected. Please try again.'
  
  logError(event.reason, { type: 'unhandled_rejection' })
}

// Register global error handlers
if (typeof window !== 'undefined') {
  window.addEventListener('error', handleGlobalError)
  window.addEventListener('unhandledrejection', handleUnhandledRejection)
}
</script>