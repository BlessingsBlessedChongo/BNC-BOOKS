<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div class="bg-white shadow rounded-lg">
        <!-- Profile Header -->
        <div class="px-6 py-4 border-b border-gray-200">
          <h1 class="text-2xl font-bold text-gray-900">Profile Settings</h1>
          <p class="mt-1 text-sm text-gray-600">Manage your account settings and preferences</p>
        </div>

        <div class="p-6">
          <!-- Personal Information -->
          <div class="mb-8">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Personal Information</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">First Name</label>
                <input 
                  v-model="profileForm.first_name"
                  type="text"
                  class="input-field"
                  :class="{ 'border-red-500': profileErrors.first_name }"
                />
                <p v-if="profileErrors.first_name" class="mt-1 text-sm text-red-600">
                  {{ profileErrors.first_name[0] }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
                <input 
                  v-model="profileForm.last_name"
                  type="text"
                  class="input-field"
                  :class="{ 'border-red-500': profileErrors.last_name }"
                />
                <p v-if="profileErrors.last_name" class="mt-1 text-sm text-red-600">
                  {{ profileErrors.last_name[0] }}
                </p>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                <input 
                  v-model="profileForm.email"
                  type="email"
                  class="input-field"
                  :class="{ 'border-red-500': profileErrors.email }"
                />
                <p v-if="profileErrors.email" class="mt-1 text-sm text-red-600">
                  {{ profileErrors.email[0] }}
                </p>
              </div>
            </div>
            <div class="mt-6 flex justify-end">
              <button 
                @click="updateProfile"
                :disabled="profileLoading"
                class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="profileLoading">Updating...</span>
                <span v-else>Update Profile</span>
              </button>
            </div>
          </div>

          <!-- Account Type -->
          <div class="mb-8">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Account Type</h2>
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-900 capitalize">{{ authStore.userRole }} Account</p>
                  <p class="text-sm text-gray-600 mt-1">
                    {{ getAccountDescription(authStore.userRole) }}
                  </p>
                </div>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800 capitalize">
                  {{ authStore.userRole }}
                </span>
              </div>
            </div>
          </div>

          <!-- Change Password -->
          <div class="border-t border-gray-200 pt-8">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Change Password</h2>
            <div class="grid grid-cols-1 gap-4 max-w-md">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
                <input 
                  v-model="passwordForm.old_password"
                  type="password"
                  class="input-field"
                  :class="{ 'border-red-500': passwordErrors.old_password }"
                />
                <p v-if="passwordErrors.old_password" class="mt-1 text-sm text-red-600">
                  {{ passwordErrors.old_password[0] }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">New Password</label>
                <input 
                  v-model="passwordForm.new_password"
                  type="password"
                  class="input-field"
                  :class="{ 'border-red-500': passwordErrors.new_password }"
                />
                <p v-if="passwordErrors.new_password" class="mt-1 text-sm text-red-600">
                  {{ passwordErrors.new_password[0] }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
                <input 
                  v-model="passwordForm.new_password_confirm"
                  type="password"
                  class="input-field"
                  :class="{ 'border-red-500': passwordErrors.new_password_confirm }"
                />
                <p v-if="passwordErrors.new_password_confirm" class="mt-1 text-sm text-red-600">
                  {{ passwordErrors.new_password_confirm[0] }}
                </p>
              </div>
              <div class="mt-4">
                <button 
                  @click="changePassword"
                  :disabled="passwordLoading"
                  class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span v-if="passwordLoading">Changing Password...</span>
                  <span v-else>Change Password</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import AppLayout from '../layouts/AppLayout.vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

const profileForm = reactive({
  first_name: '',
  last_name: '',
  email: ''
});

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
});

const profileLoading = ref(false);
const passwordLoading = ref(false);
const profileErrors = ref({});
const passwordErrors = ref({});

const getAccountDescription = (role) => {
  const descriptions = {
    buyer: 'Browse and purchase books from our marketplace',
    seller: 'List and sell your books to buyers worldwide',
    affiliate: 'Earn commissions by referring customers to our platform'
  };
  return descriptions[role] || '';
};

const updateProfile = async () => {
  profileLoading.value = true;
  profileErrors.value = {};

  try {
    // TODO: Implement profile update API call
    console.log('Updating profile:', profileForm);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Update local user data
    authStore.user = { ...authStore.user, ...profileForm };
    localStorage.setItem('user', JSON.stringify(authStore.user));
    
    // Show success message
    alert('Profile updated successfully!');
  } catch (error) {
    if (error.response?.data) {
      profileErrors.value = error.response.data;
    } else {
      alert('Failed to update profile. Please try again.');
    }
  } finally {
    profileLoading.value = false;
  }
};

const changePassword = async () => {
  passwordLoading.value = true;
  passwordErrors.value = {};

  try {
    await authStore.changePassword(passwordForm);
    
    // Clear form on success
    Object.keys(passwordForm).forEach(key => {
      passwordForm[key] = '';
    });
    
    alert('Password changed successfully!');
  } catch (error) {
    if (error.response?.data) {
      passwordErrors.value = error.response.data;
    }
  } finally {
    passwordLoading.value = false;
  }
};

// Initialize form with current user data
onMounted(() => {
  if (authStore.user) {
    profileForm.first_name = authStore.user.first_name || '';
    profileForm.last_name = authStore.user.last_name || '';
    profileForm.email = authStore.user.email || '';
  }
});
</script>