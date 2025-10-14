import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const loading = ref(false)

  const cartCount = computed(() => 
    items.value.reduce((total, item) => total + item.quantity, 0)
  )

  const cartTotal = computed(() =>
    items.value.reduce((total, item) => total + (item.book.price * item.quantity), 0)
  )

  const addToCart = async (bookId, quantity = 1) => {
    // Mock implementation
    const mockBook = {
      id: bookId,
      title: 'Sample Book',
      price: 19.99,
      cover_image: '/images/placeholder-book.jpg'
    }
    
    const existingItem = items.value.find(item => item.book.id === bookId)
    
    if (existingItem) {
      existingItem.quantity += quantity
    } else {
      items.value.push({
        id: Date.now(),
        book: mockBook,
        quantity,
        added_at: new Date().toISOString()
      })
    }
  }

  const removeFromCart = (itemId) => {
    items.value = items.value.filter(item => item.id !== itemId)
  }

  const updateQuantity = (itemId, quantity) => {
    const item = items.value.find(item => item.id === itemId)
    if (item) {
      item.quantity = quantity
    }
  }

  const clearCart = () => {
    items.value = []
  }

  return {
    items,
    loading,
    cartCount,
    cartTotal,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart
  }
})