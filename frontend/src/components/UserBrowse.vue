<template>
  <div>
    <div class="row">
      <div v-for="e in events" :key="e.id" class="col-md-4 mb-3">
        <div class="glass-card p-3 h-100 d-flex flex-column">
          <h5 class="fw-bold text-primary mb-1">{{ e.name }}</h5>
          <p class="text-secondary small mb-2"><i class="bi bi-geo-alt"></i> {{ e.venue }}</p>
          <p class="small fw-bold mb-2">{{ e.date }} at {{ e.time }}</p>
          <div class="d-flex justify-content-between align-items-center mb-3">
            <span class="badge bg-light text-dark">${{ e.price }}</span>
            <span class="small text-muted">{{ e.total_seats }} seats</span>
          </div>
          
          <button class="btn btn-premium w-100 mt-auto" @click="bookEvent(e)">Book Ticket</button>
        </div>
      </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="selectedEvent" class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" style="background: rgba(0,0,0,0.5); z-index: 1050">
      <div class="glass-card p-4 bg-white" style="width: 600px; max-width: 90%; max-height: 90vh; overflow-y: auto;">
        <div class="d-flex justify-content-between mb-3">
          <h5 class="fw-bold mb-0">Select Seat - {{ selectedEvent.name }}</h5>
          <button class="btn btn-sm btn-secondary" @click="selectedEvent = null">Close</button>
        </div>
        <div class="d-flex flex-wrap gap-2 justify-content-center mb-4">
          <div v-for="seat in seats" :key="seat.id" 
               class="p-2 border rounded text-center shadow-sm"
               :class="seat.status === 'booked' ? 'bg-secondary text-white opacity-50' : 'bg-light cursor-pointer hover-shadow'"
               @click="seat.status !== 'booked' && confirmBooking(seat)"
               :style="seat.status !== 'booked' ? 'cursor: pointer;' : 'cursor: not-allowed;'"
               style="width: 50px;">
            <small class="d-block fw-bold">{{ seat.row }}{{ seat.number }}</small>
          </div>
        </div>
        <p class="text-muted small text-center">Click an available seat to book.</p>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const events = ref([])
const selectedEvent = ref(null)
const seats = ref([])

const fetchEvents = async () => {
  try {
    const res = await api.get('/api/events')
    events.value = res.data.data
  } catch (err) {}
}

const bookEvent = async (event) => {
  try {
    const res = await api.get(`/api/events/${event.id}/seats`)
    seats.value = res.data.data
    selectedEvent.value = event
  } catch (err) {}
}

const confirmBooking = async (seat) => {
  if (confirm(`Book seat ${seat.row}${seat.number} for $${selectedEvent.value.price}?`)) {
    try {
      await api.post('/api/bookings', { event_id: selectedEvent.value.id, seat_id: seat.id })
      alert('Ticket booked successfully!')
      selectedEvent.value = null
    } catch (err) {
      alert(err.response?.data?.message || 'Error booking ticket')
    }
  }
}

onMounted(fetchEvents)
</script>