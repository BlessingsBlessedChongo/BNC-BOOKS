<template>
  <div :class="['text-center py-12', containerClass]">
    <!-- Icon -->
    <div class="flex justify-center">
      <component
        :is="icon"
        :class="['mx-auto h-12 w-12', iconColor]"
      />
    </div>

    <!-- Title -->
    <h3 :class="['mt-4 text-lg font-medium', titleClass]">
      {{ title }}
    </h3>

    <!-- Description -->
    <p :class="['mt-2 text-sm', descriptionClass]">
      {{ description }}
    </p>

    <!-- Action Buttons -->
    <div v-if="showAction" class="mt-6">
      <button
        v-if="actionButtonText"
        @click="handleAction"
        :class="[
          'inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2',
          actionButtonClass
        ]"
      >
        <component
          v-if="actionIcon"
          :is="actionIcon"
          class="h-4 w-4 mr-2"
        />
        {{ actionButtonText }}
      </button>
      
      <button
        v-if="secondaryButtonText"
        @click="handleSecondaryAction"
        class="ml-3 inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
      >
        {{ secondaryButtonText }}
      </button>
    </div>

    <!-- Additional Content Slot -->
    <div v-if="$slots.default" class="mt-4">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { 
  MagnifyingGlassIcon, 
  HeartIcon, 
  ShoppingCartIcon, 
  BookOpenIcon,
  ExclamationTriangleIcon,
  PlusIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  type: {
    type: String,
    default: 'default', // 'search', 'wishlist', 'cart', 'orders', 'error', 'custom'
    validator: (value) => ['default', 'search', 'wishlist', 'cart', 'orders', 'error', 'custom'].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  icon: {
    type: [Object, Function],
    default: null
  },
  iconColor: {
    type: String,
    default: 'text-gray-400'
  },
  showAction: {
    type: Boolean,
    default: true
  },
  actionButtonText: {
    type: String,
    default: ''
  },
  actionButtonClass: {
    type: String,
    default: 'text-white bg-teal-600 hover:bg-teal-700 focus:ring-teal-500'
  },
  actionIcon: {
    type: [Object, Function],
    default: null
  },
  secondaryButtonText: {
    type: String,
    default: ''
  },
  containerClass: {
    type: String,
    default: ''
  },
  titleClass: {
    type: String,
    default: 'text-gray-900'
  },
  descriptionClass: {
    type: String,
    default: 'text-gray-600'
  }
})

const emit = defineEmits(['action', 'secondary-action'])

// Default configurations for common empty states
const emptyStateConfigs = {
  default: {
    icon: BookOpenIcon,
    title: 'No items found',
    description: 'Get started by adding some items.',
    actionButtonText: 'Get Started',
    actionIcon: PlusIcon
  },
  search: {
    icon: MagnifyingGlassIcon,
    title: 'No results found',
    description: 'Try adjusting your search criteria or browse all items.',
    actionButtonText: 'Browse All',
    actionIcon: BookOpenIcon
  },
  wishlist: {
    icon: HeartIcon,
    title: 'Your wishlist is empty',
    description: 'Start adding books you\'d like to save for later.',
    actionButtonText: 'Browse Books',
    actionIcon: BookOpenIcon
  },
  cart: {
    icon: ShoppingCartIcon,
    title: 'Your cart is empty',
    description: 'Add some books to your cart to get started.',
    actionButtonText: 'Start Shopping',
    actionIcon: BookOpenIcon
  },
  orders: {
    icon: BookOpenIcon,
    title: 'No orders yet',
    description: 'Your order history will appear here once you make a purchase.',
    actionButtonText: 'Browse Books',
    actionIcon: BookOpenIcon
  },
  error: {
    icon: ExclamationTriangleIcon,
    title: 'Something went wrong',
    description: 'We encountered an error while loading this content.',
    actionButtonText: 'Try Again',
    actionIcon: ArrowPathIcon,
    actionButtonClass: 'text-white bg-red-600 hover:bg-red-700 focus:ring-red-500'
  }
}

// Computed properties for dynamic content
const config = emptyStateConfigs[props.type] || emptyStateConfigs.default

const finalTitle = props.title || config.title
const finalDescription = props.description || config.description
const finalIcon = props.icon || config.icon
const finalActionButtonText = props.actionButtonText || config.actionButtonText
const finalActionIcon = props.actionIcon || config.actionIcon
const finalActionButtonClass = props.actionButtonClass || config.actionButtonClass

// Methods
const handleAction = () => {
  emit('action')
}

const handleSecondaryAction = () => {
  emit('secondary-action')
}
</script>