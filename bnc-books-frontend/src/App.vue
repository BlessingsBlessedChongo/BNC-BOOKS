<template>
  <div id="app">
    <router-view />
    
    <!-- Global Notifications -->
    <div class="fixed inset-0 z-50 pointer-events-none">
      <NotificationToast
        v-for="notification in notifications"
        :key="notification.id"
        :notification="notification"
        @close="removeNotification(notification.id)"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import NotificationToast from './components/common/NotificationToast.vue';
import { useNotifications } from './composables/useNotifications';

const { notifications, removeNotification } = useNotifications();
</script>