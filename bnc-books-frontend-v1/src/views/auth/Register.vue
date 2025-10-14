<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="flex justify-center">
        <div class="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
          </svg>
        </div>
      </div>
      <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">
        Create your account
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Or 
        <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500">
          sign in to your existing account
        </router-link>
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="card py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <div>
            <label for="firstName" class="block text-sm font-medium text-gray-700">
              First Name
            </label>
            <div class="mt-1">
              <input
                id="firstName"
                v-model="form.first_name"
                name="firstName"
                type="text"
                required
                class="input-field"
                :class="{ 'border-red-500': errors.first_name }"
              >
              <p v-if="errors.first_name" class="mt-2 text-sm text-red-600">{{ errors.first_name }}</p>
            </div>
          </div>

          <div>
            <label for="lastName" class="block text-sm font-medium text-gray-700">
              Last Name
            </label>
            <div class="mt-1">
              <input
                id="lastName"
                v-model="form.last_name"
                name="lastName"
                type="text"
                required
                class="input-field"
                :class="{ 'border-red-500': errors.last_name }"
              >
              <p v-if="errors.last_name" class="mt-2 text-sm text-red-600">{{ errors.last_name }}</p>
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email address
            </label>
            <div class="mt-1">
              <input
                id="email"
                v-model="form.email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="input-field"
                :class="{ 'border-red-500': errors.email }"
              >
              <p v-if="errors.email" class="mt-2 text-sm text-red-600">{{ errors.email }}</p>
            </div>
          </div>

          <div>
            <label for="role" class="block text-sm font-medium text-gray-700">
              I want to be a
            </label>
            <div class="mt-1">
              <select
                id="role"
                v-model="form.role"
                name="role"
                required
                class="input-field"
              >
                <option value="buyer">Buyer</option>
                <option value="seller">Seller</option>
                <option value="affiliate">Affiliate</option>
              </select>
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1">
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                autocomplete="new-password"
                required
                class="input-field"
                :class="{ 'border-red-500': errors.password }"
              >
              <p v-if="errors.password" class="mt-2 text-sm text-red-600">{{ errors.password }}</p>
            </div>
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
              Confirm Password
            </label>
            <div class="mt-1">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                name="confirmPassword"
                type="password"
                autocomplete="new-password"
                required
                class="input-field"
                :class="{ 'border-red-500': errors.confirmPassword }"
              >
              <p v-if="errors.confirmPassword" class="mt-2 text-sm text-red-600">{{ errors.confirmPassword }}</p>
            </div>
          </div>

          <div class="flex items-center">
            <input
              id="terms"
              v-model="form.agreeTerms"
              name="terms"
              type="checkbox"
              required
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            >
            <label for="terms" class="ml-2 block text-sm text-gray-900">
              I agree to the 
              <a href="#" class="text-primary-600 hover:text-primary-500">Terms and Conditions</a>
            </label>
          </div>

          <div>
            <button
              type="submit"
              :disabled="authStore.isLoading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="authStore.isLoading">Creating account...</span>
              <span v-else>Create account</span>
            </button>
          </div>

          <div v-if="authStore.error" class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  Registration failed
                </h3>
                <div class="mt-2 text-sm text-red-700">
                  <p>{{ authStore.error }}</p>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  role: 'buyer',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const errors = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  confirmPassword: '',
  password2: ''
})

const validateForm = () => {
  let isValid = true
  
  // Clear previous errors
  Object.keys(errors).forEach(key => errors[key] = '')

  if (!form.first_name.trim()) {
    errors.first_name = 'First name is required'
    isValid = false
  }

  if (!form.last_name.trim()) {
    errors.last_name = 'Last name is required'
    isValid = false
  }

  if (!form.email) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Email is invalid'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (form.password.length < 8) {
    errors.password = 'Password must be at least 8 characters'
    isValid = false
  }

  if (!form.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password'
    isValid = false
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  if (!form.agreeTerms) {
    alert('Please agree to the terms and conditions')
    isValid = false
  }

  return isValid
}

const handleRegister = async () => {
  if (!validateForm()) return

  // Prepare data for Django backend - match serializer fields exactly
  const registrationData = {
    first_name: form.first_name.trim(),
    last_name: form.last_name.trim(),
    email: form.email.trim().toLowerCase(),
    role: form.role,
    password: form.password,
    password2: form.password  // Django expects password2 for confirmation
  }
  
  console.log('Sending registration data:', registrationData)
  
  try {
    const result = await authStore.register(registrationData)

    if (result.success) {
      router.push('/dashboard')
    } else {
      // Handle errors from backend
      if (result.errors) {
        console.error('Server validation errors:', result.errors)
        
        // Map server errors to form fields
        Object.keys(result.errors).forEach(key => {
          if (errors.hasOwnProperty(key)) {
            const errorMsg = result.errors[key]
            errors[key] = Array.isArray(errorMsg) ? errorMsg[0] : errorMsg
          }
        })
      }
    }
  } catch (error) {
    console.error('Registration error:', error)
  }
}

onMounted(() => {
  authStore.clearError()
})
</script>