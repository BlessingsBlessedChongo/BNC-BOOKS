<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader />
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
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import NotificationContainer from '@/components/common/NotificationContainer.vue'

const route = useRoute()
const authStore = useAuthStore()

const showSidebar = computed(() => {
  return authStore.isAuthenticated && !route.meta.hideNavigation
})
</script>