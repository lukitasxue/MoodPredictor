<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'
import { computed } from 'vue'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
)

const props = defineProps({
  history: Array
})

const chartData = computed(() => {
  const labels = props.history?.map(entry => entry.date) || []
  const data = props.history?.map(entry => entry.moodScore) || []

  return {
    labels,
    datasets: [
      {
        label: 'Mood Score',
        data,
        fill: false,
        tension: 0.3,
        borderColor: 'rgba(75,192,192,1)',
        backgroundColor: '#4bc0c0',
      },
    ],
  }
})



const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      min: 0,
      max: 10
    }
  }
}
</script>

<template>
  <div style="height: 300px;" v-if="chartData.labels.length > 0">
    <Line :data="chartData" :options="chartOptions" />
  </div>

</template>
