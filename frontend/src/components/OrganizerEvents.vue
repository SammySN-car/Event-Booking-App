<template>
  <div>
    <div class="d-flex justify-content-between mb-3">
      <h5 class="fw-bold">Manage Events</h5>
      <button class="btn btn-primary btn-sm" @click="showAddModal = true">+ Create Event</button>
    </div>
    
    <div class="table-responsive">
      <table class="table align-middle">
        <thead class="table-light">
          <tr>
            <th>Event Name</th>
            <th>Venue</th>
            <th>Date & Time</th>
            <th>Price</th>
            <th>Seats</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in events" :key="e.id">
            <td class="fw-bold">{{ e.name }}</td>
            <td>{{ e.venue }}</td>
            <td>{{ e.date }} at {{ e.time }}</td>
            <td>${{ e.price }}</td>
            <td>{{ e.total_seats }}</td>
            <td>
              <button class="btn btn-sm btn-outline-info me-2" @click="viewSeatMap(e)">Seat Map</button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteEvent(e.id)">Cancel Event</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Seat Map Modal -->
    <div v-if="selectedEvent" class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" style="background: rgba(0,0,0,0.5); z-index: 1050">
      <div class="glass-card p-4 bg-white" style="width: 600px; max-width: 90%; max-height: 90vh; overflow-y: auto;">
        <div class="d-flex justify-content-between mb-3">
          <h5 class="fw-bold mb-0">{{ selectedEvent.name }} - Seat Map</h5>
          <button class="btn btn-sm btn-secondary" @click="selectedEvent = null">Close</button>
        </div>
        <div class="d-flex flex-wrap gap-2 justify-content-center">
          <div v-for="seat in seats" :key="seat.id" 
               class="p-2 border rounded text-center shadow-sm"
               :class="seat.status === 'booked' ? 'bg-secondary text-white' : 'bg-light'"
               style="width: 50px; cursor: default;">
            <small class="d-block fw-bold">{{ seat.row }}{{ seat.number }}</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" style="background: rgba(0,0,0,0.5); z-index: 1050">
      <div class="glass-card p-4 bg-white" style="width: 500px; max-width: 90%">
        <h5 class="fw-bold mb-3">Create Event</h5>
        <form @submit.prevent="saveEvent">
          <div class="mb-2"><label class="small fw-bold">Name</label><input type="text" v-model="form.name" class="form-control" required></div>
          <div class="mb-2"><label class="small fw-bold">Venue</label><input type="text" v-model="form.venue" class="form-control" required></div>
          <div class="row mb-2">
            <div class="col-6"><label class="small fw-bold">Date (YYYY-MM-DD)</label><input type="text" v-model="form.date" class="form-control" required></div>
            <div class="col-6"><label class="small fw-bold">Time (HH:MM)</label><input type="text" v-model="form.time" class="form-control" required></div>
          </div>
          <div class="row mb-3">
            <div class="col-6"><label class="small fw-bold">Price</label><input type="number" step="0.01" v-model="form.price" class="form-control" required></div>
            <div class="col-6"><label class="small fw-bold">Total Seats</label><input type="number" v-model="form.total_seats" class="form-control" required></div>
          </div>
          <div class="d-flex justify-content-end gap-2">
            <button type="button" class="btn btn-secondary" @click="showAddModal = false">Cancel</button>
            <button type="submit" class="btn btn-premium">Create</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'
import { getUserId } from '../api/auth'

const events = ref([])
const showAddModal = ref(false)
const selectedEvent = ref(null)
const seats = ref([])
const form = ref({ name: '', venue: '', date: '', time: '', price: 0, total_seats: 50 })

const fetchEvents = async () => {
  try {
    const res = await api.get('/api/events')
    const userId = parseInt(getUserId())
    // Organizer sees their own events
    events.value = res.data.data.filter(e => e.organizer_id === userId)
  } catch (err) {}
}

const saveEvent = async () => {
  try {
    await api.post('/api/events', form.value)
    showAddModal.value = false
    fetchEvents()
  } catch (err) { alert(err.response?.data?.message || 'Error') }
}

const viewSeatMap = async (event) => {
  try {
    const res = await api.get(`/api/events/${event.id}/seats`)
    seats.value = res.data.data
    selectedEvent.value = event
  } catch (err) {}
}

const deleteEvent = async (id) => {
  if(confirm('Delete event?')) {
    await api.delete(`/api/events/${id}`)
    fetchEvents()
  }
}

onMounted(fetchEvents)
</script>