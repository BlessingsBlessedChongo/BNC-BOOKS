import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: { requiresAuth: false, hideNav: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: { requiresAuth: false, hideNav: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../views/user/OrdersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/orders/:id',
      name: 'order-details',
      component: () => import('../views/user/OrderDetailsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reviews',
      name: 'reviews',
      component: () => import('../views/user/ReviewsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/books',
      name: 'books',
      component: () => import('../views/books/BooksView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/books/:id',
      name: 'book-detail',
      component: () => import('../views/books/BookDetailView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('../views/cart/CartView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import('../views/checkout/CheckoutView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/order-confirmation',
      name: 'order-confirmation',
      component: () => import('../views/checkout/OrderConfirmationView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/seller',
      name: 'seller',
      component: () => import('../views/seller/SellerDashboard.vue'),
      meta: { requiresAuth: true, requiresRole: 'seller' }
    },
    {
      path: '/seller/books',
      name: 'seller-books',
      component: () => import('../views/seller/SellerBooksView.vue'),
      meta: { requiresAuth: true, requiresRole: 'seller' }
    },
    {
      path: '/seller/orders',
      name: 'seller-orders',
      component: () => import('../views/seller/SellerOrdersView.vue'),
      meta: { requiresAuth: true, requiresRole: 'seller' }
    },
    {
      path: '/seller/analytics',
      name: 'seller-analytics',
      component: () => import('../views/seller/SellerAnalyticsView.vue'),
      meta: { requiresAuth: true, requiresRole: 'seller' }
    },
    {
      path: '/seller/inventory',
      name: 'seller-inventory',
      component: () => import('../views/seller/SellerBooksView.vue'),
      meta: { requiresAuth: true, requiresRole: 'seller' }
    },
    {
      path: '/affiliate',
      name: 'affiliate',
      component: () => import('../views/affiliate/AffiliateDashboard.vue'),
      meta: { requiresAuth: true, requiresRole: 'affiliate' }
    },
    {
      path: '/affiliate/commissions',
      name: 'affiliate-commissions',
      component: () => import('../views/affiliate/AffiliateCommissionsView.vue'),
      meta: { requiresAuth: true, requiresRole: 'affiliate' }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue')
    },
    {
      path: '/affiliate/commissions',
      name: 'affiliate-commissions',
      component: () => import('../views/affiliate/AffiliateCommissionsView.vue'),
      meta: { requiresAuth: true, requiresRole: 'affiliate' }
    }
  ]
});

// Enhanced navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  // Check if authentication is required
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
    return;
  }
  
  // Check if user should be redirected away from auth pages when already authenticated
  if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    next('/dashboard');
    return;
  }
  
  // Check role-based access
  if (to.meta.requiresRole && authStore.userRole !== to.meta.requiresRole) {
    next('/dashboard');
    return;
  }
  
  next();
});

export default router;