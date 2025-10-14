// Global error handling utilities
export class AppError extends Error {
  constructor(message, code, details = null) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.details = details;
  }
}

export const handleApiError = (error) => {
  console.error('API Error:', error);

  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        return new AppError('Validation Error', 'VALIDATION_ERROR', data);
      case 401:
        return new AppError('Authentication required', 'UNAUTHORIZED');
      case 403:
        return new AppError('Access denied', 'FORBIDDEN');
      case 404:
        return new AppError('Resource not found', 'NOT_FOUND');
      case 429:
        return new AppError('Too many requests', 'RATE_LIMITED');
      case 500:
        return new AppError('Server error', 'SERVER_ERROR');
      default:
        return new AppError('An error occurred', 'UNKNOWN_ERROR');
    }
  } else if (error.request) {
    // Request made but no response received
    return new AppError('Network error', 'NETWORK_ERROR');
  } else {
    // Something else happened
    return new AppError('An unexpected error occurred', 'UNKNOWN_ERROR');
  }
};

export const showErrorToast = (message, type = 'error') => {
  // This would integrate with a toast notification system
  console.log(`[${type.toUpperCase()}] ${message}`);
  // For now, we'll use alert but in production you'd use a proper toast system
  if (type === 'error') {
    alert(`Error: ${message}`);
  }
};

export const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/300x400?text=No+Image';
  event.target.onerror = null; // Prevent infinite loop
};