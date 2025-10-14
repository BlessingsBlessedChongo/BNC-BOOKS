<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="card p-6">
      <div class="border-b border-gray-200 pb-6">
        <h1 class="text-2xl font-bold text-gray-900">Profile Settings</h1>
        <p class="mt-1 text-sm text-gray-600">Manage your account settings and preferences</p>
      </div>

      <div class="mt-6 grid gap-8 lg:grid-cols-3">
        <!-- Sidebar -->
        <div class="lg:col-span-1">
          <nav class="space-y-1">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              class="w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200"
              :class="activeTab === tab.id ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'"
            >
              <component :is="tab.icon" class="h-5 w-5 mr-3" />
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <!-- Content -->
        <div class="lg:col-span-2">
          <!-- Personal Information -->
          <div v-if="activeTab === 'personal'" class="space-y-6">
            <h2 class="text-lg font-medium text-gray-900">Personal Information</h2>
            
            <form @submit.prevent="updateProfile" class="space-y-6">
              <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
                  <input
                    type="text"
                    id="first_name"
                    v-model="profileForm.first_name"
                    class="mt-1 input-field"
                    :class="{ 'border-red-500': profileErrors.first_name }"
                  />
                  <p v-if="profileErrors.first_name" class="mt-2 text-sm text-red-600">{{ profileErrors.first_name }}</p>
                </div>

                <div>
                  <label for="last_name" class="block text-sm font-medium text-gray-700">Last Name</label>
                  <input
                    type="text"
                    id="last_name"
                    v-model="profileForm.last_name"
                    class="mt-1 input-field"
                    :class="{ 'border-red-500': profileErrors.last_name }"
                  />
                  <p v-if="profileErrors.last_name" class="mt-2 text-sm text-red-600">{{ profileErrors.last_name }}</p>
                </div>
              </div>

              <div>
                <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
                <input
                  type="email"
                  id="email"
                  v-model="profileForm.email"
                  class="mt-1 input-field"
                  :class="{ 'border-red-500': profileErrors.email }"
                />
                <p v-if="profileErrors.email" class="mt-2 text-sm text-red-600">{{ profileErrors.email }}</p>
              </div>

              <div>
                <label for="phone" class="block text-sm font-medium text-gray-700">Phone Number</label>
                <input
                  type="tel"
                  id="phone"
                  v-model="profileForm.phone"
                  class="mt-1 input-field"
                  :class="{ 'border-red-500': profileErrors.phone }"
                />
                <p v-if="profileErrors.phone" class="mt-2 text-sm text-red-600">{{ profileErrors.phone }}</p>
              </div>

              <div class="flex justify-end">
                <button
                  type="submit"
                  :disabled="userStore.isLoading"
                  class="btn-primary"
                >
                  <span v-if="userStore.isLoading">Saving...</span>
                  <span v-else>Save Changes</span>
                </button>
              </div>
            </form>
          </div>

          <!-- Change Password -->
          <div v-if="activeTab === 'password'" class="space-y-6">
            <h2 class="text-lg font-medium text-gray-900">Change Password</h2>
            
            <form @submit.prevent="changePassword" class="space-y-6">
              <div>
                <label for="current_password" class="block text-sm font-medium text-gray-700">Current Password</label>
                <input
                  type="password"
                  id="current_password"
                  v-model="passwordForm.current_password"
                  class="mt-1 input-field"
                  :class="{ 'border-red-500': passwordErrors.current_password }"
                />
                <p v-if="passwordErrors.current_password" class="mt-2 text-sm text-red-600">{{ passwordErrors.current_password }}</p>
              </div>

              <div>
                <label for="new_password" class="block text-sm font-medium text-gray-700">New Password</label>
                <input
                  type="password"
                  id="new_password"
                  v-model="passwordForm.new_password"
                  class="mt-1 input-field"
                  :class="{ 'border-red-500': passwordErrors.new_password }"
                />
                <p v-if="passwordErrors.new_password" class="mt-2 text-sm text-red-600">{{ passwordErrors.new_password }}</p>
              </div>

              <div>
                <label for="confirm_password" class="block text-sm font-medium text-gray-700">Confirm New Password</label>
                <input
                  type="password"
                  id="confirm_password"
                  v-model="passwordForm.confirm_password"
                  class="mt-1 input-field"
                  :class="{ 'border-red-500': passwordErrors.confirm_password }"
                />
                <p v-if="passwordErrors.confirm_password" class="mt-2 text-sm text-red-600">{{ passwordErrors.confirm_password }}</p>
              </div>

              <div class="flex justify-end">
                <button
                  type="submit"
                  :disabled="userStore.isLoading"
                  class="btn-primary"
                >
                  <span v-if="userStore.isLoading">Updating...</span>
                  <span v-else>Update Password</span>
                </button>
              </div>
            </form>
          </div>

          <!-- Account Settings -->
          <div v-if="activeTab === 'account'" class="space-y-6">
            <h2 class="text-lg font-medium text-gray-900">Account Settings</h2>
            
            <div class="space-y-4">
              <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <h3 class="text-sm font-medium text-gray-900">Account Role</h3>
                  <p class="text-sm text-gray-500 capitalize">{{ authStore.userRole }}</p>
                </div>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800 capitalize">
                  {{ authStore.userRole }}
                </span>
              </div>

              <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <h3 class="text-sm font-medium text-gray-900">Account Status</h3>
                  <p class="text-sm text-gray-500">Your account is active and in good standing</p>
                </div>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </div>

              <div class="p-4 border border-yellow-200 bg-yellow-50 rounded-lg">
                <h3 class="text-sm font-medium text-yellow-800">Danger Zone</h3>
                <p class="mt-1 text-sm text-yellow-700">Once you delete your account, there is no going back. Please be certain.</p>
                <button class="mt-3 btn-secondary bg-red-600 hover:bg-red-700 text-white">
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notifications'

const authStore = useAuthStore()
const userStore = useUserStore()
const notificationStore = useNotificationStore()

const activeTab = ref('personal')

const tabs = [
  { id: 'personal', name: 'Personal Information', icon: UserIcon },
  { id: 'password', name: 'Change Password', icon: LockIcon },
  { id: 'account', name: 'Account Settings', icon: CogIcon }
]

const profileForm = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone: ''
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const profileErrors = reactive({})
const passwordErrors = reactive({})

const validateProfile = () => {
  let isValid = true
  profileErrors.first_name = ''
  profileErrors.last_name = ''
  profileErrors.email = ''
  profileErrors.phone = ''

  if (!profileForm.first_name.trim()) {
    profileErrors.first_name = 'First name is required'
    isValid = false
  }

  if (!profileForm.last_name.trim()) {
    profileErrors.last_name = 'Last name is required'
    isValid = false
  }

  if (!profileForm.email) {
    profileErrors.email = 'Email is required'
    isValid = false
  } else if (!/\S+@\S+\.\S+/.test(profileForm.email)) {
    profileErrors.email = 'Email is invalid'
    isValid = false
  }

  return isValid
}

const validatePassword = () => {
  let isValid = true
  passwordErrors.current_password = ''
  passwordErrors.new_password = ''
  passwordErrors.confirm_password = ''

  if (!passwordForm.current_password) {
    passwordErrors.current_password = 'Current password is required'
    isValid = false
  }

  if (!passwordForm.new_password) {
    passwordErrors.new_password = 'New password is required'
    isValid = false
  } else if (passwordForm.new_password.length < 6) {
    passwordErrors.new_password = 'Password must be at least 6 characters'
    isValid = false
  }

  if (!passwordForm.confirm_password) {
    passwordErrors.confirm_password = 'Please confirm your password'
    isValid = false
  } else if (passwordForm.new_password !== passwordForm.confirm_password) {
    passwordErrors.confirm_password = 'Passwords do not match'
    isValid = false
  }

  return isValid
}

const updateProfile = async () => {
  if (!validateProfile()) return

  const result = await userStore.updateProfile(profileForm)
  
  if (result.success) {
    notificationStore.success('Profile updated successfully')
    // Update auth store user data
    authStore.user = { ...authStore.user, ...profileForm }
  }
}

const changePassword = async () => {
  if (!validatePassword()) return

  const result = await userStore.changePassword({
    old_password: passwordForm.current_password,
    new_password: passwordForm.new_password
  })
  
  if (result.success) {
    notificationStore.success('Password changed successfully')
    // Reset form
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  }
}

onMounted(async () => {
  // Load user profile
  const result = await userStore.fetchProfile()
  if (result.success) {
    Object.assign(profileForm, result.data)
  }
})

// Icon components
const UserIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </svg>
  `
}

const LockIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
    </svg>
  `
}

const CogIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  `
}
</script>