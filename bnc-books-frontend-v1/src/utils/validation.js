// Comprehensive form validation utilities
export const validationRules = {
  required: (value) => ({
    isValid: !!value && value.toString().trim().length > 0,
    message: 'This field is required'
  }),

  email: (value) => ({
    isValid: !value || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
    message: 'Please enter a valid email address'
  }),

  minLength: (min) => (value) => ({
    isValid: !value || value.length >= min,
    message: `Must be at least ${min} characters`
  }),

  maxLength: (max) => (value) => ({
    isValid: !value || value.length <= max,
    message: `Must be no more than ${max} characters`
  }),

  password: (value) => ({
    isValid: !value || /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/.test(value),
    message: 'Password must contain uppercase, lowercase, number, and special character'
  }),

  phone: (value) => ({
    isValid: !value || /^\+?[\d\s\-\(\)]{10,}$/.test(value),
    message: 'Please enter a valid phone number'
  }),

  zipCode: (value) => ({
    isValid: !value || /^\d{5}(-\d{4})?$/.test(value),
    message: 'Please enter a valid ZIP code'
  }),

  price: (value) => ({
    isValid: !value || /^\d+(\.\d{1,2})?$/.test(value) && parseFloat(value) >= 0,
    message: 'Please enter a valid price'
  }),

  isbn: (value) => ({
    isValid: !value || validateISBN(value),
    message: 'Please enter a valid ISBN'
  }),

  url: (value) => ({
    isValid: !value || /^https?:\/\/.+\..+/.test(value),
    message: 'Please enter a valid URL'
  }),

  numeric: (value) => ({
    isValid: !value || /^\d+$/.test(value),
    message: 'Must be a number'
  }),

  positive: (value) => ({
    isValid: !value || parseFloat(value) > 0,
    message: 'Must be a positive number'
  }),

  match: (fieldValue, fieldName) => (value) => ({
    isValid: !value || value === fieldValue,
    message: `Must match ${fieldName}`
  })
}

// ISBN validation
export const validateISBN = (isbn) => {
  isbn = isbn.replace(/[-\s]/g, '')
  
  if (isbn.length === 10) {
    return validateISBN10(isbn)
  } else if (isbn.length === 13) {
    return validateISBN13(isbn)
  }
  
  return false
}

const validateISBN10 = (isbn) => {
  let sum = 0
  for (let i = 0; i < 9; i++) {
    const digit = parseInt(isbn[i])
    if (isNaN(digit)) return false
    sum += digit * (10 - i)
  }
  
  const lastChar = isbn[9]
  if (lastChar === 'X') {
    sum += 10
  } else {
    const digit = parseInt(lastChar)
    if (isNaN(digit)) return false
    sum += digit
  }
  
  return sum % 11 === 0
}

const validateISBN13 = (isbn) => {
  let sum = 0
  for (let i = 0; i < 12; i++) {
    const digit = parseInt(isbn[i])
    if (isNaN(digit)) return false
    sum += digit * (i % 2 === 0 ? 1 : 3)
  }
  
  const checkDigit = parseInt(isbn[12])
  if (isNaN(checkDigit)) return false
  
  return (10 - (sum % 10)) % 10 === checkDigit
}

// Form validation composable
export const useFormValidation = (fields, rules) => {
  const errors = ref({})
  const touched = ref({})
  const isValid = ref(false)

  const validateField = (fieldName, value) => {
    const fieldRules = rules[fieldName] || []
    const fieldErrors = []

    for (const rule of fieldRules) {
      const result = typeof rule === 'function' ? rule(value) : rule
      if (!result.isValid) {
        fieldErrors.push(result.message)
      }
    }

    if (fieldErrors.length > 0) {
      errors.value[fieldName] = fieldErrors[0]
    } else {
      delete errors.value[fieldName]
    }

    validateForm()
  }

  const validateForm = () => {
    const hasErrors = Object.keys(errors.value).length > 0
    const allTouched = Object.keys(rules).every(field => touched.value[field])
    isValid.value = !hasErrors && allTouched
  }

  const markAsTouched = (fieldName) => {
    touched.value[fieldName] = true
    validateForm()
  }

  const resetValidation = () => {
    errors.value = {}
    touched.value = {}
    isValid.value = false
  }

  const validateAll = () => {
    Object.keys(rules).forEach(fieldName => {
      touched.value[fieldName] = true
      validateField(fieldName, fields[fieldName])
    })
    return isValid.value
  }

  return {
    errors,
    touched,
    isValid,
    validateField,
    markAsTouched,
    resetValidation,
    validateAll
  }
}

// Real-time validation directive
export const vValidation = {
  mounted(el, binding) {
    const { field, rules, update } = binding.value
    
    const validate = () => {
      const value = el.value
      let isValid = true
      let errorMessage = ''

      for (const rule of rules) {
        const result = typeof rule === 'function' ? rule(value) : rule
        if (!result.isValid) {
          isValid = false
          errorMessage = result.message
          break
        }
      }

      update(field, isValid, errorMessage)
    }

    el.addEventListener('input', validate)
    el.addEventListener('blur', validate)

    // Store the event listeners for cleanup
    el._validationHandlers = { validate }
  },

  unmounted(el) {
    if (el._validationHandlers) {
      el.removeEventListener('input', el._validationHandlers.validate)
      el.removeEventListener('blur', el._validationHandlers.validate)
    }
  }
}

// Credit card validation
export const validateCreditCard = (number) => {
  // Remove non-digit characters
  number = number.replace(/\D/g, '')
  
  // Luhn algorithm
  let sum = 0
  let isEven = false
  
  for (let i = number.length - 1; i >= 0; i--) {
    let digit = parseInt(number[i])
    
    if (isEven) {
      digit *= 2
      if (digit > 9) {
        digit -= 9
      }
    }
    
    sum += digit
    isEven = !isEven
  }
  
  return sum % 10 === 0
}

// Expiry date validation
export const validateExpiryDate = (month, year) => {
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  
  if (year < currentYear) return false
  if (year === currentYear && month < currentMonth) return false
  if (month < 1 || month > 12) return false
  
  return true
}

// CVV validation
export const validateCVV = (cvv) => {
  return /^\d{3,4}$/.test(cvv)
}

// Address validation
export const validateAddress = (address) => {
  const errors = {}
  
  if (!address.street_address?.trim()) {
    errors.street_address = 'Street address is required'
  }
  
  if (!address.city?.trim()) {
    errors.city = 'City is required'
  }
  
  if (!address.state?.trim()) {
    errors.state = 'State is required'
  }
  
  if (!address.zip_code?.trim()) {
    errors.zip_code = 'ZIP code is required'
  } else if (!validationRules.zipCode(address.zip_code).isValid) {
    errors.zip_code = 'Please enter a valid ZIP code'
  }
  
  if (!address.country?.trim()) {
    errors.country = 'Country is required'
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

export default {
  validationRules,
  validateISBN,
  useFormValidation,
  vValidation,
  validateCreditCard,
  validateExpiryDate,
  validateCVV,
  validateAddress
}