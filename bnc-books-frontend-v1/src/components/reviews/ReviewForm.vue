<template>
  <div class="card p-6">
    <h3 class="text-lg font-medium text-gray-900 mb-4">
      {{ editingReview ? 'Edit Review' : 'Write a Review' }}
    </h3>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Rating -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Overall Rating
        </label>
        <div class="flex items-center space-x-1">
          <button
            v-for="rating in 5"
            :key="rating"
            type="button"
            @click="form.rating = rating"
            class="p-1 focus:outline-none"
          >
            <svg
              class="w-8 h-8 transition-colors duration-200"
              :class="rating <= form.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
        </div>
        <p v-if="errors.rating" class="mt-2 text-sm text-red-600">{{ errors.rating }}</p>
      </div>

      <!-- Review Title -->
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700">
          Review Title
        </label>
        <input
          type="text"
          id="title"
          v-model="form.title"
          placeholder="Summarize your experience"
          class="mt-1 input-field"
          :class="{ 'border-red-500': errors.title }"
        />
        <p v-if="errors.title" class="mt-2 text-sm text-red-600">{{ errors.title }}</p>
      </div>

      <!-- Review Comment -->
      <div>
        <label for="comment" class="block text-sm font-medium text-gray-700">
          Your Review
        </label>
        <textarea
          id="comment"
          v-model="form.comment"
          rows="4"
          placeholder="Share your thoughts about this book..."
          class="mt-1 input-field"
          :class="{ 'border-red-500': errors.comment }"
        ></textarea>
        <p v-if="errors.comment" class="mt-2 text-sm text-red-600">{{ errors.comment }}</p>
        <p class="mt-1 text-sm text-gray-500">
          {{ form.comment.length }}/1000 characters
        </p>
      </div>

      <!-- Pros and Cons -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="pros" class="block text-sm font-medium text-gray-700">
            What you liked
          </label>
          <textarea
            id="pros"
            v-model="form.pros"
            rows="3"
            placeholder="What did you enjoy about this book?"
            class="mt-1 input-field"
          ></textarea>
        </div>

        <div>
          <label for="cons" class="block text-sm font-medium text-gray-700">
            What could be better
          </label>
          <textarea
            id="cons"
            v-model="form.cons"
            rows="3"
            placeholder="Any areas for improvement?"
            class="mt-1 input-field"
          ></textarea>
        </div>
      </div>

      <!-- Would Recommend -->
      <div class="flex items-center">
        <input
          id="would_recommend"
          v-model="form.would_recommend"
          type="checkbox"
          class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
        />
        <label for="would_recommend" class="ml-2 block text-sm text-gray-900">
          I would recommend this book to others
        </label>
      </div>

      <!-- Form Actions -->
      <div class="flex items-center justify-end space-x-3 pt-4 border-t border-gray-200">
        <button
          v-if="editingReview"
          type="button"
          @click="$emit('cancel')"
          class="btn-secondary"
        >
          Cancel
        </button>
        <button
          type="submit"
          :disabled="reviewStore.isLoading"
          class="btn-primary"
        >
          <span v-if="reviewStore.isLoading">
            {{ editingReview ? 'Updating...' : 'Submitting...' }}
          </span>
          <span v-else>
            {{ editingReview ? 'Update Review' : 'Submit Review' }}
          </span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useReviewStore } from '@/stores/reviews'
import { useNotificationStore } from '@/stores/notifications'

const props = defineProps({
  bookId: {
    type: [String, Number],
    required: true
  },
  editingReview: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['success', 'cancel'])

const reviewStore = useReviewStore()
const notificationStore = useNotificationStore()

const form = reactive({
  rating: 0,
  title: '',
  comment: '',
  pros: '',
  cons: '',
  would_recommend: true
})

const errors = reactive({})

// Initialize form with editing review data
watch(() => props.editingReview, (review) => {
  if (review) {
    Object.assign(form, {
      rating: review.rating,
      title: review.title,
      comment: review.comment,
      pros: review.pros || '',
      cons: review.cons || '',
      would_recommend: review.would_recommend
    })
  } else {
    resetForm()
  }
}, { immediate: true })

const validateForm = () => {
  let isValid = true
  Object.keys(errors).forEach(key => delete errors[key])

  if (!form.rating || form.rating < 1 || form.rating > 5) {
    errors.rating = 'Please select a rating between 1 and 5 stars'
    isValid = false
  }

  if (!form.title.trim()) {
    errors.title = 'Review title is required'
    isValid = false
  } else if (form.title.length > 200) {
    errors.title = 'Title must be less than 200 characters'
    isValid = false
  }

  if (!form.comment.trim()) {
    errors.comment = 'Review comment is required'
    isValid = false
  } else if (form.comment.length > 1000) {
    errors.comment = 'Comment must be less than 1000 characters'
    isValid = false
  }

  return isValid
}

const resetForm = () => {
  Object.assign(form, {
    rating: 0,
    title: '',
    comment: '',
    pros: '',
    cons: '',
    would_recommend: true
  })
  Object.keys(errors).forEach(key => delete errors[key])
}

const submitForm = async () => {
  if (!validateForm()) return

  const reviewData = {
    book: props.bookId,
    rating: form.rating,
    title: form.title,
    comment: form.comment,
    pros: form.pros,
    cons: form.cons,
    would_recommend: form.would_recommend
  }

  let result
  if (props.editingReview) {
    result = await reviewStore.updateReview(props.editingReview.id, reviewData)
  } else {
    result = await reviewStore.createReview(reviewData)
  }

  if (result.success) {
    notificationStore.success(
      props.editingReview ? 'Review updated successfully' : 'Review submitted successfully'
    )
    resetForm()
    emit('success')
  } else {
    notificationStore.error(result.error || 'Failed to submit review')
  }
}
</script>