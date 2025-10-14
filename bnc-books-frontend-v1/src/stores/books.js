import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiMethods } from '@/utils/api'

export const useBookStore = defineStore('books', () => {
  const books = ref([])
  const currentBook = ref(null)
  const featuredBooks = ref([])
  const categories = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  
  const filters = ref({
    search: '',
    category: '',
    genre: '',
    minPrice: '',
    maxPrice: '',
    rating: '',
    inStock: false,
    featured: false
  })
  
  const pagination = ref({
    currentPage: 1,
    totalPages: 1,
    totalCount: 0,
    pageSize: 12
  })
  
  const sortBy = ref('title')
  const sortOrder = ref('asc')

  // Computed
  const filteredBooks = computed(() => {
    let filtered = [...books.value]

    // Apply search filter
    if (filters.value.search) {
      const searchTerm = filters.value.search.toLowerCase()
      filtered = filtered.filter(book => 
        book.title.toLowerCase().includes(searchTerm) ||
        book.author.toLowerCase().includes(searchTerm) ||
        book.isbn.includes(searchTerm)
      )
    }

    // Apply category filter
    if (filters.value.category) {
      filtered = filtered.filter(book => book.category === filters.value.category)
    }

    // Apply genre filter
    if (filters.value.genre) {
      filtered = filtered.filter(book => book.genres?.includes(filters.value.genre))
    }

    // Apply price range filter
    if (filters.value.minPrice) {
      filtered = filtered.filter(book => book.price >= parseFloat(filters.value.minPrice))
    }
    if (filters.value.maxPrice) {
      filtered = filtered.filter(book => book.price <= parseFloat(filters.value.maxPrice))
    }

    // Apply rating filter
    if (filters.value.rating) {
      filtered = filtered.filter(book => book.average_rating >= parseFloat(filters.value.rating))
    }

    // Apply stock filter
    if (filters.value.inStock) {
      filtered = filtered.filter(book => book.stock_quantity > 0)
    }

    // Apply featured filter
    if (filters.value.featured) {
      filtered = filtered.filter(book => book.is_featured)
    }

    return filtered
  })

  const genres = computed(() => {
    const genres = new Set()
    books.value.forEach(book => {
      book.genres?.forEach(genre => genres.add(genre))
    })
    return Array.from(genres).sort()
  })

  // Actions
  const fetchBooks = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await apiMethods.getBooks({
        page: params.page || pagination.value.currentPage,
        page_size: params.pageSize || pagination.value.pageSize,
        search: filters.value.search,
        category: filters.value.category,
        genre: filters.value.genre,
        min_price: filters.value.minPrice,
        max_price: filters.value.maxPrice,
        min_rating: filters.value.rating,
        in_stock: filters.value.inStock,
        featured: filters.value.featured,
        ordering: `${sortOrder.value === 'desc' ? '-' : ''}${sortBy.value}`
      })
      
      books.value = response.results
      pagination.value = {
        currentPage: response.current_page,
        totalPages: response.total_pages,
        totalCount: response.count,
        pageSize: response.page_size
      }
      
      return { success: true, data: response }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch books'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchBook = async (bookId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await apiMethods.getBook(bookId)
      currentBook.value = response
      return { success: true, data: response }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch book'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchFeaturedBooks = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await apiMethods.getFeaturedBooks()
      featuredBooks.value = response.results
      return { success: true, data: response }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch featured books'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await apiMethods.getCategories()
      categories.value = response.categories
      return { success: true, data: response }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch categories'
      return { success: false, error: error.value }
    }
  }

  const updateFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.currentPage = 1
  }

  const clearFilters = () => {
    filters.value = {
      search: '',
      category: '',
      genre: '',
      minPrice: '',
      maxPrice: '',
      rating: '',
      inStock: false,
      featured: false
    }
    pagination.value.currentPage = 1
  }

  const setSorting = (field, order = 'asc') => {
    sortBy.value = field
    sortOrder.value = order
  }

  const setPage = (page) => {
    if (page >= 1 && page <= pagination.value.totalPages) {
      pagination.value.currentPage = page
    }
  }

  const clearError = () => {
    error.value = null
  }

  // Initialize categories
  fetchCategories()

  return {
    // State
    books,
    currentBook,
    featuredBooks,
    categories,
    isLoading,
    error,
    filters,
    pagination,
    sortBy,
    sortOrder,
    
    // Computed
    filteredBooks,
    genres,
    
    // Actions
    fetchBooks,
    fetchBook,
    fetchFeaturedBooks,
    fetchCategories,
    updateFilters,
    clearFilters,
    setSorting,
    setPage,
    clearError
  }
})