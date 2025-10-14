<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Success Confirmation -->
      <div class="text-center mb-8">
        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-100">
          <svg class="h-10 w-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h1 class="mt-4 text-3xl font-bold text-gray-900">Order Confirmed!</h1>
        <p class="mt-2 text-lg text-gray-600">Thank you for your purchase. Your order has been successfully placed.</p>
        <p class="mt-1 text-sm text-gray-500">Order #{{ order?.order_number || 'Loading...' }}</p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading order details...</p>
      </div>

      <!-- Order Details -->
      <div v-else-if="order" class="space-y-8">
        <!-- Order Summary -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Order Summary</h2>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div 
                v-for="item in order.items" 
                :key="item.id"
                class="flex items-center justify-between"
              >
                <div class="flex items-center space-x-4">
                  <img
                    :src="item.book.cover_image"
                    :alt="item.book.title"
                    class="w-16 h-20 object-cover rounded"
                    @error="handleImageError"
                  />
                  <div>
                    <h3 class="font-medium text-gray-900">{{ item.book.title }}</h3>
                    <p class="text-sm text-gray-600">by {{ item.book.author }}</p>
                    <p class="text-sm text-gray-600">Qty: {{ item.quantity }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="font-medium text-gray-900">${{ item.total_price }}</p>
                  <p class="text-sm text-gray-600">${{ item.unit_price }} each</p>
                </div>
              </div>
            </div>

            <!-- Order Totals -->
            <div class="mt-6 border-t border-gray-200 pt-6">
              <dl class="space-y-3">
                <div class="flex justify-between">
                  <dt class="text-gray-600">Subtotal</dt>
                  <dd class="font-medium text-gray-900">${{ order.subtotal }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">Shipping</dt>
                  <dd class="font-medium text-gray-900">${{ order.shipping_cost }}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-gray-600">Tax</dt>
                  <dd class="font-medium text-gray-900">${{ order.tax_amount }}</dd>
                </div>
                <div class="flex justify-between border-t border-gray-200 pt-3">
                  <dt class="text-lg font-medium text-gray-900">Total</dt>
                  <dd class="text-lg font-bold text-gray-900">${{ order.total_amount }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>

        <!-- Shipping Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="card">
            <div class="px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-medium text-gray-900">Shipping Address</h2>
            </div>
            <div class="p-6">
              <div class="space-y-2 text-sm">
                <p class="font-medium text-gray-900">{{ order.shipping_address.first_name }} {{ order.shipping_address.last_name }}</p>
                <p class="text-gray-600">{{ order.shipping_address.street_address }}</p>
                <p v-if="order.shipping_address.apartment" class="text-gray-600">{{ order.shipping_address.apartment }}</p>
                <p class="text-gray-600">{{ order.shipping_address.city }}, {{ order.shipping_address.state }} {{ order.shipping_address.zip_code }}</p>
                <p class="text-gray-600">{{ order.shipping_address.country }}</p>
                <p class="text-gray-600">{{ order.shipping_address.phone }}</p>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-medium text-gray-900">Shipping Method</h2>
            </div>
            <div class="p-6">
              <div class="space-y-2">
                <p class="font-medium text-gray-900">{{ order.shipping_method.name }}</p>
                <p class="text-sm text-gray-600">{{ order.shipping_method.delivery_days }}</p>
                <p class="text-sm text-gray-600">${{ order.shipping_method.price }}</p>
                <p v-if="order.tracking_number" class="text-sm text-blue-600 font-medium">
                  Tracking: {{ order.tracking_number }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Next Steps -->
        <div class="card">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">What's Next?</h2>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-gray-900">Order Confirmation Email</p>
                  <p class="text-sm text-gray-600">We've sent a confirmation email with your order details.</p>
                </div>
              </div>

              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-gray-900">Order Processing</p>
                  <p class="text-sm text-gray-600">Your order is being processed and will be shipped soon.</p>
                </div>
              </div>

              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                    </svg>
                  </div>
                </div>
                <div>
                  <p class="font-medium text-gray-900">Track Your Order</p>
                  <p class="text-sm text-gray-600">You can track your order status from your orders page.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/orders" class="btn-primary text-center">
            View Order Details
          </router-link>
          <router-link to="/books" class="btn-secondary text-center">
            Continue Shopping
          </router-link>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="text-center py-12">
        <svg class="mx-auto h-24 w-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 20c-2.22 0-4.251-.804-5.816-2.134M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <h2 class="mt-4 text-2xl font-bold text-gray-900">Unable to load order details</h2>
        <p class="mt-2 text-gray-600">There was a problem loading your order confirmation.</p>
        <div class="mt-6 space-x-4">
          <router-link to="/orders" class="btn-primary">
            View Your Orders
          </router-link>
          <router-link to="/books" class="btn-secondary">
            Browse Books
          </router-link>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AppLayout from '../../layouts/AppLayout.vue';
import { useOrdersStore } from '../../stores/orders';

const route = useRoute();
const ordersStore = useOrdersStore();

const order = ref(null);
const isLoading = ref(true);

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/100x150?text=No+Image';
};

// In a real application, you would fetch the order details
// For now, we'll simulate loading and use mock data
onMounted(async () => {
  try {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Mock order data - in real app, fetch from API using order ID from route
    order.value = {
      id: 1001,
      order_number: 'BNC-2024-1001',
      status: 'pending',
      subtotal: 25.98,
      shipping_cost: 4.99,
      tax_amount: 2.60,
      total_amount: 33.57,
      items: [
        {
          id: 1,
          book: {
            id: 1,
            title: "Harry Potter and the Philosopher's Stone",
            author: "J.K. Rowling",
            cover_image: "http://localhost:8000/media/book_covers/harry_potter.jpg",
            price: 12.99
          },
          quantity: 2,
          unit_price: 12.99,
          total_price: 25.98
        }
      ],
      shipping_address: {
        first_name: "John",
        last_name: "Doe",
        street_address: "123 Main St",
        apartment: "Apt 4B",
        city: "New York",
        state: "NY",
        zip_code: "10001",
        country: "US",
        phone: "+1-555-0123"
      },
      shipping_method: {
        id: 1,
        name: "Standard Shipping",
        price: 4.99,
        delivery_days: "5-7 business days"
      },
      tracking_number: null,
      created_at: "2024-01-15T10:30:00Z"
    };
  } catch (error) {
    console.error('Failed to load order details:', error);
  } finally {
    isLoading.value = false;
  }
});
</script>