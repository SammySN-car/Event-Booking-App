<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-0">Browse Events</h2>
      </div>
      <button @click="logout" class="btn btn-outline-danger btn-sm rounded-pill px-3">Logout</button>
    </div>

    <ul class="nav nav-pills mb-4 pb-2 border-bottom border-secondary opacity-75">
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2 me-2" :class="{ 'active': activeTab === 'browse', 'btn-premium': activeTab === 'browse' }" @click="activeTab = 'browse'">Browse Events</button>
      </li>
      <li class="nav-item">
        <button class="nav-link rounded-pill px-4 py-2 me-2" :class="{ 'active': activeTab === 'tickets', 'btn-premium': activeTab === 'tickets' }" @click="activeTab = 'tickets'">My Tickets</button>
      </li>
    </ul>

    <div class="glass-card p-4">
      <div v-if="activeTab === 'browse'"><UserBrowse /></div>
      <div v-if="activeTab === 'tickets'"><UserTickets /></div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { clearAuth } from '../api/auth'
import UserBrowse from '../components/UserBrowse.vue'
import UserTickets from '../components/UserTickets.vue'

const router = useRouter()
const activeTab = ref('browse')

const logout = () => { clearAuth(); router.push('/login') }
</script>
<style scoped>
.nav-link { color: var(--text-secondary); font-weight: 500; transition: all 0.2s; }
.nav-link:hover:not(.active) { background: var(--surface-2); color: var(--text-main); }
</style>