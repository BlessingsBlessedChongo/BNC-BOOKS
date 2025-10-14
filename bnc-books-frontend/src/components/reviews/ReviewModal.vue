<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Write a Review</h3>
          <button @click="close" class="text-gray-400 hover:text-gray-500">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Book Info -->
        <div v-if="book" class="flex items-center space-x-4 mb-6 p-4 bg-gray-50 rounded-lg">
          <img
            :src="book.cover_image"
            :alt="book.title"
            class="w-16 h-20 object-cover rounded"
            @error="handleImageError"
          />
          <div>
            <h4 class="font-medium text-gray-900">{{ book.title }}</h4>
            <p class="text-sm text-gray-600">by {{ book.author }}</p>
          </div>
        </div>

        <!-- Review Form -->
        <form @submit.prevent="submitReview" class="space-y-6">
          <!-- Rating -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Rating</label>
            <div class="flex items-center space-x-1">
              <button
                v-for="star in 5"
                :key="star"
                type="button"
                @click="form.rating = star"
                class="p-1 focus:outline-none"
              >
                <svg
                  class="w-8 h-8"
                  :class="star <= form.rating ? 'text-yellow-400' : 'text-gray-300'"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </button>
            </div>
            <p v-if="errors.rating" class="mt-1 text-sm text-red-600">{{ errors.rating[0] }}</p>
          </div>

          <!-- Title -->
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700">Review Title</label>
            <input
              id="title"
              v-model="form.title"
              type="text"
              required
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.title }"
              placeholder="Summarize your experience"
            />
            <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title[0] }}</p>
          </div>

          <!-- Comment -->
          <div>
            <label for="comment" class="block text-sm font-medium text-gray-700">Your Review</label>
            <textarea
              id="comment"
              v-model="form.comment"
              rows="4"
              required
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.comment }"
              placeholder="Share your thoughts about this book..."
            ></textarea>
            <p v-if="errors.comment" class="mt-1 text-sm text-red-600">{{ errors.comment[0] }}</p>
          </div>

          <!-- Pros -->
          <div>
            <label for="pros" class="block text-sm font-medium text-gray-700">What did you like?</label>
            <textarea
              id="pros"
              v-model="form.pros"
              rows="2"
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.pros }"
              placeholder="What stood out in a positive way?"
            ></textarea>
            <p v-if="errors.pros" class="mt-1 text-sm text-red-600">{{ errors.pros[0] }}</p>
          </div>

          <!-- Cons -->
          <div>
            <label for="cons" class="block text-sm font-medium text-gray-700">What could be better?</label>
            <textarea
              id="cons"
              v-model="form.cons"
              rows="2"
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.cons }"
              placeholder="Any areas for improvement?"
            ></textarea>
            <p v-if="errors.cons" class="mt-1 text-sm text-red-600">{{ errors.cons[0] }}</p>
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

          <!-- Error Message -->
          <div v-if="reviewsStore.error" class="rounded-md bg-red-50 p-4">
            <div class="text-sm text-red-700">{{ reviewsStore.error }}</div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="close"
              class="btn-secondary"
              :disabled="reviewsStore.isLoading"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="reviewsStore.isLoading"
            >
              <span v-if="reviewsStore.isLoading">Submitting...</span>
              <span v-else>Submit Review</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';
import { useReviewsStore } from '../../stores/reviews';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  book: {
    type: Object,
    default: null
  },
  orderItem: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close', 'submitted']);

const reviewsStore = useReviewsStore();

const form = reactive({
  book: props.book?.id || '',
  rating: 5,
  title: '',
  comment: '',
  pros: '',
  cons: '',
  would_recommend: true
});

const errors = ref({});

const close = () => {
  emit('close');
};

const submitReview = async () => {
  errors.value = {};
  reviewsStore.clearError();

  try {
    await reviewsStore.createReview(form);
    emit('submitted');
    close();
    
    // Reset form
    Object.assign(form, {
      book: props.book?.id || '',
      rating: 5,
      title: '',
      comment: '',
      pros: '',
      cons: '',
      would_recommend: true
    });
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    }
  }
};

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};

// Update book ID when prop changes
watch(() => props.book, (newBook) => {
  if (newBook) {
    form.book = newBook.id;
  }
});

// Clear errors when modal opens
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    errors.value = {};
    reviewsStore.clearError();
  }
});
</script>