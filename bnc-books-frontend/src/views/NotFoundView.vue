<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center items-center px-4">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-gray-900">404</h1>
      <p class="text-xl text-gray-600 mt-4">Page not found</p>
      <p class="text-gray-500 mt-2">Sorry, we couldn't find the page you're looking for.</p>
      <div class="mt-6 space-x-4">
        <router-link to="/" class="btn-primary">
          Go Home
        </router-link>
        <button @click="$router.back()" class="btn-secondary">
          Go Back
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 404 page logic
</script>