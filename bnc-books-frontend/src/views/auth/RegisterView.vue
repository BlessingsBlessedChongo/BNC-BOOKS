<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
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
          <div v-if="authStore.error" class="rounded-md bg-red-50 p-4">
            <div class="text-sm text-red-700">
              {{ authStore.error }}
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="first_name" class="block text-sm font-medium text-gray-700">
                First name
              </label>
              <div class="mt-1">
                <input
                  id="first_name"
                  v-model="form.first_name"
                  name="first_name"
                  type="text"
                  required
                  class="input-field"
                  :class="{ 'border-red-500': errors.first_name }"
                />
                <p v-if="errors.first_name" class="mt-2 text-sm text-red-600">
                  {{ errors.first_name[0] }}
                </p>
              </div>
            </div>

            <div>
              <label for="last_name" class="block text-sm font-medium text-gray-700">
                Last name
              </label>
              <div class="mt-1">
                <input
                  id="last_name"
                  v-model="form.last_name"
                  name="last_name"
                  type="text"
                  required
                  class="input-field"
                  :class="{ 'border-red-500': errors.last_name }"
                />
                <p v-if="errors.last_name" class="mt-2 text-sm text-red-600">
                  {{ errors.last_name[0] }}
                </p>
              </div>
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
              />
              <p v-if="errors.email" class="mt-2 text-sm text-red-600">
                {{ errors.email[0] }}
              </p>
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
              />
              <p v-if="errors.password" class="mt-2 text-sm text-red-600">
                {{ errors.password[0] }}
              </p>
              <p class="mt-1 text-xs text-gray-500">
                Must be at least 8 characters with uppercase, number, and special character
              </p>
            </div>
          </div>

          <div>
            <label for="password_confirm" class="block text-sm font-medium text-gray-700">
              Confirm password
            </label>
            <div class="mt-1">
              <input
                id="password_confirm"
                v-model="form.password_confirm"
                name="password_confirm"
                type="password"
                autocomplete="new-password"
                required
                class="input-field"
                :class="{ 'border-red-500': errors.password_confirm }"
              />
              <p v-if="errors.password_confirm" class="mt-2 text-sm text-red-600">
                {{ errors.password_confirm[0] }}
              </p>
            </div>
          </div>

          <div>
            <label for="role" class="block text-sm font-medium text-gray-700">
              Account type
            </label>
            <div class="mt-1">
              <select
                id="role"
                v-model="form.role"
                name="role"
                required
                class="input-field"
                :class="{ 'border-red-500': errors.role }"
                @change="console.log('Selected role:', form.role)"
              >
                <option value="" disabled>Select account type</option>
                <option value="buyer">Buyer</option>
                <option value="seller">Seller</option>
                <option value="affiliate">Affiliate</option>
              </select>
              <p v-if="errors.role" class="mt-2 text-sm text-red-600">
                {{ errors.role[0] }}
              </p>
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="authStore.isLoading"
              class="w-full flex justify-center btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="authStore.isLoading">Creating account...</span>
              <span v-else>Create account</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  password_confirm: '',
  role: ''
});

const errors = ref({});

const handleRegister = async () => {
  errors.value = {};
  authStore.clearError();

  try {
    const response = await authStore.register(form);
    if (Object.keys(response).length === 0) {
      router.push('/dashboard'); // Success
    } else {
      errors.value = response; // Set field-specific errors
    }
  } catch (error) {
    console.error('Registration failed:', error);
  }
};
</script>