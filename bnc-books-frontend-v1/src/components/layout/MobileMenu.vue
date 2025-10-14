<template>
  <div class="fixed inset-0 z-50 md:hidden">
    <!-- Background overlay -->
    <div 
      class="fixed inset-0 bg-gray-600 bg-opacity-75 transition-opacity"
      @click="$emit('close')"
    ></div>

    <!-- Mobile menu panel -->
    <div class="fixed inset-y-0 right-0 w-full max-w-sm bg-white shadow-xl">
      <div class="flex flex-col h-full">
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b border-gray-200">
          <div class="flex items-center space-x-2">
            <BookOpenIcon class="h-8 w-8 text-teal-600" />
            <span class="text-xl font-bold text-gray-900">BNC Books</span>
          </div>
          <button
            @click="$emit('close')"
            class="p-2 text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>

        <!-- Navigation -->
        <div class="flex-1 px-4 py-6 space-y-2">
          <!-- User info -->
          <div v-if="isAuthenticated" class="pb-4 border-b border-gray-200">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-teal-100 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-teal-600">
                  {{ userInitials }}
                </span>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">
                  {{ user?.first_name }} {{ user?.last_name }}
                </p>
                <p class="text-xs text-gray-600">{{ user?.email }}</p>
              </div>
            </div>
          </div>

          <!-- Main navigation -->
          <nav class="space-y-1">
            <router-link
              to="/books"
              class="flex items-center px-3 py-2 text-base font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-teal-600"
              active-class="bg-teal-50 text-teal-600"
              @click="$emit('close')"
            >
              <BookOpenIcon class="h-5 w-5 mr-3" />
              Browse Books
            </router-link>

            <router-link
              v-if="isAuthenticated"
              to="/orders"
              class="flex items-center px-3 py-2 text-base font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-teal-600"
              active-class="bg-teal-50 text-teal-600"
              @click="$emit('close')"
            >
              <ShoppingBagIcon class="h-5 w-5 mr-3" />
              My Orders
            </router-link>

            <router-link
              v-if="isAuthenticated"
              to="/wishlist"
              class="flex items-center px-3 py-2 text-base font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-teal-600"
              active-class="bg-teal-50 text-teal-600"
              @click="$emit('close')"
            >
              <HeartIcon class="h-5 w-5 mr-3" />
              Wishlist
            </router-link>

            <router-link
              v-if="isAuthenticated && user?.role === 'seller'"
              to="/seller"
              class="flex items-center px-3 py-2 text-base font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-teal-600"
              active-class="bg-teal-50 text-teal-600"
              @click="$emit('close')"
            >
              <ChartBarSquareIcon class="h-5 w-5 mr-3" />
              Seller Dashboard
            </router-link>

            <router-link
              v-if="isAuthenticated && user?.role === 'affiliate'"
              to="/affiliate"
              class="flex items-center px-3 py-2 text-base font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-teal-600"
              active-class="bg-teal-50 text-teal-600"
              @click="$emit('close')"
            >
              <CurrencyDollarIcon class="h-5 w-5 mr-3" />
              Affiliate Dashboard
            </router-link>

            <router-link
              to="/help"
              class="flex items-center px-3 py-2 text-base font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-teal-600"
              active-class="bg-teal-50 text-teal-600"
              @click="$emit('close')"
            >
              <QuestionMarkCircleIcon class="h-5 w-5 mr-3" />
              Help Center
            </router-link>
          </nav>

          <!-- Divider -->
          <div class="border-t border-gray-200 my-4"></div>

          <!-- Account links -->
          <div v-if="isAuthenticated" class="space-y-1">
            <router-link
              to="/profile"
              class="flex items-center px-3 py-2 text-base font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-teal-600"
              active-class="bg-teal-50 text-teal-600"
              @click="$emit('close')"
            >
              <UserIcon class="h-5 w-5 mr-3" />
              Profile
            </router-link>

            <router-link
              to="/settings"
              class="flex items-center px-3 py-2 text-base font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-teal-600"
              active-class="bg-teal-50 text-teal-600"
              @click="$emit('close')"
            >
              <Cog6ToothIcon class="h-5 w-5 mr-3" />
              Settings
            </router-link>

            <button
              @click="handleLogout"
              class="flex items-center w-full px-3 py-2 text-base font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-red-600"
            >
              <ArrowRightOnRectangleIcon class="h-5 w-5 mr-3" />
              Sign Out
            </button>
          </div>

          <!-- Auth links -->
          <div v-else class="space-y-2">
            <router-link
              to="/login"
              class="flex w-full justify-center px-4 py-2 text-base font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              @click="$emit('close')"
            >
              Sign In
            </router-link>
            <router-link
              to="/register"
              class="flex w-full justify-center px-4 py-2 text-base font-medium text-white bg-teal-600 rounded-lg hover:bg-teal-700"
              @click="$emit('close')"
            >
              Sign Up
            </router-link>
          </div>
        </div>

        <!-- Footer -->
        <div class="border-t border-gray-200 p-4">
          <div class="flex justify-center space-x-6">
            <a href="#" class="text-gray-400 hover:text-teal-600">
              <span class="sr-only">Facebook</span>
              <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd" />
              </svg>
            </a>
            <a href="#" class="text-gray-400 hover:text-teal-600">
              <span class="sr-only">Twitter</span>
              <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
              </svg>
            </a>
            <a href="#" class="text-gray-400 hover:text-teal-600">
              <span class="sr-only">Instagram</span>
              <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clip-rule="evenodd" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  BookOpenIcon,
  XMarkIcon,
  ShoppingBagIcon,
  HeartIcon,
  ChartBarSquareIcon,
  CurrencyDollarIcon,
  QuestionMarkCircleIcon,
  UserIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const emit = defineEmits(['close'])

// Computed
const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)

const userInitials = computed(() => {
  if (!user.value) return '?'
  const first = user.value.first_name?.[0] || ''
  const last = user.value.last_name?.[0] || ''
  return (first + last).toUpperCase() || 'U'
})

// Methods
const handleLogout = async () => {
  try {
    await authStore.logout()
    emit('close')
    router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>