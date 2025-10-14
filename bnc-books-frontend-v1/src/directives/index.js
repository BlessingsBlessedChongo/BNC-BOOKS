// Global directives registration
import { vValidation } from '@/utils/validation'

// Click outside directive
export const vClickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}

// Focus directive
export const vFocus = {
  mounted(el) {
    el.focus()
  }
}

// Auto-resize textarea directive
export const vAutoResize = {
  mounted(el) {
    const resize = () => {
      el.style.height = 'auto'
      el.style.height = el.scrollHeight + 'px'
    }
    
    el.addEventListener('input', resize)
    resize() // Initial resize
    
    // Store resize function for cleanup
    el._autoResize = resize
  },
  
  unmounted(el) {
    if (el._autoResize) {
      el.removeEventListener('input', el._autoResize)
    }
  }
}

// Lazy load image directive
export const vLazyLoad = {
  mounted(el, binding) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target
          const src = img.getAttribute('data-src')
          
          if (src) {
            img.src = src
            img.removeAttribute('data-src')
          }
          
          observer.unobserve(img)
        }
      })
    }, {
      rootMargin: '50px 0px',
      threshold: 0.1
    })
    
    observer.observe(el)
    
    // Store observer for cleanup
    el._lazyLoadObserver = observer
  },
  
  unmounted(el) {
    if (el._lazyLoadObserver) {
      el._lazyLoadObserver.disconnect()
    }
  }
}

// Tooltip directive
export const vTooltip = {
  mounted(el, binding) {
    const tooltip = document.createElement('div')
    tooltip.className = 'tooltip hidden absolute z-50 px-2 py-1 text-sm text-white bg-gray-900 rounded shadow-lg whitespace-nowrap'
    tooltip.textContent = binding.value
    
    // Position tooltip
    const position = binding.arg || 'top'
    tooltip.classList.add(`tooltip-${position}`)
    
    el.style.position = 'relative'
    el.appendChild(tooltip)
    
    const showTooltip = () => {
      tooltip.classList.remove('hidden')
      
      // Position calculation
      const rect = el.getBoundingClientRect()
      const tooltipRect = tooltip.getBoundingClientRect()
      
      switch (position) {
        case 'top':
          tooltip.style.bottom = '100%'
          tooltip.style.left = '50%'
          tooltip.style.transform = 'translateX(-50%)'
          break
        case 'bottom':
          tooltip.style.top = '100%'
          tooltip.style.left = '50%'
          tooltip.style.transform = 'translateX(-50%)'
          break
        case 'left':
          tooltip.style.right = '100%'
          tooltip.style.top = '50%'
          tooltip.style.transform = 'translateY(-50%)'
          break
        case 'right':
          tooltip.style.left = '100%'
          tooltip.style.top = '50%'
          tooltip.style.transform = 'translateY(-50%)'
          break
      }
    }
    
    const hideTooltip = () => {
      tooltip.classList.add('hidden')
    }
    
    el.addEventListener('mouseenter', showTooltip)
    el.addEventListener('mouseleave', hideTooltip)
    el.addEventListener('focus', showTooltip)
    el.addEventListener('blur', hideTooltip)
    
    // Store event listeners for cleanup
    el._tooltipHandlers = { showTooltip, hideTooltip }
  },
  
  unmounted(el) {
    if (el._tooltipHandlers) {
      el.removeEventListener('mouseenter', el._tooltipHandlers.showTooltip)
      el.removeEventListener('mouseleave', el._tooltipHandlers.hideTooltip)
      el.removeEventListener('focus', el._tooltipHandlers.showTooltip)
      el.removeEventListener('blur', el._tooltipHandlers.hideTooltip)
    }
    
    const tooltip = el.querySelector('.tooltip')
    if (tooltip) {
      tooltip.remove()
    }
  }
}

// Copy to clipboard directive
export const vCopy = {
  mounted(el, binding) {
    const copyText = binding.value
    
    const copyToClipboard = async () => {
      try {
        await navigator.clipboard.writeText(copyText)
        
        // Show success feedback
        const originalText = el.textContent
        el.textContent = 'Copied!'
        el.classList.add('text-green-600')
        
        setTimeout(() => {
          el.textContent = originalText
          el.classList.remove('text-green-600')
        }, 2000)
      } catch (err) {
        console.error('Failed to copy text: ', err)
        
        // Show error feedback
        const originalText = el.textContent
        el.textContent = 'Copy failed'
        el.classList.add('text-red-600')
        
        setTimeout(() => {
          el.textContent = originalText
          el.classList.remove('text-red-600')
        }, 2000)
      }
    }
    
    el.style.cursor = 'pointer'
    el.addEventListener('click', copyToClipboard)
    
    // Store event listener for cleanup
    el._copyHandler = copyToClipboard
  },
  
  unmounted(el) {
    if (el._copyHandler) {
      el.removeEventListener('click', el._copyHandler)
    }
  }
}

// Permission directive (role-based)
export const vPermission = {
  beforeMount(el, binding) {
    const { roles } = binding.value
    const userRole = JSON.parse(localStorage.getItem('bnc_user_data'))?.role
    
    if (!roles.includes(userRole)) {
      el.style.display = 'none'
    }
  }
}

// Debounce directive
export const vDebounce = {
  mounted(el, binding) {
    const { event, handler, delay = 300 } = binding.value
    
    const debouncedHandler = debounce(handler, delay)
    
    el.addEventListener(event, debouncedHandler)
    
    // Store for cleanup
    el._debouncedHandler = debouncedHandler
  },
  
  unmounted(el, binding) {
    const { event } = binding.value
    if (el._debouncedHandler) {
      el.removeEventListener(event, el._debouncedHandler)
    }
  }
}

// Helper function for debounce
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Export all directives
export default {
  vClickOutside,
  vFocus,
  vAutoResize,
  vLazyLoad,
  vTooltip,
  vCopy,
  vPermission,
  vDebounce,
  vValidation
}