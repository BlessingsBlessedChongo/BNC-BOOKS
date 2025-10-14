import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../utils/api';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
  const accessToken = ref(localStorage.getItem('access_token') || '');
  const refreshToken = ref(localStorage.getItem('refresh_token') || '');
  const isLoading = ref(false);
  const error = ref('');

  const isAuthenticated = computed(() => !!accessToken.value);
  const userRole = computed(() => user.value?.role || '');

  const setAuth = (userData, tokens) => {
    user.value = userData;
    accessToken.value = tokens.access;
    refreshToken.value = tokens.refresh;
    
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
  };

  const clearAuth = () => {
    user.value = null;
    accessToken.value = '';
    refreshToken.value = '';
    
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  const register = async (userData) => {
    isLoading.value = true;
    error.value = '';
    
    try {
      console.log('Register payload:', userData); // Debug
      const response = await api.post('/auth/register/', userData);
      console.log('Register response:', response.data); // Debug
      setAuth(response.data.user, response.data.tokens);
      return {}; // Return empty object on success
    } catch (err) {
      console.error('Register error:', err.response?.data); // Debug
      if (err.response?.status === 400 && err.response?.data) {
        // Prioritize field-specific errors
        if (err.response.data.first_name) {
          error.value = err.response.data.first_name[0] || 'Invalid first name';
        } else if (err.response.data.last_name) {
          error.value = err.response.data.last_name[0] || 'Invalid last name';
        } else if (err.response.data.email) {
          error.value = err.response.data.email[0] || 'This email is already registered';
        } else if (err.response.data.password) {
          error.value = err.response.data.password[0] || 'Invalid password';
        } else if (err.response.data.password_confirm) {
          error.value = err.response.data.password_confirm[0] || 'Passwords do not match';
        } else if (err.response.data.role) {
          error.value = err.response.data.role[0] || 'Invalid account type';
        } else {
          error.value = err.response.data.error || err.response.data.message || 'Registration failed';
        }
        return err.response.data; // Return errors for field-specific handling
      } else {
        error.value = 'An unexpected error occurred during registration';
        return { general: error.value };
      }
    } finally {
      isLoading.value = false;
    }
  };

  const login = async (credentials) => {
    isLoading.value = true;
    error.value = '';
    
    try {
      console.log('Login payload:', credentials); // Debug
      const response = await api.post('/auth/login/', credentials);
      console.log('Login response:', response.data); // Debug
      setAuth(response.data.user, response.data.tokens);
      return {};
    } catch (err) {
      console.error('Login error:', err.response?.data); // Debug
      if (err.response?.status === 401) {
        error.value = err.response.data.error || 'Invalid email or password';
      } else if (err.response?.status === 400) {
        error.value = err.response.data.error || 'Invalid input';
        return err.response.data;
      } else {
        error.value = 'An unexpected error occurred during login';
      }
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    clearAuth();
  };

  const changePassword = async (passwordData) => {
    try {
      const response = await api.post('/auth/password/change/', passwordData);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.error || 'Password change failed';
      throw err;
    }
  };

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    isAuthenticated,
    userRole,
    register,
    login,
    logout,
    changePassword,
    clearError: () => error.value = ''
  };
});