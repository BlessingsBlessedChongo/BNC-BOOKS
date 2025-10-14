<template>
  <div class="card p-6">
    <!-- Review Header -->
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center space-x-3">
        <!-- User Avatar -->
        <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
          <span class="text-sm font-medium text-primary-700">
            {{ review.user.first_name?.[0] }}{{ review.user.last_name?.[0] }}
          </span>
        </div>
        
        <div>
          <h4 class="text-sm font-semibold text-gray-900">
            {{ review.user.first_name }} {{ review.user.last_name }}
          </h4>
          <p class="text-sm text-gray-500">
            {{ formatDate(review.created_at) }}
          </p>
        </div>
      </div>

      <!-- Rating -->
      <div class="flex items-center">
        <div class="flex items-center">
          <svg
            v-for="star in 5"
            :key="star"
            class="w-4 h-4"
            :class="star <= review.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Review Content -->
    <div>
      <h5 class="text-lg font-medium text-gray-900 mb-2">
        {{ review.title }}
      </h5>
      <p class="text-gray-600 leading-relaxed mb-4">
        {{ review.comment }}
      </p>
    </div>

    <!-- Review Actions -->
    <div v-if="isUserReview" class="flex items-center justify-between pt-4 border-t border-gray-200">
      <div class="text-sm text-gray-500">
        Last updated {{ formatDate(review.updated_at) }}
      </div>
      <div class="flex space-x-2">
        <button
          @click="editReview"
          class="text-sm text-primary-600 hover:text-primary-500 font-medium"
        >
          Edit
        </button>
        <button
          @click="deleteReview"
          class="text-sm text-red-600 hover:text-red-500 font-medium"
        >
          Delete
        </button>
      </div>
    </div>

    <!-- Verified Purchase Badge -->
    <div v-if="review.verified_purchase" class="mt-3 flex items-center text-sm text-green-600">
      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
      </svg>
      Verified Purchase
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useReviewStore } from '@/stores/reviews'
import { useNotificationStore } from '@/stores/notifications'

const props = defineProps({
  review: {
    type: Object,
    required: true
  }
})

const authStore = useAuthStore()
const reviewStore = useReviewStore()
const notificationStore = useNotificationStore()

const isUserReview = computed(() => {
  return authStore.user?.id === props.review.user.id
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const editReview = () => {
  // Emit event to parent to open edit modal
  emit('edit', props.review)
}

const deleteReview = async () => {
  if (!confirm('Are you sure you want to delete this review?')) return

  const result = await reviewStore.deleteReview(props.review.id)
  if (result.success) {
    notificationStore.success('Review deleted successfully')
  } else {
    notificationStore.error(result.error || 'Failed to delete review')
  }
}

const emit = defineEmits(['edit'])
</script>