<template>
  <aside
    class="bg-white border-r border-gray-200 w-64 flex-shrink-0 hidden lg:block lg:static fixed inset-y-0 left-0 z-40 transform transition-transform duration-300 ease-in-out"
    :class="{
      'translate-x-0': isOpen,
      '-translate-x-full': !isOpen
    }"
  >
    <div class="h-full flex flex-col">
      <!-- Sidebar header -->
      <div class="flex items-center justify-between h-16 px-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">Navigation</h2>
        <button
          @click="closeSidebar"
          class="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <!-- Common Navigation -->
        <router-link
          to="/dashboard"
          class="nav-item"
          :class="{ 'nav-item-active': $route.path === '/dashboard' }"
        >
          <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
          </svg>
          <span class="nav-text">Dashboard</span>
        </router-link>

        <router-link
          to="/books"
          class="nav-item"
          :class="{ 'nav-item-active': $route.path.startsWith('/books') }"
        >
          <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
          </svg>
          <span class="nav-text">Browse Books</span>
        </router-link>

        <!-- Seller Navigation -->
        <div v-if="authStore.userRole === 'seller'">
          <p class="nav-section-label">Seller Tools</p>
          
          <router-link
            to="/seller/books"
            class="nav-item"
            :class="{ 'nav-item-active': $route.path.startsWith('/seller/books') }"
          >
            <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
            </svg>
            <span class="nav-text">My Listings</span>
          </router-link>

          <router-link
            to="/seller/analytics"
            class="nav-item"
            :class="{ 'nav-item-active': $route.path.startsWith('/seller/analytics') }"
          >
            <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            <span class="nav-text">Analytics</span>
          </router-link>
        </div>

        <!-- Affiliate Navigation -->
        <div v-if="authStore.userRole === 'affiliate'">
          <p class="nav-section-label">Affiliate</p>
          
          <router-link
            to="/affiliate/dashboard"
            class="nav-item"
            :class="{ 'nav-item-active': $route.path.startsWith('/affiliate') }"
          >
            <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
            <span class="nav-text">Affiliate Dashboard</span>
          </router-link>
        </div>

        <!-- Buyer Navigation -->
        <div v-if="authStore.userRole === 'buyer'">
          <p class="nav-section-label">Shopping</p>
          
          <router-link
            to="/cart"
            class="nav-item"
            :class="{ 'nav-item-active': $route.path.startsWith('/cart') }"
          >
            <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <span class="nav-text">Shopping Cart</span>
          </router-link>

          <router-link
            to="/orders"
            class="nav-item"
            :class="{ 'nav-item-active': $route.path.startsWith('/orders') }"
          >
            <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
            </svg>
            <span class="nav-text">My Orders</span>
          </router-link>
        </div>

        <!-- Common Bottom Navigation -->
        <div class="pt-4 border-t border-gray-200">
          <router-link
            to="/profile"
            class="nav-item"
            :class="{ 'nav-item-active': $route.path.startsWith('/profile') }"
          >
            <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            <span class="nav-text">Profile</span>
          </router-link>

          <router-link
            to="/settings"
            class="nav-item"
            :class="{ 'nav-item-active': $route.path.startsWith('/settings') }"
          >
            <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
            <span class="nav-text">Settings</span>
          </router-link>
        </div>
      </nav>
    </div>
  </aside>

  <!-- Mobile overlay -->
  <div
    v-if="isOpen"
    @click="closeSidebar"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 z-30 lg:hidden"
  ></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isOpen = ref(false)

const closeSidebar = () => {
  isOpen.value = false
}

const handleToggleSidebar = (event) => {
  isOpen.value = event.detail
}

onMounted(() => {
  window.addEventListener('toggle-sidebar', handleToggleSidebar)
})

onUnmounted(() => {
  window.removeEventListener('toggle-sidebar', handleToggleSidebar)
})
</script>

<style scoped>
.nav-item {
  @apply flex items-center px-3 py-2 text-sm font-medium rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors duration-200;
}

.nav-item-active {
  @apply bg-primary-50 text-primary-700 hover:bg-primary-100 hover:text-primary-800;
}

.nav-icon {
  @apply h-5 w-5 mr-3;
}

.nav-text {
  @apply flex-1;
}

.nav-section-label {
  @apply px-3 pt-4 text-xs font-semibold text-gray-500 uppercase tracking-wider;
}
</style>