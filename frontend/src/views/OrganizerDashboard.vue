<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import OrganizerEvents from '@/components/OrganizerEvents.vue'
import OrganizerBookings from '@/components/OrganizerBookings.vue'
import OrganizerSummary from '@/components/OrganizerSummary.vue'

const router = useRouter()
const currentTab = ref('events')
const token = ref('')

onMounted(() => {
    token.value = localStorage.getItem('token')
    const role = localStorage.getItem('role')
    if (!token.value || role !== 'organizer') {
        router.push('/')
    }
})

const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('id')
    router.push('/')
}
</script>

<template>
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2>Organizer Control Panel</h2>
            <span class="badge bg-secondary">Role: Organizer</span>
        </div>
        
        <nav class="nav nav-pills flex-column flex-sm-row mb-4 p-2 bg-light rounded shadow-sm">
            <button class="flex-sm-fill text-sm-center nav-link border-0" :class="{ active: currentTab === 'events' }" @click="currentTab = 'events'">My Events</button>
            <button class="flex-sm-fill text-sm-center nav-link border-0" :class="{ active: currentTab === 'bookings' }" @click="currentTab = 'bookings'">Ticket Bookings</button>
            <button class="flex-sm-fill text-sm-center nav-link border-0" :class="{ active: currentTab === 'summary' }" @click="currentTab = 'summary'">Dashboard Analytics</button>
            <button class="flex-sm-fill text-sm-center nav-link border-0 text-danger" @click="logout">Logout</button>
        </nav>

        <div class="card shadow-sm">
            <div class="card-body">
                <OrganizerEvents v-if="currentTab === 'events'" />
                <OrganizerBookings v-else-if="currentTab === 'bookings'" />
                <OrganizerSummary v-else-if="currentTab === 'summary'" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.nav-link {
    cursor: pointer;
    font-weight: 500;
}
.nav-link.active {
    background-color: #0d6efd !important;
    color: white !important;
}
</style>
