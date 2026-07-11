<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const form = ref({ email_id: '', password: '' })
const message = ref('')
const isSuccess = ref(false)
const router = useRouter()

const login = async () => {
    try {
        const response = await axios.post('http://localhost:5000/login', form.value)
        const token = response.data.token
        const role = response.data.role
        const id = response.data.id

        localStorage.setItem('token', token)
        localStorage.setItem('role', role)
        localStorage.setItem('id', id)

        message.value = 'Login successful'
        isSuccess.value = true

        setTimeout(() => {
            if (role === 'organizer') {
                router.push('/admin')
            } else {
                router.push('/dashboard')
            }
        }, 1000)
    } catch (err) {
        message.value = err.response?.data?.message || 'Error occurred'
        isSuccess.value = false
    }
}
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow">
                    <div class="card-body p-5">
                        <h3 class="text-center mb-4">Event Ticket Login</h3>
                        <div v-if="message" class="alert" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
                            {{ message }}
                        </div>
                        <form @submit.prevent="login">
                            <div class="mb-3">
                                <label for="email_id" class="form-label">Email ID</label>
                                <input type="email" class="form-control" id="email_id" name="email_id" v-model="form.email_id" required placeholder="Enter your email">
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" name="password" v-model="form.password" required placeholder="Enter your password">
                            </div>
                            <button type="submit" class="btn btn-primary w-100 py-2">Login</button>
                        </form>
                        <div class="text-center mt-3">
                            <p>Don't have an account? <router-link to="/register" class="link-primary text-decoration-none">Register here</router-link></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
