<template>
  <AppLayout>
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Welcome Section -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">
          Welcome back, {{ authStore.user?.first_name }}!
        </h1>
        <p class="mt-2 text-lg text-gray-600">
          Here's what's happening with your {{ getRoleDescription(authStore.userRole) }} account today.
        </p>
      </div>

      <!-- Role-Based Dashboard -->
      <div v-if="authStore.userRole === 'buyer'" class="space-y-8">
        <!-- Buyer Dashboard -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Orders</p>
                <p class="text-2xl font-semibold text-gray-900">12</p>
              </div>
            </div>
          </div>
          
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Reviews Written</p>
                <p class="text-2xl font-semibold text-gray-900">8</p>
              </div>
            </div>
          </div>
          
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Wishlist Items</p>
                <p class="text-2xl font-semibold text-gray-900">5</p>
              </div>
            </div>
          </div>
          
          <div class="card p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Pending Orders</p>
                <p class="text-2xl font-semibold text-gray-900">2</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions for Buyer -->
        <div class="card p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <router-link to="/books" class="card p-4 text-center hover:bg-gray-50 transition-colors">
              <svg class="h-8 w-8 text-primary-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <p class="text-sm font-medium text-gray-900">Browse Books</p>
            </router-link>
            
            <router-link to="/orders" class="card p-4 text-center hover:bg-gray-50 transition-colors">
              <svg class="h-8 w-8 text-green-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              <p class="text-sm font-medium text-gray-900">View Orders</p>
            </router-link>
            
            <router-link to="/reviews" class="card p-4 text-center hover:bg-gray-50 transition-colors">
              <svg class="h-8 w-8 text-yellow-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
              <p class="text-sm font-medium text-gray-900">My Reviews</p>
            </router-link>
            
            <router-link to="/profile" class="card p-4 text-center hover:bg-gray-50 transition-colors">
              <svg class="h-8 w-8 text-blue-600 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <p class="text-sm font-medium text-gray-900">Profile Settings</p>
            </router-link>
          </div>
        </div>
      </div>

      <!-- Seller Dashboard -->
      <div v-else-if="authStore.userRole === 'seller'" class="space-y-8">
        <div class="card p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Seller Dashboard</h2>
          <p class="text-gray-600">Manage your book listings, inventory, and sales analytics.</p>
          <div class="mt-4">
            <router-link to="/seller" class="btn-primary">
              Go to Seller Dashboard
            </router-link>
          </div>
        </div>
      </div>

      <!-- Affiliate Dashboard -->
      <div v-else-if="authStore.userRole === 'affiliate'" class="space-y-8">
        <div class="card p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Affiliate Dashboard</h2>
          <p class="text-gray-600">Track your referrals, commissions, and generate referral links.</p>
          <div class="mt-4">
            <router-link to="/affiliate" class="btn-primary">
              Go to Affiliate Dashboard
            </router-link>
          </div>
        </div>
      </div>

      <!-- Account Information -->
      <div class="mt-8 card p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Account Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-sm font-medium text-gray-600">Account Type</h3>
            <p class="mt-1 text-lg font-semibold text-gray-900 capitalize">{{ authStore.userRole }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-600">Member Since</h3>
            <p class="mt-1 text-lg font-semibold text-gray-900">{{ formatDate(authStore.user?.date_joined) }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-600">Email</h3>
            <p class="mt-1 text-lg font-semibold text-gray-900">{{ authStore.user?.email }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-600">Status</h3>
            <span :class="authStore.user?.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" 
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium capitalize">
              {{ authStore.user?.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import AppLayout from '../layouts/AppLayout.vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

const getRoleDescription = (role) => {
  const descriptions = {
    buyer: 'book purchasing',
    seller: 'book selling',
    affiliate: 'affiliate marketing'
  };
  return descriptions[role] || '';
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};
</script>