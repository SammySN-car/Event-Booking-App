<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-0">Organizer Dashboard</h2>
      </div>
      <button @click="logout" class="btn btn-outline-danger btn-sm rounded-pill px-3">Logout</button>
    </div>

    <ul class="nav nav-pills mb-4 pb-2 border-bottom border-secondary opacity-75">
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2 me-2" :class="{ 'active': activeTab === 'events', 'btn-premium': activeTab === 'events' }" @click="activeTab = 'events'">Events & Seats</button>
      </li>
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2 me-2" :class="{ 'active': activeTab === 'bookings', 'btn-premium': activeTab === 'bookings' }" @click="activeTab = 'bookings'">Bookings List</button>
      </li>
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2" :class="{ 'active': activeTab === 'summary', 'btn-premium': activeTab === 'summary' }" @click="activeTab = 'summary'">Summary Charts</button>
      </li>
    </ul>

    <div class="glass-card p-4">
      <div v-if="activeTab === 'events'"><OrganizerEvents /></div>
      <div v-if="activeTab === 'bookings'"><OrganizerBookings /></div>
      <div v-if="activeTab === 'summary'"><OrganizerSummary /></div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { clearAuth } from '../api/auth'
import OrganizerEvents from '../components/OrganizerEvents.vue'
import OrganizerBookings from '../components/OrganizerBookings.vue'
import OrganizerSummary from '../components/OrganizerSummary.vue'

const router = useRouter()
const activeTab = ref('events')

const logout = () => { clearAuth(); router.push('/login') }
</script>
<style scoped>
.nav-link { color: var(--text-secondary); font-weight: 500; transition: all 0.2s; }
.nav-link:hover:not(.active) { background: var(--surface-2); color: var(--text-main); }
</style>