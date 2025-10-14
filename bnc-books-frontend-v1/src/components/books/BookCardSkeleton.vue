<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden animate-pulse">
    <!-- Image Skeleton -->
    <div class="bg-gray-200 h-48 w-full"></div>
    
    <!-- Content Skeleton -->
    <div class="p-4 space-y-3">
      <!-- Title -->
      <div class="h-4 bg-gray-200 rounded w-3/4"></div>
      
      <!-- Author -->
      <div class="h-3 bg-gray-200 rounded w-1/2"></div>
      
      <!-- Rating -->
      <div class="flex items-center space-x-1">
        <div class="h-4 w-16 bg-gray-200 rounded"></div>
      </div>
      
      <!-- Price -->
      <div class="h-5 bg-gray-200 rounded w-1/4"></div>
      
      <!-- Buttons -->
      <div class="flex space-x-2 pt-2">
        <div class="h-9 bg-gray-200 rounded flex-1"></div>
        <div class="h-9 w-9 bg-gray-200 rounded"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Skeleton component for loading states
</script>