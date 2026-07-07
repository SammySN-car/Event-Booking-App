import os

components = {
    "views/Login.vue": """<template>
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
</script>""",

    "views/Signup.vue": """<template>
  <div class="row justify-content-center align-items-center py-5">
    <div class="col-md-6">
      <div class="glass-card p-5">
        <div class="text-center mb-4">
          <h2 class="fw-bold">Create Account</h2>
          <p class="text-muted">Join Event Ticket Booking</p>
        </div>
        
        <form @submit.prevent="handleSignup">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label text-secondary small fw-bold">Full Name</label>
              <input type="text" v-model="form.name" class="form-control form-control-premium py-2" required>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label text-secondary small fw-bold">Email address</label>
              <input type="email" v-model="form.email" class="form-control form-control-premium py-2" required>
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label text-secondary small fw-bold">Phone</label>
              <input type="text" v-model="form.phone" class="form-control form-control-premium py-2" required>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label text-secondary small fw-bold">Account Type</label>
              <select v-model="form.role" class="form-control form-control-premium py-2">
                <option value="user">Standard User</option>
                <option value="organizer">Event Organizer</option>
              </select>
            </div>
          </div>
          
          <div class="mb-4">
            <label class="form-label text-secondary small fw-bold">Password</label>
            <input type="password" v-model="form.password" class="form-control form-control-premium py-2" required>
          </div>
          
          <div class="d-grid mb-3">
            <button type="submit" class="btn btn-premium py-2 fw-bold" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              Sign Up
            </button>
          </div>
          
          <div v-if="error" class="alert alert-danger py-2 text-center small mb-0 rounded">{{ error }}</div>
          <div v-if="success" class="alert alert-success py-2 text-center small mb-0 rounded">{{ success }}</div>
        </form>
        <div class="text-center mt-4 pt-3 border-top border-secondary opacity-50">
          <p class="small text-muted mb-0">Already have an account? <router-link to="/login" class="text-primary fw-bold text-decoration-none">Sign in</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/client'

const router = useRouter()
const form = ref({ name: '', email: '', phone: '', password: '', role: 'user' })
const error = ref('')
const success = ref('')
const loading = ref(false)

const handleSignup = async () => {
  error.value = ''; success.value = ''; loading.value = true
  try {
    await api.post('/api/signup', form.value)
    success.value = 'Account created successfully! Redirecting...'
    setTimeout(() => router.push('/login'), 1500)
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to register'
  } finally {
    loading.value = false
  }
}
</script>""",

    "views/OrganizerDashboard.vue": """<template>
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
</style>""",

    "views/UserDashboard.vue": """<template>
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
</style>""",

    "components/OrganizerEvents.vue": """<template>
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
</script>""",

    "components/OrganizerBookings.vue": """<template>
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
</script>""",

    "components/OrganizerSummary.vue": """<template>
  <div>
    <h5 class="fw-bold mb-4">Event Summary</h5>
    <div class="row">
      <div v-for="s in summary" :key="s.event_name" class="col-md-6 mb-3">
        <div class="glass-card p-4 h-100">
          <h6 class="fw-bold text-primary mb-3">{{ s.event_name }}</h6>
          <div class="d-flex justify-content-between mb-2 pb-2 border-bottom">
            <span class="text-secondary">Revenue</span>
            <span class="fw-bold text-success">${{ s.revenue.toFixed(2) }}</span>
          </div>
          <div class="d-flex justify-content-between mb-2 pb-2 border-bottom">
            <span class="text-secondary">Tickets Sold</span>
            <span class="fw-bold">{{ s.confirmed_bookings }}</span>
          </div>
          <div class="d-flex justify-content-between">
            <span class="text-secondary">Occupancy</span>
            <span class="fw-bold" :class="s.occupancy_percent > 80 ? 'text-success' : 'text-warning'">{{ s.occupancy_percent }}%</span>
          </div>
        </div>
      </div>
      <div v-if="summary.length === 0" class="text-muted p-3">No events to summarize.</div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const summary = ref([])

const fetchSummary = async () => {
  try {
    const res = await api.get('/api/summary')
    summary.value = res.data.data
  } catch (err) {}
}

onMounted(fetchSummary)
</script>""",

    "components/UserBrowse.vue": """<template>
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
</script>""",

    "components/UserTickets.vue": """<template>
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
</script>"""
}

base_path = r"c:\Users\samar\Downloads\4-projects\event-booking\frontend\src"
os.makedirs(os.path.join(base_path, "components"), exist_ok=True)
os.makedirs(os.path.join(base_path, "views"), exist_ok=True)

for name, content in components.items():
    path = os.path.join(base_path, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Vue components for event-booking generated successfully.")
