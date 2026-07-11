<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'

const bookings = ref([])
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

// CSV Export States
const exportMessage = ref('')
const downl = ref('')
const downR = ref(false)
let starpoll = null

const fetchMyTickets = async () => {
    try {
        const response = await axios.get('http://localhost:5000/user/home', {
            headers: { Authorization: `Bearer ${token}` }
        })
        bookings.value = response.data.all_bookings
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch tickets'
        isSuccess.value = false
    }
}

const cancelTicket = async (bookingId) => {
    if (!confirm('Are you sure you want to cancel this booking? This action is permanent.')) return
    try {
        const response = await axios.put(`http://localhost:5000/user/release/${bookingId}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Ticket booking cancelled successfully'
        isSuccess.value = true
        fetchMyTickets()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to cancel ticket'
        isSuccess.value = false
    }
}

// CSV Export Methods
const triggerExport = async () => {
    try {
        const pat = await axios.get('http://localhost:5000/user/export_csv', {
            headers: { Authorization: `Bearer ${token}` }
        })
        const file_name = pat.data.file_name
        localStorage.setItem('file_name', file_name)
        exportMessage.value = 'CSV Export has been scheduled and is processing...'
        stpoll()
    } catch (err) {
        exportMessage.value = 'Failed to schedule CSV export'
    }
}

const checkdownl = async () => {
    const file_name = localStorage.getItem('file_name')
    if (!file_name || file_name === 'none') return

    try {
        const pat = await axios.get(`http://localhost:5000/user/export_csv/${file_name}`, {
            headers: { Authorization: `Bearer ${token}` },
            responseType: 'blob'
        })
        if (pat.status === 200) {
            downl.value = URL.createObjectURL(pat.data)
            downR.value = true
            exportMessage.value = 'CSV Export complete! Ready for download.'
            if (starpoll) {
                clearInterval(starpoll)
                starpoll = null
            }
        }
    } catch (e) {
        // Not ready yet
    }
}

const stpoll = () => {
    if (starpoll) clearInterval(starpoll)
    starpoll = setInterval(checkdownl, 3000)
}

const cleardownl = () => {
    localStorage.removeItem('file_name')
    downR.value = false
    exportMessage.value = ''
    if (downl.value) {
        URL.revokeObjectURL(downl.value)
        downl.value = ''
    }
}

onMounted(() => {
    fetchMyTickets()
    const file_name = localStorage.getItem('file_name')
    if (file_name && file_name !== 'none') {
        stpoll()
    }
})

onBeforeUnmount(() => {
    if (starpoll) {
        clearInterval(starpoll)
        starpoll = null
    }
})
</script>

<template>
    <div>
        <h3 class="mb-4">My Booked Tickets & History</h3>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <div class="row">
            <!-- Active Tickets -->
            <div class="col-12 mb-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5 class="card-title text-primary mb-3">Active Tickets</h5>
                        <div class="table-responsive">
                            <table class="table table-striped align-middle">
                                <thead>
                                    <tr>
                                        <th>Booking ID</th>
                                        <th>Event Name</th>
                                        <th>Venue</th>
                                        <th>Date & Time</th>
                                        <th>Seat Code</th>
                                        <th>Ticket ID</th>
                                        <th>Booked At</th>
                                        <th>Status</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="b in bookings.filter(x => x.status === 'confirmed')" :key="b.id">
                                        <td>{{ b.id }}</td>
                                        <td><strong>{{ b.event_name }}</strong></td>
                                        <td>{{ b.venue }}</td>
                                        <td>{{ b.date }}</td>
                                        <td><span class="badge bg-secondary">{{ b.seat }}</span></td>
                                        <td><code>{{ b.ticket_id }}</code></td>
                                        <td><small>{{ b.booking_timestamp }}</small></td>
                                        <td><span class="badge bg-success">Confirmed</span></td>
                                        <td>
                                            <button class="btn btn-sm btn-danger" @click="cancelTicket(b.id)">
                                                Cancel Ticket
                                            </button>
                                        </td>
                                    </tr>
                                    <tr v-if="bookings.filter(x => x.status === 'confirmed').length === 0">
                                        <td colspan="9" class="text-center text-muted py-3">You don't have any active ticket bookings.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Cancelled History -->
            <div class="col-12 mb-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5 class="card-title text-secondary mb-3">Cancellation History</h5>
                        <div class="table-responsive">
                            <table class="table table-striped align-middle">
                                <thead>
                                    <tr>
                                        <th>Booking ID</th>
                                        <th>Event Name</th>
                                        <th>Venue</th>
                                        <th>Date & Time</th>
                                        <th>Seat Code</th>
                                        <th>Ticket ID</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="b in bookings.filter(x => x.status === 'cancelled')" :key="b.id">
                                        <td>{{ b.id }}</td>
                                        <td><strong>{{ b.event_name }}</strong></td>
                                        <td>{{ b.venue }}</td>
                                        <td>{{ b.date }}</td>
                                        <td><span class="badge bg-light text-dark">{{ b.seat }}</span></td>
                                        <td><code>{{ b.ticket_id }}</code></td>
                                        <td><span class="badge bg-danger">Cancelled</span></td>
                                    </tr>
                                    <tr v-if="bookings.filter(x => x.status === 'cancelled').length === 0">
                                        <td colspan="7" class="text-center text-muted py-3">No cancelled bookings found.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Export CSV Section -->
        <hr class="my-4">
        <div class="d-flex align-items-center flex-wrap gap-3">
            <button class="btn btn-outline-primary" @click="triggerExport">Export Booking History (CSV)</button>
            <button v-if="downR" class="btn btn-secondary" @click="cleardownl">Clear Export</button>
        </div>

        <div v-if="exportMessage" class="alert mt-3" :class="downR ? 'alert-success' : 'alert-info'" role="alert">
            {{ exportMessage }}
            <div v-if="downR" class="mt-2">
                <a :href="downl" target="_blank" class="btn btn-success btn-sm" download="booking_history.csv">Download CSV</a>
            </div>
        </div>
    </div>
</template>
