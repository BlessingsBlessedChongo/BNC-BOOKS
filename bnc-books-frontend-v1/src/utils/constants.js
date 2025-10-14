// Application-wide constants

// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  TIMEOUT: 30000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000
}

// User Roles
export const USER_ROLES = {
  BUYER: 'buyer',
  SELLER: 'seller',
  AFFILIATE: 'affiliate',
  ADMIN: 'admin'
}

// Book Conditions
export const BOOK_CONDITIONS = {
  NEW: 'new',
  LIKE_NEW: 'like_new',
  VERY_GOOD: 'very_good',
  GOOD: 'good',
  ACCEPTABLE: 'acceptable'
}

export const BOOK_CONDITION_LABELS = {
  [BOOK_CONDITIONS.NEW]: 'New',
  [BOOK_CONDITIONS.LIKE_NEW]: 'Like New',
  [BOOK_CONDITIONS.VERY_GOOD]: 'Very Good',
  [BOOK_CONDITIONS.GOOD]: 'Good',
  [BOOK_CONDITIONS.ACCEPTABLE]: 'Acceptable'
}

// Book Formats
export const BOOK_FORMATS = {
  HARDCOVER: 'hardcover',
  PAPERBACK: 'paperback',
  EBOOK: 'ebook',
  AUDIOBOOK: 'audiobook'
}

export const BOOK_FORMAT_LABELS = {
  [BOOK_FORMATS.HARDCOVER]: 'Hardcover',
  [BOOK_FORMATS.PAPERBACK]: 'Paperback',
  [BOOK_FORMATS.EBOOK]: 'E-book',
  [BOOK_FORMATS.AUDIOBOOK]: 'Audiobook'
}

// Order Statuses
export const ORDER_STATUS = {
  PENDING: 'pending',
  CONFIRMED: 'confirmed',
  PROCESSING: 'processing',
  SHIPPED: 'shipped',
  DELIVERED: 'delivered',
  CANCELLED: 'cancelled',
  REFUNDED: 'refunded'
}

export const ORDER_STATUS_LABELS = {
  [ORDER_STATUS.PENDING]: 'Pending',
  [ORDER_STATUS.CONFIRMED]: 'Confirmed',
  [ORDER_STATUS.PROCESSING]: 'Processing',
  [ORDER_STATUS.SHIPPED]: 'Shipped',
  [ORDER_STATUS.DELIVERED]: 'Delivered',
  [ORDER_STATUS.CANCELLED]: 'Cancelled',
  [ORDER_STATUS.REFUNDED]: 'Refunded'
}

// Payment Methods
export const PAYMENT_METHODS = {
  CREDIT_CARD: 'credit_card',
  PAYPAL: 'paypal',
  STRIPE: 'stripe',
  BANK_TRANSFER: 'bank_transfer'
}

export const PAYMENT_METHOD_LABELS = {
  [PAYMENT_METHODS.CREDIT_CARD]: 'Credit Card',
  [PAYMENT_METHODS.PAYPAL]: 'PayPal',
  [PAYMENT_METHODS.STRIPE]: 'Stripe',
  [PAYMENT_METHODS.BANK_TRANSFER]: 'Bank Transfer'
}

// Notification Types
export const NOTIFICATION_TYPES = {
  ORDER_PLACED: 'order_placed',
  ORDER_SHIPPED: 'order_shipped',
  ORDER_DELIVERED: 'order_delivered',
  ORDER_CANCELLED: 'order_cancelled',
  REVIEW_RECEIVED: 'review_received',
  REVIEW_REPLIED: 'review_replied',
  COMMISSION_EARNED: 'commission_earned',
  PAYOUT_PROCESSED: 'payout_processed',
  PRICE_DROP: 'price_drop',
  BACK_IN_STOCK: 'back_in_stock',
  SYSTEM: 'system'
}

// Commission Status
export const COMMISSION_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  PAID: 'paid',
  CANCELLED: 'cancelled'
}

// Review Status
export const REVIEW_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected'
}

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 12,
  MAX_PAGE_SIZE: 100,
  PAGE_SIZES: [12, 24, 48, 96]
}

// File Upload
export const FILE_UPLOAD = {
  MAX_FILE_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/webp', 'image/gif'],
  ALLOWED_DOCUMENT_TYPES: ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
}

// Validation Rules
export const VALIDATION = {
  PASSWORD: {
    MIN_LENGTH: 8,
    REQUIRE_UPPERCASE: true,
    REQUIRE_LOWERCASE: true,
    REQUIRE_NUMBER: true,
    REQUIRE_SPECIAL_CHAR: true
  },
  NAME: {
    MIN_LENGTH: 2,
    MAX_LENGTH: 30
  },
  EMAIL: {
    MAX_LENGTH: 255
  },
  BOOK: {
    TITLE_MAX_LENGTH: 200,
    AUTHOR_MAX_LENGTH: 100,
    DESCRIPTION_MAX_LENGTH: 2000,
    ISBN_LENGTHS: [10, 13]
  }
}

// Countries (commonly used in dropdowns)
export const COUNTRIES = [
  { code: 'US', name: 'United States' },
  { code: 'CA', name: 'Canada' },
  { code: 'GB', name: 'United Kingdom' },
  { code: 'AU', name: 'Australia' },
  { code: 'DE', name: 'Germany' },
  { code: 'FR', name: 'France' },
  { code: 'JP', name: 'Japan' },
  { code: 'IN', name: 'India' },
  { code: 'BR', name: 'Brazil' },
  { code: 'MX', name: 'Mexico' }
]

// US States
export const US_STATES = [
  { code: 'AL', name: 'Alabama' },
  { code: 'AK', name: 'Alaska' },
  { code: 'AZ', name: 'Arizona' },
  { code: 'AR', name: 'Arkansas' },
  { code: 'CA', name: 'California' },
  { code: 'CO', name: 'Colorado' },
  { code: 'CT', name: 'Connecticut' },
  { code: 'DE', name: 'Delaware' },
  { code: 'FL', name: 'Florida' },
  { code: 'GA', name: 'Georgia' },
  { code: 'HI', name: 'Hawaii' },
  { code: 'ID', name: 'Idaho' },
  { code: 'IL', name: 'Illinois' },
  { code: 'IN', name: 'Indiana' },
  { code: 'IA', name: 'Iowa' },
  { code: 'KS', name: 'Kansas' },
  { code: 'KY', name: 'Kentucky' },
  { code: 'LA', name: 'Louisiana' },
  { code: 'ME', name: 'Maine' },
  { code: 'MD', name: 'Maryland' },
  { code: 'MA', name: 'Massachusetts' },
  { code: 'MI', name: 'Michigan' },
  { code: 'MN', name: 'Minnesota' },
  { code: 'MS', name: 'Mississippi' },
  { code: 'MO', name: 'Missouri' },
  { code: 'MT', name: 'Montana' },
  { code: 'NE', name: 'Nebraska' },
  { code: 'NV', name: 'Nevada' },
  { code: 'NH', name: 'New Hampshire' },
  { code: 'NJ', name: 'New Jersey' },
  { code: 'NM', name: 'New Mexico' },
  { code: 'NY', name: 'New York' },
  { code: 'NC', name: 'North Carolina' },
  { code: 'ND', name: 'North Dakota' },
  { code: 'OH', name: 'Ohio' },
  { code: 'OK', name: 'Oklahoma' },
  { code: 'OR', name: 'Oregon' },
  { code: 'PA', name: 'Pennsylvania' },
  { code: 'RI', name: 'Rhode Island' },
  { code: 'SC', name: 'South Carolina' },
  { code: 'SD', name: 'South Dakota' },
  { code: 'TN', name: 'Tennessee' },
  { code: 'TX', name: 'Texas' },
  { code: 'UT', name: 'Utah' },
  { code: 'VT', name: 'Vermont' },
  { code: 'VA', name: 'Virginia' },
  { code: 'WA', name: 'Washington' },
  { code: 'WV', name: 'West Virginia' },
  { code: 'WI', name: 'Wisconsin' },
  { code: 'WY', name: 'Wyoming' }
]

// Languages
export const LANGUAGES = [
  'English',
  'Spanish',
  'French',
  'German',
  'Chinese',
  'Japanese',
  'Korean',
  'Russian',
  'Arabic',
  'Portuguese',
  'Italian',
  'Dutch',
  'Hindi',
  'Bengali'
]

// Categories
export const CATEGORIES = [
  'Fiction',
  'Non-Fiction',
  'Science',
  'Technology',
  'Business',
  'Self-Help',
  'Biography',
  'History',
  'Children',
  'Young Adult',
  'Romance',
  'Mystery',
  'Thriller',
  'Science Fiction',
  'Fantasy',
  'Horror',
  'Poetry',
  'Drama',
  'Comics',
  'Cookbooks',
  'Travel',
  'Religion',
  'Philosophy',
  'Art',
  'Music'
]

// Genres
export const GENRES = [
  'Action',
  'Adventure',
  'Classic',
  'Contemporary',
  'Crime',
  'Dystopian',
  'Fantasy',
  'Historical',
  'Horror',
  'Humor',
  'Literary',
  'Magical Realism',
  'Mystery',
  'Paranormal',
  'Philosophical',
  'Political',
  'Romance',
  'Satire',
  'Science Fiction',
  'Short Story',
  'Suspense',
  'Thriller',
  'Urban',
  'Western',
  'Young Adult'
]

// Theme Colors
export const THEME_COLORS = {
  primary: {
    50: '#f0fdfa',
    100: '#ccfbf1',
    200: '#99f6e4',
    300: '#5eead4',
    400: '#2dd4bf',
    500: '#14b8a6',
    600: '#0d9488',
    700: '#0f766e',
    800: '#115e59',
    900: '#134e4a'
  },
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827'
  }
}

// Breakpoints
export const BREAKPOINTS = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px'
}

// Local Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'bnc_auth_token',
  REFRESH_TOKEN: 'bnc_refresh_token',
  USER_DATA: 'bnc_user_data',
  CART: 'bnc_cart',
  WISHLIST: 'bnc_wishlist',
  RECENT_SEARCHES: 'bnc_recent_searches',
  NOTIFICATION_SETTINGS: 'bnc_notification_settings'
}

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  SERVER_ERROR: 'Server error. Please try again later.',
  UNAUTHORIZED: 'Please log in to continue.',
  FORBIDDEN: 'You do not have permission to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  UNKNOWN_ERROR: 'An unexpected error occurred.'
}

// Success Messages
export const SUCCESS_MESSAGES = {
  PROFILE_UPDATED: 'Profile updated successfully.',
  PASSWORD_CHANGED: 'Password changed successfully.',
  BOOK_ADDED: 'Book added successfully.',
  ORDER_PLACED: 'Order placed successfully.',
  REVIEW_SUBMITTED: 'Review submitted successfully.',
  ITEM_ADDED_TO_CART: 'Item added to cart.',
  ITEM_ADDED_TO_WISHLIST: 'Item added to wishlist.'
}

export default {
  API_CONFIG,
  USER_ROLES,
  BOOK_CONDITIONS,
  BOOK_CONDITION_LABELS,
  BOOK_FORMATS,
  BOOK_FORMAT_LABELS,
  ORDER_STATUS,
  ORDER_STATUS_LABELS,
  PAYMENT_METHODS,
  PAYMENT_METHOD_LABELS,
  NOTIFICATION_TYPES,
  COMMISSION_STATUS,
  REVIEW_STATUS,
  PAGINATION,
  FILE_UPLOAD,
  VALIDATION,
  COUNTRIES,
  US_STATES,
  LANGUAGES,
  CATEGORIES,
  GENRES,
  THEME_COLORS,
  BREAKPOINTS,
  STORAGE_KEYS,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES
}