<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const form = ref({
    full_name: '',
    email_id: '',
    password: '',
    phone: '',
    role: 'user'
})
const message = ref('')
const isSuccess = ref(false)
const router = useRouter()

const register = async () => {
    try {
        const response = await axios.post('http://localhost:5000/register', form.value)
        message.value = response.data.message || 'Registration successful!'
        isSuccess.value = true
        setTimeout(() => {
            router.push('/')
        }, 1500)
    } catch (err) {
        message.value = err.response?.data?.message || 'Registration failed'
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
                        <h3 class="text-center mb-4">Event Ticket Registration</h3>
                        <div v-if="message" class="alert" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
                            {{ message }}
                        </div>
                        <form @submit.prevent="register">
                            <div class="mb-3">
                                <label for="full_name" class="form-label">Full Name</label>
                                <input type="text" class="form-control" id="full_name" v-model="form.full_name" required placeholder="Enter your full name">
                            </div>
                            <div class="mb-3">
                                <label for="email_id" class="form-label">Email ID</label>
                                <input type="email" class="form-control" id="email_id" v-model="form.email_id" required placeholder="Enter your email">
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" v-model="form.password" required placeholder="Create a password">
                            </div>
                            <div class="mb-3">
                                <label for="phone" class="form-label">Phone Number</label>
                                <input type="text" class="form-control" id="phone" v-model="form.phone" placeholder="Enter phone number">
                            </div>
                            <div class="mb-3">
                                <label for="role" class="form-label">Register As</label>
                                <select class="form-select" id="role" v-model="form.role">
                                    <option value="user">User (Book Tickets)</option>
                                    <option value="organizer">Organizer (Manage Events)</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-primary w-100 py-2">Register</button>
                        </form>
                        <div class="text-center mt-3">
                            <p>Already have an account? <router-link to="/" class="link-primary text-decoration-none">Login here</router-link></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
