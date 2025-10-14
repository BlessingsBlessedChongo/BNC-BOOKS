<template>
  <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <BookOpenIcon class="h-8 w-8 text-teal-600" />
            <span class="text-xl font-bold text-gray-900">BNC Books</span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center space-x-8">
          <router-link
            to="/books"
            class="text-gray-700 hover:text-teal-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            active-class="text-teal-600 bg-teal-50"
          >
            Browse Books
          </router-link>
          
          <router-link
            v-if="isAuthenticated && user?.role === 'seller'"
            to="/seller"
            class="text-gray-700 hover:text-teal-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            active-class="text-teal-600 bg-teal-50"
          >
            Seller Dashboard
          </router-link>
          
          <router-link
            v-if="isAuthenticated && user?.role === 'affiliate'"
            to="/affiliate"
            class="text-gray-700 hover:text-teal-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            active-class="text-teal-600 bg-teal-50"
          >
            Affiliate Dashboard
          </router-link>
        </nav>

        <!-- Right side actions -->
        <div class="flex items-center space-x-4">
          <!-- Search Button (Mobile) -->
          <button
            @click="showSearch = true"
            class="md:hidden p-2 text-gray-400 hover:text-gray-600"
          >
            <MagnifyingGlassIcon class="h-5 w-5" />
          </button>

          <!-- Search Button (Desktop) -->
          <button
            @click="showSearch = true"
            class="hidden md:flex items-center space-x-2 px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50"
          >
            <MagnifyingGlassIcon class="h-4 w-4" />
            <span>Search books...</span>
            <kbd class="text-xs bg-gray-100 px-1 py-0.5 rounded border">Ctrl K</kbd>
          </button>

          <!-- Notification Center -->
          <NotificationCenter />

          <!-- Wishlist -->
          <button
            v-if="isAuthenticated"
            @click="navigateToWishlist"
            class="relative p-2 text-gray-400 hover:text-gray-600"
          >
            <HeartIcon class="h-5 w-5" />
            <span
              v-if="wishlistCount > 0"
              class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
            >
              {{ wishlistCount > 99 ? '99+' : wishlistCount }}
            </span>
          </button>

          <!-- Shopping Cart -->
          <button
            @click="navigateToCart"
            class="relative p-2 text-gray-400 hover:text-gray-600"
          >
            <ShoppingCartIcon class="h-5 w-5" />
            <span
              v-if="cartCount > 0"
              class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
            >
              {{ cartCount > 99 ? '99+' : cartCount }}
            </span>
          </button>

          <!-- User Menu -->
          <div class="relative" v-if="isAuthenticated">
            <button
              @click="showUserMenu = !showUserMenu"
              class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <div class="w-8 h-8 bg-teal-100 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-teal-600">
                  {{ userInitials }}
                </span>
              </div>
              <span class="hidden sm:block text-sm font-medium text-gray-700">
                {{ user?.first_name }}
              </span>
              <ChevronDownIcon class="h-4 w-4 text-gray-400" />
            </button>

            <!-- User Dropdown Menu -->
            <div
              v-if="showUserMenu"
              class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50"
            >
              <div class="px-4 py-2 border-b border-gray-200">
                <p class="text-sm font-medium text-gray-900">{{ user?.first_name }} {{ user?.last_name }}</p>
                <p class="text-xs text-gray-600">{{ user?.email }}</p>
              </div>
              
              <router-link
                to="/profile"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                @click="showUserMenu = false"
              >
                Profile
              </router-link>
              
              <router-link
                to="/orders"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                @click="showUserMenu = false"
              >
                My Orders
              </router-link>
              
              <router-link
                to="/wishlist"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                @click="showUserMenu = false"
              >
                Wishlist
              </router-link>

              <div class="border-t border-gray-200 my-1"></div>

              <button
                @click="logout"
                class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              >
                Sign out
              </button>
            </div>
          </div>

          <!-- Auth Buttons -->
          <div v-else class="flex items-center space-x-2">
            <router-link
              to="/login"
              class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
            >
              Sign in
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-lg hover:bg-teal-700"
            >
              Sign up
            </router-link>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="showMobileMenu = true"
            class="md:hidden p-2 text-gray-400 hover:text-gray-600"
          >
            <Bars3Icon class="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Search Modal -->
    <SearchModal
      v-if="showSearch"
      @close="showSearch = false"
    />

    <!-- Mobile Menu -->
    <MobileMenu
      v-if="showMobileMenu"
      @close="showMobileMenu = false"
    />
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import {
  BookOpenIcon,
  MagnifyingGlassIcon,
  HeartIcon,
  ShoppingCartIcon,
  ChevronDownIcon,
  Bars3Icon
} from '@heroicons/vue/24/outline'

import NotificationCenter from '@/components/notifications/NotificationCenter.vue'
import SearchModal from '@/components/search/SearchModal.vue'
import MobileMenu from '@/components/layout/MobileMenu.vue'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()

// State
const showUserMenu = ref(false)
const showSearch = ref(false)
const showMobileMenu = ref(false)

// Computed
const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)
const cartCount = computed(() => cartStore.cartCount)
const wishlistCount = computed(() => wishlistStore.wishlistCount)

const userInitials = computed(() => {
  if (!user.value) return '?'
  const first = user.value.first_name?.[0] || ''
  const last = user.value.last_name?.[0] || ''
  return (first + last).toUpperCase() || 'U'
})

// Methods
const navigateToCart = () => {
  if (isAuthenticated.value) {
    router.push('/cart')
  } else {
    router.push('/login')
  }
}

const navigateToWishlist = () => {
  if (isAuthenticated.value) {
    router.push('/wishlist')
  } else {
    router.push('/login')
  }
}

const logout = async () => {
  showUserMenu.value = false
  try {
    await authStore.logout()
    router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showUserMenu.value = false
  }
}

// Keyboard shortcuts
const handleKeydown = (event) => {
  // Ctrl/Cmd + K for search
  if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
    event.preventDefault()
    showSearch.value = true
  }

  // Escape key to close menus
  if (event.key === 'Escape') {
    showUserMenu.value = false
    showSearch.value = false
    showMobileMenu.value = false
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.router-link-active {
  @apply text-teal-600 bg-teal-50;
}
</style>