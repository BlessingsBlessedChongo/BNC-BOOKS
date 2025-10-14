// Service Worker for offline functionality
const CACHE_NAME = 'bnc-books-v1'
const API_CACHE_NAME = 'bnc-books-api-v1'

const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/images/logo.png',
  '/images/placeholder-book.jpg'
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  )
})

self.addEventListener('fetch', (event) => {
  // API requests - cache with network-first strategy
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Cache successful API responses
          if (response.status === 200) {
            const responseClone = response.clone()
            caches.open(API_CACHE_NAME)
              .then(cache => cache.put(event.request, responseClone))
          }
          return response
        })
        .catch(() => {
          // Fallback to cache when offline
          return caches.match(event.request)
        })
    )
  } else {
    // Static assets - cache-first strategy
    event.respondWith(
      caches.match(event.request)
        .then(response => response || fetch(event.request))
    )
  }
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
            return caches.delete(cacheName)
          }
        })
      )
    })
  )
})