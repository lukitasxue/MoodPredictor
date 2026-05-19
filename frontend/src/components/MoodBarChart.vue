<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
} from 'chart.js'
import { computed, watch } from 'vue'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, BarElement)

const props = defineProps({ moodHistory: Array })

// Simplified correlation: how much each value varies with mood
const correlations = computed(() => {
  if (!props.moodHistory || props.moodHistory.length < 2) return {}

  const keys = ['sleep_hours', 'stress_level', 'nutrition_quality', 'social_minutes', 'water_effect']
  const moodAvg = props.moodHistory.reduce((a, b) => a + b.moodScore, 0) / props.moodHistory.length

  const result = {}

  keys.forEach(key => {
    const avg = props.moodHistory.reduce((a, b) => a + b[key], 0) / props.moodHistory.length
    const cov = props.moodHistory.reduce((sum, entry) => sum + (entry[key] - avg) * (entry.moodScore - moodAvg), 0)
    const varKey = props.moodHistory.reduce((sum, entry) => sum + (entry[key] - avg) ** 2, 0)
    result[key] = varKey ? cov / varKey : 0
  })

  return result
})
watch(() => props.moodHistory, (val) => {
  console.log("Bar Chart History Sample:", val.slice(0, 3));
})


const labels = Object.keys(correlations.value).map(k =>
  k.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
);

const chartData = computed(() => {
  const values = Object.values(correlations.value);

  return {
    labels: Object.keys(correlations.value).map(k =>
      k === 'water_effect'
        ? 'Hydration Effect'
        : k.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    ),
    datasets: [{
      label: 'Estimated Impact on Mood',
      data: values,
      backgroundColor: values.map(val =>
        val >= 0 ? 'rgba(75, 192, 192, 0.6)' : 'rgba(255, 99, 132, 0.6)'
      ),
      borderRadius: 4
    }]
  };
});




const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Relative Influence'
      }
    }
  }
}
</script>

<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>
