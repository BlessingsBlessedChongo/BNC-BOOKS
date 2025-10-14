import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import directives from '@/directives'

const app = createApp(App)
const pinia = createPinia()

// Register global directives
Object.keys(directives).forEach(key => {
  app.directive(key.replace('v', '').toLowerCase(), directives[key])
})

app.use(pinia)
app.use(router)

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue error:', err)
  console.error('Component:', instance)
  console.error('Info:', info)
  
  // Send to error reporting service
  if (window.Sentry) {
    window.Sentry.captureException(err, { extra: { component: instance, info } })
  }
}

// Global warn handler
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Vue warning:', msg)
  console.warn('Component:', instance)
  console.warn('Trace:', trace)
}

app.mount('#app')