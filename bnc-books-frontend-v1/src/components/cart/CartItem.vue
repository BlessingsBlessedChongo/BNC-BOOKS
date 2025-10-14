<template>
  <div class="flex items-center hover:bg-gray-50 -mx-8 px-6 py-5">
    <div class="flex w-2/5">
      <!-- Product -->
      <div class="w-20">
        <img
          :src="item.book.cover_image || '/placeholder-book.jpg'"
          :alt="item.book.title"
          class="h-24 w-16 object-cover rounded"
        />
      </div>
      <div class="flex flex-col justify-between ml-4 flex-grow">
        <span class="font-bold text-sm">{{ item.book.title }}</span>
        <span class="text-red-500 text-xs">by {{ item.book.author }}</span>
        <button
          @click="removeItem"
          class="font-semibold hover:text-red-500 text-gray-500 text-xs text-left"
        >
          Remove
        </button>
      </div>
    </div>
    
    <div class="flex justify-center w-1/5">
      <!-- Quantity Controls -->
      <div class="flex items-center border rounded-lg">
        <button
          @click="decreaseQuantity"
          :disabled="item.quantity <= 1"
          class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path>
          </svg>
        </button>
        <input
          :value="item.quantity"
          @change="updateQuantity($event.target.value)"
          class="mx-2 border text-center w-8 text-sm"
          type="number"
          min="1"
          :max="item.book.stock_quantity"
        />
        <button
          @click="increaseQuantity"
          :disabled="item.quantity >= item.book.stock_quantity"
          class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
        </button>
      </div>
    </div>
    
    <span class="text-center w-1/5 font-semibold text-sm">
      ${{ item.book.price.toFixed(2) }}
    </span>
    
    <span class="text-center w-1/5 font-semibold text-sm">
      ${{ (item.book.price * item.quantity).toFixed(2) }}
    </span>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notifications'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const cartStore = useCartStore()
const notificationStore = useNotificationStore()

const decreaseQuantity = async () => {
  if (props.item.quantity > 1) {
    await updateQuantity(props.item.quantity - 1)
  }
}

const increaseQuantity = async () => {
  if (props.item.quantity < props.item.book.stock_quantity) {
    await updateQuantity(props.item.quantity + 1)
  }
}

const updateQuantity = async (newQuantity) => {
  const quantity = parseInt(newQuantity)
  if (isNaN(quantity) || quantity < 1 || quantity > props.item.book.stock_quantity) {
    return
  }

  const result = await cartStore.updateCartItem(props.item.id, quantity)
  if (result.success) {
    notificationStore.success('Cart updated')
  }
}

const removeItem = async () => {
  const result = await cartStore.removeFromCart(props.item.id)
  if (result.success) {
    notificationStore.success('Item removed from cart')
  }
}
</script>