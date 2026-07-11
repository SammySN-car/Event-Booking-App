<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Chart, BarController, BarElement, CategoryScale, LinearScale, PieController, ArcElement, Tooltip, Legend } from 'chart.js'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, PieController, ArcElement, Tooltip, Legend)

const occupancyChartRef = ref(null)
const revenueChartRef = ref(null)
const message = ref('')
const isSuccess = ref(false)
const token = localStorage.getItem('token')

const occupancyChartInstance = ref(null)
const revenueChartInstance = ref(null)

const fetchSummary = async () => {
    try {
        const response = await axios.get('http://localhost:5000/admin/summary', {
            headers: { Authorization: `Bearer ${token}` }
        })
        const data = response.data
        const revenue = data.revenue_data || []
        const occupancy = data.occupancy_data || []

        if (occupancy.length > 0) {
            if (occupancyChartInstance.value) occupancyChartInstance.value.destroy()
            occupancyChartInstance.value = new Chart(occupancyChartRef.value, {
                type: 'bar',
                data: {
                    labels: occupancy.map(o => o.name),
                    datasets: [
                        {
                            label: 'Tickets Booked',
                            data: occupancy.map(o => o.booked),
                            backgroundColor: 'rgba(54, 162, 235, 0.7)'
                        },
                        {
                            label: 'Total Available Seats',
                            data: occupancy.map(o => o.total_seats),
                            backgroundColor: 'rgba(201, 203, 207, 0.5)'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { precision: 0 }
                        }
                    }
                }
            })
        }

        if (revenue.length > 0) {
            if (revenueChartInstance.value) revenueChartInstance.value.destroy()
            revenueChartInstance.value = new Chart(revenueChartRef.value, {
                type: 'pie',
                data: {
                    labels: revenue.map(r => r.name),
                    datasets: [{
                        label: 'Revenue distribution',
                        data: revenue.map(r => r.revenue),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(255, 206, 86, 0.7)',
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(153, 102, 255, 0.7)',
                            'rgba(255, 159, 64, 0.7)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            })
        }
    } catch (err) {
        message.value = err.response?.data?.message || 'Failed to fetch analytics'
        isSuccess.value = false
    }
}

onMounted(() => {
    fetchSummary()
})
</script>

<template>
    <div>
        <h3 class="mb-4">Organizer Dashboard Analytics</h3>

        <div v-if="message" class="alert mb-3" :class="isSuccess ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>

        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Event Occupancy (Seats Booked vs Capacity)</h5>
                        <div style="height: 320px;">
                            <canvas ref="occupancyChartRef"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6 mb-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5 class="card-title mb-3">Revenue Distribution ($)</h5>
                        <div style="height: 320px;">
                            <canvas ref="revenueChartRef"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
