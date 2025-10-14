<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">
        Sign in to BNC Books
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Or
        <router-link to="/register" class="font-medium text-primary-600 hover:text-primary-500">
          create a new account
        </router-link>
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="card py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <div v-if="authStore.error" class="rounded-md bg-red-50 p-4">
            <div class="text-sm text-red-700">
              {{ authStore.error }}
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
                autocomplete="current-password"
                required
                class="input-field"
                :class="{ 'border-red-500': errors.password }"
              />
              <p v-if="errors.password" class="mt-2 text-sm text-red-600">
                {{ errors.password[0] }}
              </p>
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="authStore.isLoading"
              class="w-full flex justify-center btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="authStore.isLoading">Signing in...</span>
              <span v-else>Sign in</span>
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
  email: '',
  password: ''
});

const errors = ref({});

const handleLogin = async () => {
  errors.value = {};
  authStore.clearError();

  try {
    const response = await authStore.login(form);
    errors.value = response; // Set field-specific errors
    if (!response.email && !response.password) {
      router.push('/dashboard'); // Success
    }
  } catch (error) {
    // Errors are already set in authStore.login
  }
};
</script>