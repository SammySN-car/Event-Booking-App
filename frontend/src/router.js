import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Signup from '@/views/Signup.vue'
import OrganizerDashboard from '@/views/OrganizerDashboard.vue'
import UserDashboard from '@/views/UserDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Signup
    },
    {
      path: '/admin',
      name: 'organizer_dashboard',
      component: OrganizerDashboard,
      meta: { requiresAuth: true, role: 'organizer' }
    },
    {
      path: '/dashboard',
      name: 'user_dashboard',
      component: UserDashboard,
      meta: { requiresAuth: true, role: 'user' }
    }
  ]
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  let role = localStorage.getItem('role')

  if (role && role !== 'organizer' && role !== 'user') {
    role = null
  }

  if (to.meta.requiresAuth) {
    if (!token || !role) {
      next({ name: 'login' })
    } else if (to.meta.role && to.meta.role !== role) {
      if (role === 'organizer' && to.name !== 'organizer_dashboard') {
        next({ name: 'organizer_dashboard' })
      } else if (role === 'user' && to.name !== 'user_dashboard') {
        next({ name: 'user_dashboard' })
      } else {
        next()
      }
    } else {
      next()
    }
  } else {
    if (token && role && (to.name === 'login' || to.name === 'register')) {
      if (role === 'organizer' && to.name !== 'organizer_dashboard') {
        next({ name: 'organizer_dashboard' })
      } else if (role === 'user' && to.name !== 'user_dashboard') {
        next({ name: 'user_dashboard' })
      } else {
        next()
      }
    } else {
      next()
    }
  }
})

export default router
