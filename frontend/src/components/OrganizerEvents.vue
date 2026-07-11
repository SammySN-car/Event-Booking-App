<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const events = ref([])
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

// Form states
const showAddForm = ref(false)
const showEditForm = ref(false)

const newEvent = ref({
    name: '',
    venue: '',
    date: '',
    start_time: '',
    end_time: '',
    price: 0,
    total_seats: 50
})

const editEventData = ref({
    id: null,
    name: '',
    venue: '',
    date: '',
    start_time: '',
    end_time: '',
    price: 0,
    total_seats: 50
})

const fetchEvents = async () => {
    try {
        const response = await axios.get('http://localhost:5000/admin/home', {
            headers: { Authorization: `Bearer ${token}` }
        })
        events.value = response.data.all_events
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch events'
        isSuccess.value = false
    }
}

const addEvent = async () => {
    try {
        const response = await axios.post('http://localhost:5000/admin/add_lot', newEvent.value, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Event added successfully'
        isSuccess.value = true
        showAddForm.value = false
        // Reset form
        newEvent.value = { name: '', venue: '', date: '', start_time: '', end_time: '', price: 0, total_seats: 50 }
        fetchEvents()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to add event'
        isSuccess.value = false
    }
}

const editEvent = (event) => {
    editEventData.value = { ...event }
    showEditForm.value = true
    showAddForm.value = false
}

const updateEvent = async () => {
    try {
        const response = await axios.put(`http://localhost:5000/admin/edit_lot/${editEventData.value.id}`, editEventData.value, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Event updated successfully'
        isSuccess.value = true
        showEditForm.value = false
        fetchEvents()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to update event'
        isSuccess.value = false
    }
}

const deleteEvent = async (eventId) => {
    if (!confirm('Are you sure you want to delete this event? This will release all booked seats.')) return
    try {
        const response = await axios.delete(`http://localhost:5000/admin/delete_lot/${eventId}`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        message.value = response.data.message || 'Event deleted successfully'
        isSuccess.value = true
        fetchEvents()
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to delete event'
        isSuccess.value = false
    }
}

onMounted(() => {
    fetchEvents()
})
</script>

<template>
    <div>
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h3>Manage Events</h3>
            <button class="btn btn-success" @click="showAddForm = !showAddForm; showEditForm = false">
                {{ showAddForm ? 'Cancel' : 'Create New Event' }}
            </button>
        </div>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <!-- Add Event Form -->
        <div v-if="showAddForm" class="card bg-light mb-4 shadow-sm border-0">
            <div class="card-body">
                <h5 class="card-title">Create New Event</h5>
                <form @submit.prevent="addEvent">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Event Name</label>
                            <input type="text" class="form-control" v-model="newEvent.name" required placeholder="e.g. Summer Music Fest">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Venue</label>
                            <input type="text" class="form-control" v-model="newEvent.venue" required placeholder="e.g. Auditorium A">
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Date</label>
                            <input type="date" class="form-control" v-model="newEvent.date" required>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Start Time</label>
                            <input type="time" class="form-control" v-model="newEvent.start_time" required>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">End Time</label>
                            <input type="time" class="form-control" v-model="newEvent.end_time" required>
                        </div>
                        <div class="col-md-2">
                            <label class="form-label">Ticket Price ($)</label>
                            <input type="number" class="form-control" v-model.number="newEvent.price" min="0" required>
                        </div>
                        <div class="col-md-2">
                            <label class="form-label">Total Seats</label>
                            <input type="number" class="form-control" v-model.number="newEvent.total_seats" min="1" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary mt-3">Publish Event</button>
                </form>
            </div>
        </div>

        <!-- Edit Event Form -->
        <div v-if="showEditForm" class="card bg-light mb-4 shadow-sm border-0 border-start border-primary border-4">
            <div class="card-body">
                <h5 class="card-title">Edit Event: {{ editEventData.name }}</h5>
                <form @submit.prevent="updateEvent">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Event Name</label>
                            <input type="text" class="form-control" v-model="editEventData.name" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Venue</label>
                            <input type="text" class="form-control" v-model="editEventData.venue" required>
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Date</label>
                            <input type="date" class="form-control" v-model="editEventData.date" required>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Start Time</label>
                            <input type="time" class="form-control" v-model="editEventData.start_time" required>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">End Time</label>
                            <input type="time" class="form-control" v-model="editEventData.end_time" required>
                        </div>
                        <div class="col-md-2">
                            <label class="form-label">Ticket Price ($)</label>
                            <input type="number" class="form-control" v-model.number="editEventData.price" min="0" required>
                        </div>
                        <div class="col-md-2">
                            <label class="form-label">Total Seats</label>
                            <input type="number" class="form-control" v-model.number="editEventData.total_seats" min="1" required>
                        </div>
                    </div>
                    <div class="mt-3">
                        <button type="submit" class="btn btn-primary me-2">Save Changes</button>
                        <button type="button" class="btn btn-secondary" @click="showEditForm = false">Cancel</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Events List -->
        <div class="row row-cols-1 row-cols-md-2 g-4">
            <div class="col" v-for="item in events" :key="item.id">
                <div class="card shadow-sm h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <h4 class="card-title text-primary">{{ item.name }}</h4>
                            <span class="badge bg-secondary">ID: {{ item.id }}</span>
                        </div>
                        <h6 class="card-subtitle mb-2 text-muted">{{ item.venue }} | {{ item.date }} @ {{ item.start_time }} - {{ item.end_time }}</h6>
                        <p class="card-text">
                            <strong>Ticket Price:</strong> ${{ item.price }} <br>
                            <strong>Seats:</strong> {{ item.booked }} booked / {{ item.total_seats }} total
                        </p>

                        <div class="mb-3">
                            <strong>Seat Map:</strong>
                            <div class="d-flex flex-wrap gap-1 mt-2">
                                <span v-for="seat in item.seats" :key="seat.id" class="badge" :class="seat.status === 'B' ? 'bg-danger' : 'bg-success'">
                                    {{ seat.row }}{{ seat.number }}
                                </span>
                            </div>
                        </div>

                        <div class="mt-3">
                            <button class="btn btn-sm btn-outline-primary me-2" @click="editEvent(item)">Edit</button>
                            <button class="btn btn-sm btn-outline-danger" @click="deleteEvent(item.id)">Delete</button>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="events.length === 0" class="col-12 text-center text-muted py-5">
                No events found. Click "Create New Event" to publish one!
            </div>
        </div>
    </div>
</template>
