import { ref } from 'vue';

const notifications = ref([]);

export const useNotifications = () => {
  const showNotification = (notification) => {
    const id = Date.now();
    const newNotification = {
      id,
      type: notification.type || 'info',
      title: notification.title,
      message: notification.message,
      show: true,
      duration: notification.duration || 5000
    };

    notifications.value.push(newNotification);

    // Auto remove after duration
    if (newNotification.duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, newNotification.duration);
    }

    return id;
  };

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) {
      notifications.value.splice(index, 1);
    }
  };

  const clearAll = () => {
    notifications.value = [];
  };

  return {
    notifications,
    showNotification,
    removeNotification,
    clearAll
  };
};