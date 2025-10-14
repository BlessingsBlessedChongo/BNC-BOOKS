<template>
  <div class="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50">
    <!-- Hero Section -->
    <section class="relative py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Discover Your Next
          <span class="text-teal-600">Favorite Book</span>
        </h1>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Explore millions of books across all genres. From bestsellers to hidden gems, 
          find your perfect read at BNC Books.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link
            to="/books"
            class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
          >
            Browse Books
          </router-link>
          <router-link
            to="/register"
            class="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
          >
            Create Account
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900">Why Choose BNC Books?</h2>
          <p class="mt-4 text-lg text-gray-600">The best reading experience starts here</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="mx-auto h-12 w-12 bg-teal-100 rounded-lg flex items-center justify-center mb-4">
              <TruckIcon class="h-6 w-6 text-teal-600" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Free Shipping</h3>
            <p class="text-gray-600">Free delivery on orders over $25</p>
          </div>
          
          <div class="text-center">
            <div class="mx-auto h-12 w-12 bg-teal-100 rounded-lg flex items-center justify-center mb-4">
              <ShieldCheckIcon class="h-6 w-6 text-teal-600" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Secure Payment</h3>
            <p class="text-gray-600">Your payment information is safe with us</p>
          </div>
          
          <div class="text-center">
            <div class="mx-auto h-12 w-12 bg-teal-100 rounded-lg flex items-center justify-center mb-4">
              <ArrowPathIcon class="h-6 w-6 text-teal-600" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Easy Returns</h3>
            <p class="text-gray-600">30-day return policy on all books</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Categories Section -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900">Popular Categories</h2>
          <p class="mt-4 text-lg text-gray-600">Explore books by category</p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <router-link
            v-for="category in categories"
            :key="category.name"
            :to="`/books?category=${category.name}`"
            class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center hover:shadow-md transition-shadow"
          >
            <component :is="category.icon" class="mx-auto h-8 w-8 text-teal-600 mb-3" />
            <h3 class="font-medium text-gray-900">{{ category.name }}</h3>
            <p class="text-sm text-gray-600 mt-1">{{ category.count }} books</p>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import {
  TruckIcon,
  ShieldCheckIcon,
  ArrowPathIcon,
  BookOpenIcon,
  AcademicCapIcon,
  ChartBarSquareIcon,
  HeartIcon
} from '@heroicons/vue/24/outline'

const categories = [
  { name: 'Fiction', count: '10,000+', icon: BookOpenIcon },
  { name: 'Science', count: '5,000+', icon: AcademicCapIcon },
  { name: 'Business', count: '3,000+', icon: ChartBarSquareIcon },
  { name: 'Romance', count: '2,500+', icon: HeartIcon }
]
</script>