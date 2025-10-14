import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import api from '../utils/api';

export const useBooksStore = defineStore('books', () => {
  const books = ref([]);
  const featuredBooks = ref([]);
  const categories = ref([]);
  const currentBook = ref(null);
  const isLoading = ref(false);
  const searchQuery = ref('');
  const filters = reactive({
    category: '',
    genre: '',
    min_price: '',
    max_price: '',
    min_rating: '',
    in_stock: false,
    featured: false,
    ordering: 'title',
    page: 1,
    page_size: 12
  });
  const pagination = reactive({
    count: 0,
    next: null,
    previous: null,
    total_pages: 0,
    current_page: 1
  });

  // Getters
  const hasBooks = () => books.value.length > 0;
  const hasFilters = () => {
    return Object.values(filters).some(value => 
      value !== '' && value !== false && value !== 1
    );
  };

  // Actions
  const fetchBooks = async (params = {}) => {
    isLoading.value = true;
    try {
      const response = await api.get('/books/', { 
        params: { ...filters, ...params, search: searchQuery.value } 
      });
      books.value = response.data.results;
      Object.assign(pagination, {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        total_pages: response.data.total_pages,
        current_page: response.data.current_page || 1
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch books:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };

  const fetchFeaturedBooks = async () => {
    try {
      const response = await api.get('/books/featured/');
      featuredBooks.value = response.data.results;
      return response.data;
    } catch (error) {
      console.error('Failed to fetch featured books:', error);
      throw error;
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get('/books/categories/');
      categories.value = response.data.categories;
      return response.data;
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      throw error;
    }
  };

  const fetchBookById = async (id) => {
    isLoading.value = true;
    try {
      const response = await api.get(`/books/${id}/`);
      currentBook.value = response.data;
      return response.data;
    } catch (error) {
      console.error('Failed to fetch book:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };

  const searchBooks = async (query) => {
    searchQuery.value = query;
    filters.page = 1; // Reset to first page when searching
    return await fetchBooks();
  };

  const updateFilters = async (newFilters) => {
    Object.assign(filters, newFilters);
    filters.page = 1; // Reset to first page when filters change
    return await fetchBooks();
  };

  const clearFilters = async () => {
    Object.keys(filters).forEach(key => {
      if (key !== 'page_size' && key !== 'ordering') {
        filters[key] = key === 'in_stock' || key === 'featured' ? false : '';
      }
    });
    searchQuery.value = '';
    return await fetchBooks();
  };

  const loadNextPage = async () => {
    if (pagination.next) {
      filters.page += 1;
      return await fetchBooks();
    }
  };

  const loadPreviousPage = async () => {
    if (pagination.previous) {
      filters.page -= 1;
      return await fetchBooks();
    }
  };

  const goToPage = async (page) => {
    filters.page = page;
    return await fetchBooks();
  };

  return {
    // State
    books,
    featuredBooks,
    categories,
    currentBook,
    isLoading,
    searchQuery,
    filters,
    pagination,
    
    // Getters
    hasBooks,
    hasFilters,
    
    // Actions
    fetchBooks,
    fetchFeaturedBooks,
    fetchCategories,
    fetchBookById,
    searchBooks,
    updateFilters,
    clearFilters,
    loadNextPage,
    loadPreviousPage,
    goToPage
  };
});