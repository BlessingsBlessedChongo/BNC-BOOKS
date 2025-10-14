<template>
  <div class="card group hover:shadow-lg transition-all duration-300 h-full flex flex-col">
    <!-- Book Cover -->
    <div class="relative overflow-hidden bg-gray-200">
      <img
        :src="book.cover_image"
        :alt="book.title"
        class="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
        @error="handleImageError"
      />
      
      <!-- Sale Badge -->
      <div v-if="hasDiscount" class="absolute top-2 left-2">
        <span class="bg-red-500 text-white px-2 py-1 text-xs font-bold rounded">
          {{ discountPercentage }}% OFF
        </span>
      </div>
      
      <!-- Stock Status -->
      <div class="absolute top-2 right-2">
        <span 
          :class="book.stock_quantity > 0 ? 'bg-green-500' : 'bg-red-500'"
          class="text-white px-2 py-1 text-xs font-bold rounded"
        >
          {{ book.stock_quantity > 0 ? 'In Stock' : 'Out of Stock' }}
        </span>
      </div>

      <!-- Quick Actions Overlay -->
      <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
        <div class="flex space-x-2">
          <button 
            @click="viewDetails"
            class="bg-white text-gray-900 p-2 rounded-full hover:bg-gray-100 transition-colors"
            title="View Details"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
          <button 
            v-if="book.stock_quantity > 0"
            @click="addToCart"
            class="bg-primary-500 text-white p-2 rounded-full hover:bg-primary-600 transition-colors"
            title="Add to Cart"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Book Info -->
    <div class="p-4 flex-1 flex flex-col">
      <!-- Title -->
      <h3 class="font-semibold text-lg text-gray-900 mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
        {{ book.title }}
      </h3>
      
      <!-- Author -->
      <p class="text-gray-600 text-sm mb-3">by {{ book.author }}</p>
      
      <!-- Rating -->
      <div class="flex items-center mb-3">
        <div class="flex items-center">
          <div v-for="n in 5" :key="n" class="mr-1">
            <svg 
              class="h-4 w-4" 
              :class="n <= Math.floor(book.average_rating) ? 'text-yellow-400' : 'text-gray-300'"
              fill="currentColor" 
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
        </div>
        <span class="ml-2 text-sm text-gray-600">
          {{ book.average_rating?.toFixed(1) || '0.0' }} ({{ book.review_count || 0 }})
        </span>
      </div>

      <!-- Genres -->
      <div class="mb-4">
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="genre in book.genres?.slice(0, 2)" 
            :key="genre"
            class="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
          >
            {{ genre }}
          </span>
          <span 
            v-if="book.genres && book.genres.length > 2"
            class="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
          >
            +{{ book.genres.length - 2 }}
          </span>
        </div>
      </div>

      <!-- Price and Action -->
      <div class="mt-auto flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <!-- Current Price -->
          <span class="text-xl font-bold text-gray-900">
            ${{ book.price }}
          </span>
          
          <!-- Original Price (if on sale) -->
          <span v-if="hasDiscount" class="text-sm text-gray-500 line-through">
            ${{ book.original_price }}
          </span>
        </div>
        
        <!-- Seller Info -->
        <div class="text-right">
          <p class="text-xs text-gray-500">Sold by</p>
          <p class="text-xs font-medium text-gray-700 truncate max-w-20">
            {{ book.seller?.store_name || 'Unknown' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useCartStore } from '../../stores/cart';

const props = defineProps({
  book: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const cartStore = useCartStore();

const hasDiscount = computed(() => {
  return props.book.original_price && props.book.original_price > props.book.price;
});

const discountPercentage = computed(() => {
  if (!hasDiscount.value) return 0;
  return Math.round((1 - props.book.price / props.book.original_price) * 100);
});

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/300x400?text=No+Image';
};

const viewDetails = () => {
  router.push(`/books/${props.book.id}`);
};

const addToCart = () => {
  if (props.book.stock_quantity > 0) {
    cartStore.addToCart(props.book, 1);
    // You can add a toast notification here later
    console.log('Added to cart:', props.book.title);
  }
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>