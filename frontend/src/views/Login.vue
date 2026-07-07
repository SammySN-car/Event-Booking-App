<template>
  <div class="row justify-content-center align-items-center" style="min-height: 80vh">
    <div class="col-md-5">
      <div class="glass-card p-5">
        <div class="text-center mb-4">
          <h2 class="fw-bold">Welcome Back</h2>
          <p class="text-muted">Sign in to your Event Booking account</p>
        </div>
        
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label text-secondary small fw-bold">Email address</label>
            <input type="email" v-model="email" class="form-control form-control-premium py-2" required>
          </div>
          <div class="mb-4">
            <label class="form-label text-secondary small fw-bold">Password</label>
            <input type="password" v-model="password" class="form-control form-control-premium py-2" required>
          </div>
          
          <div class="d-grid mb-3">
            <button type="submit" class="btn btn-premium py-2 fw-bold" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              Sign In
            </button>
          </div>
          
          <div v-if="error" class="alert alert-danger py-2 text-center small mb-0 rounded">{{ error }}</div>
        </form>
        
        <div class="text-center mt-4 pt-3 border-top border-secondary opacity-50">
          <p class="small text-muted mb-0">Don't have an account? <router-link to="/signup" class="text-primary fw-bold text-decoration-none">Sign up</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/client'
import { setAuth } from '../api/auth'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    const res = await api.post('/api/login', { email: email.value, password: password.value })
    const { token, user } = res.data.data
    setAuth(token, user)
    router.push(user.role === 'organizer' ? '/organizer' : '/dashboard')
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to login'
  } finally {
    loading.value = false
  }
}
</script>