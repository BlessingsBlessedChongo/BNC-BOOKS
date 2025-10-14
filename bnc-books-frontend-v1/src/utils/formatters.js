// Comprehensive formatting utilities
import { ref, computed } from 'vue'

// Price formatting
export const formatPrice = (price, currency = 'USD', locale = 'en-US') => {
  if (price == null || isNaN(price)) return ''
  
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(price)
}

// Percentage formatting
export const formatPercentage = (value, decimals = 1) => {
  if (value == null || isNaN(value)) return ''
  
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value / 100)
}

// Date formatting
export const formatDate = (date, options = {}) => {
  if (!date) return ''
  
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }
  
  const mergedOptions = { ...defaultOptions, ...options }
  
  return new Intl.DateTimeFormat('en-US', mergedOptions).format(new Date(date))
}

// Relative time formatting (e.g., "2 hours ago")
export const formatRelativeTime = (date) => {
  if (!date) return ''
  
  const now = new Date()
  const target = new Date(date)
  const diffMs = now - target
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  const diffWeeks = Math.floor(diffDays / 7)
  const diffMonths = Math.floor(diffDays / 30)
  const diffYears = Math.floor(diffDays / 365)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`
  if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`
  if (diffWeeks < 4) return `${diffWeeks} week${diffWeeks !== 1 ? 's' : ''} ago`
  if (diffMonths < 12) return `${diffMonths} month${diffMonths !== 1 ? 's' : ''} ago`
  return `${diffYears} year${diffYears !== 1 ? 's' : ''} ago`
}

// File size formatting
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Text truncation
export const truncateText = (text, maxLength, suffix = '...') => {
  if (!text || text.length <= maxLength) return text
  return text.substring(0, maxLength - suffix.length) + suffix
}

// ISBN formatting
export const formatISBN = (isbn) => {
  if (!isbn) return ''
  
  // Remove any existing formatting
  const cleanIsbn = isbn.replace(/[-\s]/g, '')
  
  if (cleanIsbn.length === 10) {
    return cleanIsbn.replace(/^(\d{1})(\d{3})(\d{5})(\d{1})$/, '$1-$2-$3-$4')
  } else if (cleanIsbn.length === 13) {
    return cleanIsbn.replace(/^(\d{3})(\d{1})(\d{3})(\d{5})(\d{1})$/, '$1-$2-$3-$4-$5')
  }
  
  return isbn
}

// Phone number formatting
export const formatPhoneNumber = (phone) => {
  if (!phone) return ''
  
  // Remove non-digit characters
  const cleaned = phone.replace(/\D/g, '')
  
  // US phone number format
  if (cleaned.length === 10) {
    return cleaned.replace(/^(\d{3})(\d{3})(\d{4})$/, '($1) $2-$3')
  } else if (cleaned.length === 11 && cleaned[0] === '1') {
    return cleaned.replace(/^1(\d{3})(\d{3})(\d{4})$/, '+1 ($1) $2-$3')
  }
  
  return phone
}

// Number formatting with commas
export const formatNumber = (number, decimals = 0) => {
  if (number == null || isNaN(number)) return ''
  
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(number)
}

// Rating formatting (stars)
export const formatRating = (rating, maxStars = 5) => {
  if (rating == null || isNaN(rating)) return ''
  
  const fullStars = Math.floor(rating)
  const hasHalfStar = rating % 1 >= 0.5
  const emptyStars = maxStars - fullStars - (hasHalfStar ? 1 : 0)
  
  return {
    fullStars,
    hasHalfStar,
    emptyStars,
    display: `${rating.toFixed(1)}/5.0`
  }
}

// Social media number formatting (e.g., 1.2K, 3.5M)
export const formatSocialNumber = (number) => {
  if (number < 1000) return number.toString()
  if (number < 1000000) return (number / 1000).toFixed(1) + 'K'
  if (number < 1000000000) return (number / 1000000).toFixed(1) + 'M'
  return (number / 1000000000).toFixed(1) + 'B'
}

// Duration formatting (e.g., "2h 30m")
export const formatDuration = (minutes) => {
  if (!minutes || isNaN(minutes)) return ''
  
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  
  if (hours === 0) return `${mins}m`
  if (mins === 0) return `${hours}h`
  return `${hours}h ${mins}m`
}

// Composable for reactive formatting
export const useFormatters = () => {
  const price = (value, currency = 'USD') => 
    computed(() => formatPrice(value, currency))
  
  const date = (value, options = {}) => 
    computed(() => formatDate(value, options))
  
  const relativeTime = (value) => 
    computed(() => formatRelativeTime(value))
  
  const number = (value, decimals = 0) => 
    computed(() => formatNumber(value, decimals))
  
  return {
    price,
    date,
    relativeTime,
    number
  }
}

// Export all formatters
export default {
  formatPrice,
  formatPercentage,
  formatDate,
  formatRelativeTime,
  formatFileSize,
  truncateText,
  formatISBN,
  formatPhoneNumber,
  formatNumber,
  formatRating,
  formatSocialNumber,
  formatDuration,
  useFormatters
}