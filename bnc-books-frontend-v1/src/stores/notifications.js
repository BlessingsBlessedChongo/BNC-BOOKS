import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useNotificationStore = defineStore('notifications', () => {
  const notifications = ref([])
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    currentPage: 1,
    totalPages: 1,
    totalCount: 0,
    pageSize: 20
  })
  const unreadCount = ref(0)
  const websocket = ref(null)
  const isConnected = ref(false)

  // Computed
  const unreadNotifications = computed(() => 
    notifications.value.filter(n => !n.read)
  )

  const notificationsByType = computed(() => ({
    orders: notifications.value.filter(n => n.type?.includes('order')),
    reviews: notifications.value.filter(n => n.type?.includes('review')),
    commissions: notifications.value.filter(n => n.type?.includes('commission')),
    system: notifications.value.filter(n => n.type === 'system' || !n.type)
  }))

  const hasMore = computed(() => 
    pagination.value.currentPage < pagination.value.totalPages
  )

  // Actions
  const fetchNotifications = async (page = 1) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/notifications/', {
        params: {
          page,
          page_size: pagination.value.pageSize
        }
      })
      
      if (page === 1) {
        notifications.value = response.data.results
      } else {
        notifications.value = [...notifications.value, ...response.data.results]
      }
      
      pagination.value = {
        currentPage: response.data.current_page,
        totalPages: response.data.total_pages,
        totalCount: response.data.total_count,
        pageSize: response.data.page_size
      }
      
      // Update unread count
      unreadCount.value = response.data.unread_count || 
        notifications.value.filter(n => !n.read).length
      
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch notifications'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const loadMoreNotifications = async () => {
    if (!hasMore.value) return
    
    const nextPage = pagination.value.currentPage + 1
    return await fetchNotifications(nextPage)
  }

  const markAsRead = async (notificationId) => {
    try {
      await api.patch(`/notifications/${notificationId}/read/`)
      
      // Update local state
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification) {
        notification.read = true
        unreadCount.value = Math.max(0, unreadCount.value - 1)
      }
      
      return { success: true }
    } catch (err) {
      console.error('Failed to mark notification as read:', err)
      return { success: false, error: err.response?.data?.message }
    }
  }

  const markAsUnread = async (notificationId) => {
    try {
      await api.patch(`/notifications/${notificationId}/unread/`)
      
      // Update local state
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification) {
        notification.read = false
        unreadCount.value += 1
      }
      
      return { success: true }
    } catch (err) {
      console.error('Failed to mark notification as unread:', err)
      return { success: false, error: err.response?.data?.message }
    }
  }

  const markAllAsRead = async () => {
    try {
      await api.post('/notifications/mark-all-read/')
      
      // Update local state
      notifications.value.forEach(notification => {
        notification.read = true
      })
      unreadCount.value = 0
      
      return { success: true }
    } catch (err) {
      console.error('Failed to mark all notifications as read:', err)
      return { success: false, error: err.response?.data?.message }
    }
  }

  const deleteNotification = async (notificationId) => {
    try {
      await api.delete(`/notifications/${notificationId}/`)
      
      // Remove from local state
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification && !notification.read) {
        unreadCount.value = Math.max(0, unreadCount.value - 1)
      }
      notifications.value = notifications.value.filter(n => n.id !== notificationId)
      
      return { success: true }
    } catch (err) {
      console.error('Failed to delete notification:', err)
      return { success: false, error: err.response?.data?.message }
    }
  }

  const addNotification = (notification) => {
    // Add to beginning of list
    notifications.value.unshift(notification)
    
    if (!notification.read) {
      unreadCount.value += 1
    }
    
    // Keep only latest 100 notifications in memory
    if (notifications.value.length > 100) {
      notifications.value = notifications.value.slice(0, 100)
    }
  }

  // WebSocket connection for real-time notifications
  const connectWebSocket = () => {
    if (websocket.value || !isConnected.value) return

    try {
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${wsProtocol}//${window.location.host}/ws/notifications/`
      
      websocket.value = new WebSocket(wsUrl)
      
      websocket.value.onopen = () => {
        console.log('WebSocket connected for notifications')
        isConnected.value = true
      }
      
      websocket.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          if (data.type === 'notification') {
            addNotification(data.notification)
          }
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err)
        }
      }
      
      websocket.value.onclose = () => {
        console.log('WebSocket disconnected')
        isConnected.value = false
        websocket.value = null
        
        // Attempt reconnect after 5 seconds
        setTimeout(() => {
          connectWebSocket()
        }, 5000)
      }
      
      websocket.value.onerror = (error) => {
        console.error('WebSocket error:', error)
        isConnected.value = false
      }
    } catch (err) {
      console.error('Failed to connect WebSocket:', err)
    }
  }

  const disconnectWebSocket = () => {
    if (websocket.value) {
      websocket.value.close()
      websocket.value = null
      isConnected.value = false
    }
  }

  // Initialize WebSocket when store is created
  const initialize = () => {
    connectWebSocket()
  }

  return {
    // State
    notifications,
    loading,
    error,
    pagination,
    unreadCount,
    isConnected,
    
    // Computed
    unreadNotifications,
    notificationsByType,
    hasMore,
    
    // Actions
    fetchNotifications,
    loadMoreNotifications,
    markAsRead,
    markAsUnread,
    markAllAsRead,
    deleteNotification,
    addNotification,
    connectWebSocket,
    disconnectWebSocket,
    initialize
  }
})

// Initialize WebSocket connection when store is created
const notificationStore = useNotificationStore()
notificationStore.initialize()