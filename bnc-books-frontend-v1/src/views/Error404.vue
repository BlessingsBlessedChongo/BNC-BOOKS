<template>
  <EmptyState
    type="error"
    title="Page Not Found"
    description="The page you are looking for doesn't exist or has been moved."
    :show-action="true"
    action-button-text="Go Home"
    @action="goHome"
  />
</template>

<script setup>
import { useRouter } from 'vue-router'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>