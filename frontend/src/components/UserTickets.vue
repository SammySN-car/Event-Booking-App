<template>
  <div>
    <h5 class="fw-bold mb-4">My Tickets</h5>
    <div class="row">
      <div v-for="b in bookings" :key="b.id" class="col-md-6 mb-3">
        <div class="glass-card p-4 position-relative" :class="b.status === 'cancelled' ? 'opacity-75' : ''">
          <div class="position-absolute top-0 end-0 m-3">
             <span class="badge" :class="b.status === 'confirmed' ? 'bg-success' : 'bg-danger'">
               {{ b.status.toUpperCase() }}
             </span>
          </div>
          <p class="text-muted small fw-bold mb-1">Ticket #{{ b.ticket_id }}</p>
          <h5 class="fw-bold text-primary mb-2">{{ b.event_name }}</h5>
          <p class="mb-1"><i class="bi bi-calendar"></i> {{ b.date }}</p>
          <p class="mb-3"><i class="bi bi-person"></i> Seat: <span class="badge bg-secondary">{{ b.seat }}</span></p>
          
          <button v-if="b.status === 'confirmed'" class="btn btn-outline-danger btn-sm w-100" @click="cancelTicket(b.id)">
            Cancel & Refund
          </button>
        </div>
      </div>
      <div v-if="bookings.length === 0" class="col-12 text-center text-muted py-5">
        No tickets found.
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const bookings = ref([])

const fetchBookings = async () => {
  try {
    const res = await api.get('/api/bookings')
    bookings.value = res.data.data
  } catch(err) {}
}

const cancelTicket = async (id) => {
  if (confirm('Cancel this ticket?')) {
    try {
      await api.delete(`/api/bookings/${id}`)
      fetchBookings()
    } catch (err) {}
  }
}

onMounted(fetchBookings)
</script>