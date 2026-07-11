<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const events = ref([])
const searchQuery = ref('')
const selectedEvent = ref(null)
const selectedSeat = ref(null)
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

const getEventStatus = (event) => {
    try {
        const now = new Date()
        const endDt = new Date(`${event.date}T${event.end_time}:00`)
        const startDt = new Date(`${event.date}T${event.start_time}:00`)
        if (now >= endDt) return 'Ended'
        if (now >= startDt) return 'Started'
        return 'Upcoming'
    } catch (e) {
        return 'Upcoming'
    }
}

const fetchEvents = async () => {
    try {
        const response = await axios.get('http://localhost:5000/admin/home', {
            headers: { Authorization: `Bearer ${token}` }
        })
        events.value = response.data.all_events
        // Update selected event if it's currently opened
        if (selectedEvent.value) {
            const updated = events.value.find(e => e.id === selectedEvent.value.id)
            if (updated) selectedEvent.value = updated
        }
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch events'
        isSuccess.value = false
    }
}

const selectEvent = (event) => {
    selectedEvent.value = event
    selectedSeat.value = null
    message.value = ''
}

const bookSeat = async () => {
    if (!selectedEvent.value || !selectedSeat.value) return
    try {
        const response = await axios.post(`http://localhost:5000/user/book/${selectedEvent.value.id}`, {
            event_id: selectedEvent.value.id,
            seat_id: selectedSeat.value.id
        }, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Seat booked successfully!'
        isSuccess.value = true
        selectedSeat.value = null
        await fetchEvents()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to book ticket'
        isSuccess.value = false
    }
}

const filteredEvents = computed(() => {
    if (!searchQuery.value) return events.value
    const query = searchQuery.value.toLowerCase()
    return events.value.filter(e => 
        e.name.toLowerCase().includes(query) ||
        e.venue.toLowerCase().includes(query)
    )
})

onMounted(() => {
    fetchEvents()
})
</script>

<template>
    <div>
        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <div class="row">
            <!-- Events List Column -->
            <div class="col-md-7 mb-4">
                <h4 class="mb-3">Available Events</h4>
                <div class="mb-3">
                    <input type="text" class="form-control" v-model="searchQuery" placeholder="Search events by name or venue...">
                </div>

                <div class="list-group shadow-sm">
                    <button v-for="item in filteredEvents" :key="item.id" 
                            class="list-group-item list-group-item-action border-0 mb-2 rounded p-3"
                            :class="{ active: selectedEvent && selectedEvent.id === item.id }"
                            @click="selectEvent(item)">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1 fw-bold">{{ item.name }}</h5>
                            <span class="badge" :class="selectedEvent && selectedEvent.id === item.id ? 'bg-light text-primary' : 'bg-primary'">
                                ${{ item.price }}
                            </span>
                        </div>
                        <p class="mb-1 text-truncate"><small>{{ item.venue }}</small></p>
                        <div class="d-flex justify-content-between align-items-center mt-2">
                            <small :class="selectedEvent && selectedEvent.id === item.id ? 'text-white-50' : 'text-muted'">
                                Date: {{ item.date }} @ {{ item.start_time }} - {{ item.end_time }}
                            </small>
                            <span v-if="getEventStatus(item) === 'Ended'" class="badge bg-danger ms-2">Ended</span>
                            <span v-else-if="getEventStatus(item) === 'Started'" class="badge bg-warning text-dark ms-2">Started</span>
                            <span v-else class="badge rounded-pill" :class="item.available > 0 ? 'bg-success' : 'bg-danger'">
                                {{ item.available }} seats remaining
                            </span>
                        </div>
                    </button>
                    <div v-if="filteredEvents.length === 0" class="text-center text-muted py-4">No events found.</div>
                </div>
            </div>

            <!-- Seat Booking Grid Column -->
            <div class="col-md-5 mb-4">
                <h4 class="mb-3">Seat Selection</h4>
                <div v-if="selectedEvent" class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5 class="card-title text-primary">{{ selectedEvent.name }}</h5>
                        <p class="card-text mb-3 text-muted">Venue: {{ selectedEvent.venue }}</p>
                        
                        <div v-if="getEventStatus(selectedEvent) === 'Ended'" class="alert alert-danger text-center my-3">
                            This event has ended. Tickets cannot be booked.
                        </div>
                        <div v-else-if="getEventStatus(selectedEvent) === 'Started'" class="alert alert-warning text-center my-3">
                            This event has already started. Booking is closed.
                        </div>
                        <template v-else>
                            <div class="border p-3 text-center mb-3 bg-light rounded text-uppercase tracking-wider fw-bold text-secondary">
                                --- STAGE / SCREEN ---
                            </div>

                            <!-- Seat Grid -->
                            <div class="d-flex flex-wrap justify-content-center gap-2 mb-4">
                                <button v-for="seat in selectedEvent.seats" :key="seat.id"
                                        class="btn btn-sm px-3"
                                        :class="{
                                            'btn-danger disabled': seat.status === 'B',
                                            'btn-outline-success': seat.status === 'A' && (!selectedSeat || selectedSeat.id !== seat.id),
                                            'btn-success text-white': selectedSeat && selectedSeat.id === seat.id
                                        }"
                                        :disabled="seat.status === 'B'"
                                        @click="selectedSeat = seat">
                                    {{ seat.row }}{{ seat.number }}
                                </button>
                            </div>

                            <div v-if="selectedSeat" class="bg-light p-3 rounded mb-3 border">
                                <p class="mb-1">Selected Seat: <strong>{{ selectedSeat.row }}{{ selectedSeat.number }}</strong></p>
                                <p class="mb-0">Price: <strong>${{ selectedEvent.price }}</strong></p>
                            </div>

                            <button class="btn btn-primary w-100 py-2" :disabled="!selectedSeat" @click="bookSeat">
                                Confirm Booking
                            </button>
                        </template>
                    </div>
                </div>
                <div v-else class="card shadow-sm border-0 text-center py-5 text-muted">
                    Select an event from the list to view seating layout and book tickets.
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.list-group-item {
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid rgba(0,0,0,.125) !important;
}
.list-group-item.active {
    background-color: #0d6efd !important;
    border-color: #0d6efd !important;
}
</style>
