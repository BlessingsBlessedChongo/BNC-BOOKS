<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
      <div>
        <label for="first_name" class="block text-sm font-medium text-gray-700">
          First name
        </label>
        <input
          type="text"
          id="first_name"
          v-model="form.first_name"
          required
          class="mt-1 input-field"
          :class="{ 'border-red-500': errors.first_name }"
        />
        <p v-if="errors.first_name" class="mt-2 text-sm text-red-600">{{ errors.first_name }}</p>
      </div>

      <div>
        <label for="last_name" class="block text-sm font-medium text-gray-700">
          Last name
        </label>
        <input
          type="text"
          id="last_name"
          v-model="form.last_name"
          required
          class="mt-1 input-field"
          :class="{ 'border-red-500': errors.last_name }"
        />
        <p v-if="errors.last_name" class="mt-2 text-sm text-red-600">{{ errors.last_name }}</p>
      </div>
    </div>

    <div>
      <label for="street_address" class="block text-sm font-medium text-gray-700">
        Street address
      </label>
      <input
        type="text"
        id="street_address"
        v-model="form.street_address"
        required
        class="mt-1 input-field"
        :class="{ 'border-red-500': errors.street_address }"
      />
      <p v-if="errors.street_address" class="mt-2 text-sm text-red-600">{{ errors.street_address }}</p>
    </div>

    <div>
      <label for="apartment" class="block text-sm font-medium text-gray-700">
        Apartment, suite, etc. (optional)
      </label>
      <input
        type="text"
        id="apartment"
        v-model="form.apartment"
        class="mt-1 input-field"
      />
    </div>

    <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
      <div>
        <label for="city" class="block text-sm font-medium text-gray-700">
          City
        </label>
        <input
          type="text"
          id="city"
          v-model="form.city"
          required
          class="mt-1 input-field"
          :class="{ 'border-red-500': errors.city }"
        />
        <p v-if="errors.city" class="mt-2 text-sm text-red-600">{{ errors.city }}</p>
      </div>

      <div>
        <label for="state" class="block text-sm font-medium text-gray-700">
          State / Province
        </label>
        <input
          type="text"
          id="state"
          v-model="form.state"
          required
          class="mt-1 input-field"
          :class="{ 'border-red-500': errors.state }"
        />
        <p v-if="errors.state" class="mt-2 text-sm text-red-600">{{ errors.state }}</p>
      </div>

      <div>
        <label for="zip_code" class="block text-sm font-medium text-gray-700">
          ZIP / Postal code
        </label>
        <input
          type="text"
          id="zip_code"
          v-model="form.zip_code"
          required
          class="mt-1 input-field"
          :class="{ 'border-red-500': errors.zip_code }"
        />
        <p v-if="errors.zip_code" class="mt-2 text-sm text-red-600">{{ errors.zip_code }}</p>
      </div>
    </div>

    <div>
      <label for="country" class="block text-sm font-medium text-gray-700">
        Country
      </label>
      <select
        id="country"
        v-model="form.country"
        required
        class="mt-1 input-field"
        :class="{ 'border-red-500': errors.country }"
      >
        <option value="">Select a country</option>
        <option value="US">United States</option>
        <option value="CA">Canada</option>
        <option value="UK">United Kingdom</option>
        <option value="AU">Australia</option>
        <!-- Add more countries as needed -->
      </select>
      <p v-if="errors.country" class="mt-2 text-sm text-red-600">{{ errors.country }}</p>
    </div>

    <div>
      <label for="phone" class="block text-sm font-medium text-gray-700">
        Phone number
      </label>
      <input
        type="tel"
        id="phone"
        v-model="form.phone"
        class="mt-1 input-field"
        :class="{ 'border-red-500': errors.phone }"
      />
      <p v-if="errors.phone" class="mt-2 text-sm text-red-600">{{ errors.phone }}</p>
    </div>

    <div class="flex items-center">
      <input
        id="save_address"
        v-model="form.save_to_profile"
        type="checkbox"
        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
      />
      <label for="save_address" class="ml-2 block text-sm text-gray-900">
        Save this address to my profile
      </label>
    </div>

    <div class="flex justify-end">
      <button
        type="submit"
        :disabled="isLoading"
        class="btn-primary"
      >
        <span v-if="isLoading">Saving...</span>
        <span v-else>{{ submitButtonText }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'

const props = defineProps({
  address: {
    type: Object,
    default: () => ({})
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  submitButtonText: {
    type: String,
    default: 'Save Address'
  }
})

const emit = defineEmits(['submit'])

const form = reactive({
  first_name: props.address.first_name || '',
  last_name: props.address.last_name || '',
  street_address: props.address.street_address || '',
  apartment: props.address.apartment || '',
  city: props.address.city || '',
  state: props.address.state || '',
  zip_code: props.address.zip_code || '',
  country: props.address.country || 'US',
  phone: props.address.phone || '',
  save_to_profile: props.address.save_to_profile || false
})

const errors = reactive({})

const validateForm = () => {
  let isValid = true
  Object.keys(errors).forEach(key => delete errors[key])

  if (!form.first_name.trim()) {
    errors.first_name = 'First name is required'
    isValid = false
  }

  if (!form.last_name.trim()) {
    errors.last_name = 'Last name is required'
    isValid = false
  }

  if (!form.street_address.trim()) {
    errors.street_address = 'Street address is required'
    isValid = false
  }

  if (!form.city.trim()) {
    errors.city = 'City is required'
    isValid = false
  }

  if (!form.state.trim()) {
    errors.state = 'State is required'
    isValid = false
  }

  if (!form.zip_code.trim()) {
    errors.zip_code = 'ZIP code is required'
    isValid = false
  }

  if (!form.country) {
    errors.country = 'Country is required'
    isValid = false
  }

  return isValid
}

const submitForm = () => {
  if (validateForm()) {
    emit('submit', form)
  }
}
</script>