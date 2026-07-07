<template>
  <div>
    <h5 class="fw-bold mb-3">Recent Bookings</h5>
    <div class="table-responsive">
      <table class="table align-middle">
        <thead class="table-light">
          <tr><th>Ticket ID</th><th>Event</th><th>Attendee</th><th>Seat</th><th>Status</th><th>Action</th></tr>
        </thead>
        <tbody>
          <tr v-for="b in bookings" :key="b.id">
            <td class="fw-bold text-primary">{{ b.ticket_id }}</td>
            <td>{{ b.event_name }}</td>
            <td>{{ b.user_name }}</td>
            <td><span class="badge bg-secondary">{{ b.seat }}</span></td>
            <td>
              <span class="badge" :class="b.status === 'confirmed' ? 'bg-success' : 'bg-danger'">{{ b.status.toUpperCase() }}</span>
            </td>
            <td>
              <button v-if="b.status === 'confirmed'" class="btn btn-sm btn-outline-danger" @click="cancelBooking(b.id)">Cancel Ticket</button>
            </td>
          </tr>
        </tbody>
      </table>
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
  } catch (err) {}
}

const cancelBooking = async (id) => {
  if(confirm('Cancel this booking?')) {
    await api.delete(`/api/bookings/${id}`)
    fetchBookings()
  }
}

onMounted(fetchBookings)
</script>