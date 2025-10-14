<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Integrated Header with NotificationCenter -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <!-- Your existing navigation (e.g., logo or links from AppHeader) -->
          <!-- If AppHeader contains nav elements, you can nest or move them here -->
          
          <div class="flex items-center space-x-4">
            <!-- Notification Center -->
            <NotificationCenter />
            
            <!-- User menu and other items (add your existing user-related components here) -->
          </div>
        </div>
      </div>
    </header>
    
    <div class="flex flex-1">
      <AppSidebar v-if="showSidebar" />
      <main class="flex-1 overflow-auto">
        <NotificationContainer />
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import NotificationContainer from '@/components/common/NotificationContainer.vue'
import NotificationCenter from '@/components/notifications/NotificationCenter.vue'

const route = useRoute()
const authStore = useAuthStore()

const showSidebar = computed(() => {
  return authStore.isAuthenticated && !route.meta.hideNavigation
})
</script>