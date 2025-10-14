// Global error handler
export class AppError extends Error {
  constructor(message, code, details = null) {
    super(message)
    this.name = 'AppError'
    this.code = code
    this.details = details
    this.timestamp = new Date().toISOString()
  }
}

// Error codes
export const ERROR_CODES = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  AUTH_ERROR: 'AUTH_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  NOT_FOUND: 'NOT_FOUND',
  PERMISSION_DENIED: 'PERMISSION_DENIED',
  RATE_LIMITED: 'RATE_LIMITED',
  SERVER_ERROR: 'SERVER_ERROR'
}

// Error handler utility
export const handleError = (error, context = '') => {
  console.error(`[${context}]`, error)

  // Log to error reporting service
  if (import.meta.env.PROD) {
    logErrorToService(error, context)
  }

  // User-friendly error messages
  const userMessage = getUserFriendlyMessage(error)
  
  return {
    success: false,
    error: userMessage,
    code: error.code || ERROR_CODES.SERVER_ERROR,
    timestamp: error.timestamp || new Date().toISOString()
  }
}

const getUserFriendlyMessage = (error) => {
  if (error.code === ERROR_CODES.NETWORK_ERROR) {
    return 'Unable to connect to the server. Please check your internet connection.'
  }
  
  if (error.code === ERROR_CODES.AUTH_ERROR) {
    return 'Your session has expired. Please log in again.'
  }
  
  if (error.code === ERROR_CODES.VALIDATION_ERROR) {
    return 'Please check your input and try again.'
  }
  
  if (error.code === ERROR_CODES.NOT_FOUND) {
    return 'The requested resource was not found.'
  }
  
  if (error.code === ERROR_CODES.PERMISSION_DENIED) {
    return 'You do not have permission to perform this action.'
  }
  
  if (error.code === ERROR_CODES.RATE_LIMITED) {
    return 'Too many requests. Please try again later.'
  }
  
  return error.message || 'An unexpected error occurred. Please try again.'
}

const logErrorToService = (error, context) => {
  // Integrate with error reporting service (Sentry, LogRocket, etc.)
  const errorData = {
    context,
    message: error.message,
    stack: error.stack,
    code: error.code,
    url: window.location.href,
    userAgent: navigator.userAgent,
    timestamp: new Date().toISOString()
  }
  
  // Example: Send to error reporting endpoint
  fetch('/api/error-log', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(errorData)
  }).catch(() => {
    // Silent fail for error logging
  })
}

// Error boundary component data
export const withErrorHandling = (fn, context = '') => {
  return async (...args) => {
    try {
      return await fn(...args)
    } catch (error) {
      return handleError(error, context)
    }
  }
}