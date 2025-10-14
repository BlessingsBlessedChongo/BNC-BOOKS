<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Simple header for now -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-2">
            <BookOpenIcon class="h-8 w-8 text-teal-600" />
            <span class="text-xl font-bold text-gray-900">BNC Books</span>
          </div>
          <nav class="flex items-center space-x-4">
            <router-link to="/" class="text-gray-700 hover:text-teal-600">Home</router-link>
            <router-link to="/books" class="text-gray-700 hover:text-teal-600">Books</router-link>
            <router-link to="/login" class="text-gray-700 hover:text-teal-600">Login</router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1">
      <router-view />
    </main>

    <!-- Simple footer -->
    <footer class="bg-white border-t border-gray-200 mt-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <p class="text-center text-gray-600">
          &copy; 2024 BNC Books. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { BookOpenIcon } from '@heroicons/vue/24/outline'
</script>

<style>
/* Basic styles */
#app {
  font-family: 'Inter', sans-serif;
}

.router-link-active {
  @apply text-teal-600 font-medium;
}
</style>