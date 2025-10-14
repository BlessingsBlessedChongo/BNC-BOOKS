<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo and primary navigation -->
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <h1 class="text-2xl font-bold text-primary-600">BNC Books</h1>
            </router-link>
            <nav class="hidden md:ml-8 md:flex md:space-x-8">
              <router-link 
                to="/books" 
                class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="{ 'text-primary-600 border-b-2 border-primary-600': $route.path.includes('/books') }"
              >
                Browse Books
              </router-link>
              <router-link 
                v-if="authStore.userRole === 'seller'"
                to="/seller" 
                class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="{ 'text-primary-600 border-b-2 border-primary-600': $route.path.includes('/seller') }"
              >
                Seller Dashboard
              </router-link>
              <router-link 
                v-if="authStore.userRole === 'affiliate'"
                to="/affiliate" 
                class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="{ 'text-primary-600 border-b-2 border-primary-600': $route.path.includes('/affiliate') }"
              >
                Affiliate Dashboard
              </router-link>
            </nav>
          </div>

          <!-- Secondary navigation -->
          <div class="flex items-center space-x-4">
            <!-- Cart Icon -->
            <button 
              @click="openCart"
              class="relative p-2 text-gray-700 hover:text-primary-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span 
                v-if="cartStore.totalItems > 0"
                class="absolute -top-1 -right-1 bg-primary-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
              >
                {{ cartStore.totalItems }}
              </span>
            </button>

            <!-- User menu -->
            <div class="relative" ref="userMenuRef">
              <button 
                @click="toggleUserMenu"
                class="flex items-center space-x-2 text-sm font-medium text-gray-700 hover:text-primary-600 focus:outline-none transition-colors"
              >
                <div class="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center text-white font-semibold">
                  {{ authStore.user?.first_name?.charAt(0) }}{{ authStore.user?.last_name?.charAt(0) }}
                </div>
                <span class="hidden md:block">{{ authStore.user?.first_name }} {{ authStore.user?.last_name }}</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- User dropdown menu -->
              <div 
                v-if="isUserMenuOpen"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50"
              >
                <router-link 
                  to="/profile"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  @click="closeUserMenu"
                >
                  Your Profile
                </router-link>
                <router-link 
                  to="/orders"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  @click="closeUserMenu"
                >
                  Your Orders
                </router-link>
                <router-link 
                  to="/reviews"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  @click="closeUserMenu"
                >
                  Your Reviews
                </router-link>
                <div class="border-t border-gray-200 my-1"></div>
                <button 
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 transition-colors"
                >
                  Sign out
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile menu -->
    <div v-if="isMobileMenuOpen" class="md:hidden bg-white border-b border-gray-200">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link 
          to="/books"
          class="block px-3 py-2 text-gray-700 hover:text-primary-600 rounded-md text-base font-medium"
          @click="closeMobileMenu"
        >
          Browse Books
        </router-link>
        <router-link 
          v-if="authStore.userRole === 'seller'"
          to="/seller"
          class="block px-3 py-2 text-gray-700 hover:text-primary-600 rounded-md text-base font-medium"
          @click="closeMobileMenu"
        >
          Seller Dashboard
        </router-link>
        <router-link 
          v-if="authStore.userRole === 'affiliate'"
          to="/affiliate"
          class="block px-3 py-2 text-gray-700 hover:text-primary-600 rounded-md text-base font-medium"
          @click="closeMobileMenu"
        >
          Affiliate Dashboard
        </router-link>
      </div>
    </div>

    <!-- Main content -->
    <main>
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-12">
      <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div class="col-span-1">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">BNC Books</h3>
            <p class="text-gray-600 text-sm">
              Your premier destination for discovering and purchasing books from sellers worldwide.
            </p>
          </div>
          <div>
            <h4 class="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">Account</h4>
            <ul class="space-y-2">
              <li><router-link to="/profile" class="text-gray-600 hover:text-primary-600 text-sm">Profile</router-link></li>
              <li><router-link to="/orders" class="text-gray-600 hover:text-primary-600 text-sm">Orders</router-link></li>
              <li><router-link to="/reviews" class="text-gray-600 hover:text-primary-600 text-sm">Reviews</router-link></li>
            </ul>
          </div>
          <div>
            <h4 class="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">Support</h4>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-600 hover:text-primary-600 text-sm">Help Center</a></li>
              <li><a href="#" class="text-gray-600 hover:text-primary-600 text-sm">Contact Us</a></li>
              <li><a href="#" class="text-gray-600 hover:text-primary-600 text-sm">Shipping Info</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">Legal</h4>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-600 hover:text-primary-600 text-sm">Privacy Policy</a></li>
              <li><a href="#" class="text-gray-600 hover:text-primary-600 text-sm">Terms of Service</a></li>
              <li><a href="#" class="text-gray-600 hover:text-primary-600 text-sm">Return Policy</a></li>
            </ul>
          </div>
        </div>
        <div class="mt-8 pt-8 border-t border-gray-200 text-center">
          <p class="text-gray-500 text-sm">&copy; 2024 BNC Books. All rights reserved.</p>
        </div>
      </div>
    </footer>

    <!-- Cart Sidebar -->
    <CartSidebar 
      :isOpen="isCartOpen" 
      @close="isCartOpen = false" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useCartStore } from '../stores/cart';
import { useRouter } from 'vue-router';
import CartSidebar from '../components/cart/CartSidebar.vue';

const authStore = useAuthStore();
const cartStore = useCartStore();
const router = useRouter();

const isUserMenuOpen = ref(false);
const isMobileMenuOpen = ref(false);
const userMenuRef = ref(null);
const isCartOpen = ref(false);

const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value;
};

const closeUserMenu = () => {
  isUserMenuOpen.value = false;
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const handleLogout = () => {
  authStore.logout();
  closeUserMenu();
  router.push('/');
};

const openCart = () => {
  isCartOpen.value = true;
};

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    closeUserMenu();
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

// Expose the openCart method if needed
defineExpose({
  openCart
});
</script>