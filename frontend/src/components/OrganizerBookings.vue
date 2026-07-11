<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const bookings = ref([])
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

const fetchBookings = async () => {
    try {
        const response = await axios.get('http://localhost:5000/user/home', {
            headers: { Authorization: `Bearer ${token}` }
        })
        bookings.value = response.data.all_bookings
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch bookings'
        isSuccess.value = false
    }
}

const cancelUserBooking = async (bookingId) => {
    if (!confirm('Are you sure you want to cancel this booking on behalf of the user?')) return
    try {
        const response = await axios.put(`http://localhost:5000/user/release/${bookingId}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Booking cancelled successfully'
        isSuccess.value = true
        fetchBookings()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to cancel booking'
        isSuccess.value = false
    }
}

onMounted(() => {
    fetchBookings()
})
</script>

<template>
    <div>
        <h3 class="mb-4">Ticket Booking Details</h3>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <div class="table-responsive">
            <table class="table table-striped table-hover align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>Booking ID</th>
                        <th>User ID</th>
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
                    <tr v-for="b in bookings" :key="b.id">
                        <td>{{ b.id }}</td>
                        <td>{{ b.user_id }}</td>
                        <td><strong>{{ b.event_name }}</strong></td>
                        <td>{{ b.venue }}</td>
                        <td>{{ b.date }}</td>
                        <td><span class="badge bg-secondary">{{ b.seat }}</span></td>
                        <td><code>{{ b.ticket_id }}</code></td>
                        <td><small>{{ b.booking_timestamp }}</small></td>
                        <td>
                            <span class="badge" :class="b.status === 'confirmed' ? 'bg-success' : 'bg-danger'">
                                {{ b.status }}
                            </span>
                        </td>
                        <td>
                            <button v-if="b.status === 'confirmed'" class="btn btn-sm btn-outline-danger" @click="cancelUserBooking(b.id)">
                                Cancel
                            </button>
                            <span v-else class="text-muted">-</span>
                        </td>
                    </tr>
                    <tr v-if="bookings.length === 0">
                        <td colspan="10" class="text-center text-muted py-4">No bookings made for your events.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
