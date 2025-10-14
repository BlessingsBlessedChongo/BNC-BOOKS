import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/books',
    name: 'Books',
    component: () => import('@/views/books/BookList.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Login.vue') // Use same component for demo
  },
  {
    path: '/wishlist',
    name: 'Wishlist',
    component: () => import('@/views/user/Wishlist.vue')
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: () => import('@/views/Notifications.vue')
  },
  {
    path: '/404',
    name: 'NotFound',
    component: {
      template: '<div class="p-8 text-center"><h1 class="text-2xl font-bold">Page Not Found</h1></div>'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router