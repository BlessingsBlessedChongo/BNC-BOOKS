// Performance optimization utilities
import { ref, onMounted, onUnmounted } from 'vue'

// Image lazy loading
export const useLazyLoad = (options = {}) => {
  const { root = null, rootMargin = '0px', threshold = 0.1 } = options
  const observer = ref(null)
  const elements = ref(new Set())

  const init = () => {
    observer.value = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target
          const src = img.getAttribute('data-src')
          if (src) {
            img.src = src
            img.removeAttribute('data-src')
          }
          observer.value.unobserve(img)
          elements.value.delete(img)
        }
      })
    }, { root, rootMargin, threshold })
  }

  const observe = (element) => {
    if (element && element.getAttribute('data-src')) {
      elements.value.add(element)
      observer.value.observe(element)
    }
  }

  const unobserve = (element) => {
    if (element) {
      observer.value.unobserve(element)
      elements.value.delete(element)
    }
  }

  const disconnect = () => {
    if (observer.value) {
      observer.value.disconnect()
      elements.value.clear()
    }
  }

  onMounted(init)
  onUnmounted(disconnect)

  return {
    observe,
    unobserve,
    disconnect
  }
}

// API response caching
export class ApiCache {
  constructor(options = {}) {
    this.maxAge = options.maxAge || 5 * 60 * 1000 // 5 minutes default
    this.maxSize = options.maxSize || 100 // max cache entries
    this.cache = new Map()
  }

  set(key, data) {
    // Remove oldest entry if cache is full
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value
      this.cache.delete(firstKey)
    }

    this.cache.set(key, {
      data,
      timestamp: Date.now()
    })
  }

  get(key) {
    const entry = this.cache.get(key)
    if (!entry) return null

    // Check if cache entry is expired
    if (Date.now() - entry.timestamp > this.maxAge) {
      this.cache.delete(key)
      return null
    }

    return entry.data
  }

  delete(key) {
    this.cache.delete(key)
  }

  clear() {
    this.cache.clear()
  }

  size() {
    return this.cache.size
  }
}

// Global cache instance
export const apiCache = new ApiCache({
  maxAge: 10 * 60 * 1000, // 10 minutes
  maxSize: 200
})

// Debounce function for search and filter inputs
export const debounce = (func, wait, immediate = false) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      timeout = null
      if (!immediate) func(...args)
    }
    const callNow = immediate && !timeout
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
    if (callNow) func(...args)
  }
}

// Throttle function for scroll and resize events
export const throttle = (func, limit) => {
  let inThrottle
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

// Memory management for large lists
export const useVirtualScroll = (items, itemHeight, containerHeight, overscan = 3) => {
  const scrollTop = ref(0)
  
  const visibleRange = computed(() => {
    const startIndex = Math.max(0, Math.floor(scrollTop.value / itemHeight) - overscan)
    const endIndex = Math.min(
      items.value.length - 1,
      Math.floor((scrollTop.value + containerHeight) / itemHeight) + overscan
    )
    return { startIndex, endIndex }
  })

  const visibleItems = computed(() => {
    const { startIndex, endIndex } = visibleRange.value
    return items.value.slice(startIndex, endIndex + 1).map((item, index) => ({
      ...item,
      originalIndex: startIndex + index,
      offset: (startIndex + index) * itemHeight
    }))
  })

  const totalHeight = computed(() => items.value.length * itemHeight)

  const onScroll = (event) => {
    scrollTop.value = event.target.scrollTop
  }

  return {
    visibleItems,
    totalHeight,
    onScroll
  }
}

// Performance monitoring
export const usePerformanceMonitor = () => {
  const metrics = ref({
    fcp: null, // First Contentful Paint
    lcp: null, // Largest Contentful Paint
    fid: null, // First Input Delay
    cls: null  // Cumulative Layout Shift
  })

  const observe = () => {
    if ('PerformanceObserver' in window) {
      // Observe Largest Contentful Paint
      const lcpObserver = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries()
        const lastEntry = entries[entries.length - 1]
        metrics.value.lcp = lastEntry.renderTime || lastEntry.loadTime
      })
      lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true })

      // Observe Cumulative Layout Shift
      const clsObserver = new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
          if (!entry.hadRecentInput) {
            metrics.value.cls += entry.value
          }
        }
      })
      clsObserver.observe({ type: 'layout-shift', buffered: true })

      // Observe First Input Delay
      const fidObserver = new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
          metrics.value.fid = entry.processingStart - entry.startTime
        }
      })
      fidObserver.observe({ type: 'first-input', buffered: true })
    }
  }

  const getMetrics = () => metrics.value

  return {
    observe,
    getMetrics
  }
}

// Bundle splitting helper
export const lazyLoadComponent = (componentLoader) => {
  return defineAsyncComponent({
    loader: componentLoader,
    loadingComponent: {
      template: '<div class="animate-pulse bg-gray-200 rounded h-32"></div>'
    },
    errorComponent: {
      template: '<div class="text-red-600">Failed to load component</div>'
    },
    delay: 200,
    timeout: 5000
  })
}

// Memory leak prevention
export const useCleanup = () => {
  const cleanupCallbacks = []

  const addCleanup = (callback) => {
    cleanupCallbacks.push(callback)
  }

  const cleanup = () => {
    cleanupCallbacks.forEach(callback => callback())
    cleanupCallbacks.length = 0
  }

  onUnmounted(cleanup)

  return {
    addCleanup,
    cleanup
  }
}