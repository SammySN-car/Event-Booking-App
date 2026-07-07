<template>
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
</script>