<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="close"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full sm:p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ mode === 'create' ? 'Add New Book' : 'Edit Book' }}
          </h3>
          <button @click="close" class="text-gray-400 hover:text-gray-500">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Book Form -->
        <form @submit.prevent="submitForm" class="space-y-6 max-h-96 overflow-y-auto pr-2">
          <!-- Basic Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="title" class="block text-sm font-medium text-gray-700">Title *</label>
              <input
                id="title"
                v-model="form.title"
                type="text"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.title }"
              />
              <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title[0] }}</p>
            </div>
            <div>
              <label for="author" class="block text-sm font-medium text-gray-700">Author *</label>
              <input
                id="author"
                v-model="form.author"
                type="text"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.author }"
              />
              <p v-if="errors.author" class="mt-1 text-sm text-red-600">{{ errors.author[0] }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="isbn" class="block text-sm font-medium text-gray-700">ISBN *</label>
              <input
                id="isbn"
                v-model="form.isbn"
                type="text"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.isbn }"
              />
              <p v-if="errors.isbn" class="mt-1 text-sm text-red-600">{{ errors.isbn[0] }}</p>
            </div>
            <div>
              <label for="category" class="block text-sm font-medium text-gray-700">Category *</label>
              <select
                id="category"
                v-model="form.category"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.category }"
              >
                <option value="">Select category</option>
                <option value="Fiction">Fiction</option>
                <option value="Non-Fiction">Non-Fiction</option>
                <option value="Science">Science</option>
                <option value="Technology">Technology</option>
                <option value="Business">Business</option>
                <option value="Self-Help">Self-Help</option>
                <option value="Biography">Biography</option>
                <option value="History">History</option>
                <option value="Children">Children</option>
                <option value="Young Adult">Young Adult</option>
              </select>
              <p v-if="errors.category" class="mt-1 text-sm text-red-600">{{ errors.category[0] }}</p>
            </div>
          </div>

          <!-- Description -->
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700">Description *</label>
            <textarea
              id="description"
              v-model="form.description"
              rows="3"
              required
              class="input-field mt-1"
              :class="{ 'border-red-500': errors.description }"
            ></textarea>
            <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description[0] }}</p>
          </div>

          <!-- Pricing -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label for="price" class="block text-sm font-medium text-gray-700">Price *</label>
              <input
                id="price"
                v-model="form.price"
                type="number"
                step="0.01"
                min="0.01"
                max="9999.99"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.price }"
              />
              <p v-if="errors.price" class="mt-1 text-sm text-red-600">{{ errors.price[0] }}</p>
            </div>
            <div>
              <label for="original_price" class="block text-sm font-medium text-gray-700">Original Price</label>
              <input
                id="original_price"
                v-model="form.original_price"
                type="number"
                step="0.01"
                min="0.01"
                max="9999.99"
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.original_price }"
              />
              <p v-if="errors.original_price" class="mt-1 text-sm text-red-600">{{ errors.original_price[0] }}</p>
            </div>
            <div>
              <label for="stock_quantity" class="block text-sm font-medium text-gray-700">Stock Quantity *</label>
              <input
                id="stock_quantity"
                v-model="form.stock_quantity"
                type="number"
                min="0"
                max="999999"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.stock_quantity }"
              />
              <p v-if="errors.stock_quantity" class="mt-1 text-sm text-red-600">{{ errors.stock_quantity[0] }}</p>
            </div>
          </div>

          <!-- Book Details -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label for="language" class="block text-sm font-medium text-gray-700">Language *</label>
              <select
                id="language"
                v-model="form.language"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.language }"
              >
                <option value="">Select language</option>
                <option value="English">English</option>
                <option value="Spanish">Spanish</option>
                <option value="French">French</option>
                <option value="German">German</option>
                <option value="Chinese">Chinese</option>
                <option value="Japanese">Japanese</option>
              </select>
              <p v-if="errors.language" class="mt-1 text-sm text-red-600">{{ errors.language[0] }}</p>
            </div>
            <div>
              <label for="pages" class="block text-sm font-medium text-gray-700">Pages</label>
              <input
                id="pages"
                v-model="form.pages"
                type="number"
                min="1"
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.pages }"
              />
              <p v-if="errors.pages" class="mt-1 text-sm text-red-600">{{ errors.pages[0] }}</p>
            </div>
            <div>
              <label for="condition" class="block text-sm font-medium text-gray-700">Condition *</label>
              <select
                id="condition"
                v-model="form.condition"
                required
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.condition }"
              >
                <option value="">Select condition</option>
                <option value="new">New</option>
                <option value="like_new">Like New</option>
                <option value="very_good">Very Good</option>
                <option value="good">Good</option>
                <option value="acceptable">Acceptable</option>
              </select>
              <p v-if="errors.condition" class="mt-1 text-sm text-red-600">{{ errors.condition[0] }}</p>
            </div>
          </div>

          <!-- Publication Details -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="publisher" class="block text-sm font-medium text-gray-700">Publisher</label>
              <input
                id="publisher"
                v-model="form.publisher"
                type="text"
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.publisher }"
              />
              <p v-if="errors.publisher" class="mt-1 text-sm text-red-600">{{ errors.publisher[0] }}</p>
            </div>
            <div>
              <label for="publication_date" class="block text-sm font-medium text-gray-700">Publication Date</label>
              <input
                id="publication_date"
                v-model="form.publication_date"
                type="date"
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.publication_date }"
              />
              <p v-if="errors.publication_date" class="mt-1 text-sm text-red-600">{{ errors.publication_date[0] }}</p>
            </div>
          </div>

          <!-- Genres -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Genres</label>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="genre in availableGenres"
                :key="genre"
                @click="toggleGenre(genre)"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm cursor-pointer transition-colors"
                :class="form.genres.includes(genre) ? 'bg-primary-100 text-primary-800' : 'bg-gray-100 text-gray-800 hover:bg-gray-200'"
              >
                {{ genre }}
              </span>
            </div>
            <p v-if="errors.genres" class="mt-1 text-sm text-red-600">{{ errors.genres[0] }}</p>
          </div>

          <!-- Images -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="cover_image" class="block text-sm font-medium text-gray-700">Cover Image URL</label>
              <input
                id="cover_image"
                v-model="form.cover_image"
                type="url"
                class="input-field mt-1"
                :class="{ 'border-red-500': errors.cover_image }"
              />
              <p v-if="errors.cover_image" class="mt-1 text-sm text-red-600">{{ errors.cover_image[0] }}</p>
            </div>
            <div>
              <label for="additional_images" class="block text-sm font-medium text-gray-700">Additional Images (URLs, comma separated)</label>
              <input
                id="additional_images"
                v-model="additionalImagesInput"
                type="text"
                class="input-field mt-1"
                placeholder="https://example.com/image1.jpg, https://example.com/image2.jpg"
              />
            </div>
          </div>

          <!-- Status -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex items-center">
              <input
                id="is_published"
                v-model="form.is_published"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="is_published" class="ml-2 block text-sm text-gray-900">
                Publish this book
              </label>
            </div>
            <div class="flex items-center">
              <input
                id="is_featured"
                v-model="form.is_featured"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="is_featured" class="ml-2 block text-sm text-gray-900">
                Feature this book
              </label>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="sellerStore.error" class="rounded-md bg-red-50 p-4">
            <div class="text-sm text-red-700">{{ sellerStore.error }}</div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="close"
              class="btn-secondary"
              :disabled="sellerStore.isLoading"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="sellerStore.isLoading"
            >
              <span v-if="sellerStore.isLoading">Saving...</span>
              <span v-else>{{ mode === 'create' ? 'Create Book' : 'Update Book' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';
import { useSellerStore } from '../../stores/seller';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  book: {
    type: Object,
    default: null
  },
  mode: {
    type: String,
    default: 'create' // 'create' or 'edit'
  }
});

const emit = defineEmits(['close', 'saved']);

const sellerStore = useSellerStore();

const availableGenres = [
  'Fantasy', 'Science Fiction', 'Mystery', 'Thriller', 'Romance', 
  'Historical', 'Horror', 'Adventure', 'Biography', 'Self-Help',
  'Business', 'Science', 'Technology', 'Cooking', 'Travel',
  'Art', 'Philosophy', 'Religion', 'Health', 'Sports'
];

const form = reactive({
  title: '',
  author: '',
  isbn: '',
  description: '',
  price: '',
  original_price: '',
  stock_quantity: 0,
  category: '',
  language: 'English',
  pages: '',
  publisher: '',
  publication_date: '',
  condition: 'new',
  genres: [],
  cover_image: '',
  additional_images: [],
  is_published: true,
  is_featured: false
});

const additionalImagesInput = ref('');
const errors = ref({});

const close = () => {
  emit('close');
};

const toggleGenre = (genre) => {
  const index = form.genres.indexOf(genre);
  if (index > -1) {
    form.genres.splice(index, 1);
  } else {
    form.genres.push(genre);
  }
};

const submitForm = async () => {
  errors.value = {};
  sellerStore.clearError();

  // Process additional images
  if (additionalImagesInput.value) {
    form.additional_images = additionalImagesInput.value
      .split(',')
      .map(url => url.trim())
      .filter(url => url);
  }

  try {
    if (props.mode === 'create') {
      await sellerStore.createBook(form);
    } else {
      await sellerStore.updateBook(props.book.id, form);
    }
    emit('saved');
    close();
  } catch (error) {
    if (error.response?.data) {
      errors.value = error.response.data;
    }
  }
};

// Initialize form when modal opens or book changes
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    errors.value = {};
    sellerStore.clearError();
    
    if (props.book && props.mode === 'edit') {
      // Populate form with existing book data
      Object.keys(form).forEach(key => {
        if (props.book[key] !== undefined) {
          form[key] = props.book[key];
        }
      });
      // Set additional images input
      additionalImagesInput.value = Array.isArray(props.book.additional_images) 
        ? props.book.additional_images.join(', ') 
        : '';
    } else {
      // Reset form for create mode
      Object.keys(form).forEach(key => {
        if (key === 'stock_quantity') {
          form[key] = 0;
        } else if (key === 'is_published') {
          form[key] = true;
        } else if (key === 'is_featured') {
          form[key] = false;
        } else if (key === 'language') {
          form[key] = 'English';
        } else if (key === 'condition') {
          form[key] = 'new';
        } else if (Array.isArray(form[key])) {
          form[key] = [];
        } else {
          form[key] = '';
        }
      });
      additionalImagesInput.value = '';
    }
  }
});
</script>