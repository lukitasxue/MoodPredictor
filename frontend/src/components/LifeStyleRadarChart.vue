<template>
    <div class="radar-container">
      <Radar :data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script setup>
  import { Radar } from 'vue-chartjs';
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
  } from 'chart.js';
  
  import { computed } from 'vue';
  
  ChartJS.register(Title, Tooltip, Legend, RadialLinearScale, PointElement, LineElement, Filler);
  
  const props = defineProps({ averages: Object });
  
  const recommended = {
    sleep_hours: 8,
    stress_level: 3,
    nutrition_quality: 7,
    social_minutes: 60,
    water_liters: 2,
  };
  
  // Normalize lifestyle values to a 0–10 scale for better comparison
  function normalize(value, max) {
    return Math.min((value / max) * 10, 10);
  }
  console.log("Radar Averages:", props.averages);

  const labels = ['Sleep Hours', 'Stress Level', 'Nutrition Quality', 'Social Minutes', 'Water Liters'];


  const normalizedUser = computed(() => [
    normalize(props.averages.sleep_hours ?? 0, 10),
    normalize(props.averages.stress_level ?? 0, 10),
    normalize(props.averages.nutrition_quality ?? 0, 10),
    normalize(props.averages.social_minutes ?? 0, 120),
    normalize(props.averages.water_liters ?? 0, 3) 
  ])

  
  const normalizedRecommended = [
    normalize(recommended.sleep_hours, 10),
    normalize(recommended.stress_level, 10),
    normalize(recommended.nutrition_quality, 10),
    normalize(recommended.social_minutes, 120),
    normalize(recommended.water_liters, 3),
  ];
  

  
  const chartData = computed(() => ({
    labels,
    datasets: [
      {
        label: 'Your Averages',
        data: normalizedUser.value,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2
      },
      {
        label: 'Recommended',
        data: normalizedRecommended,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2
      }
    ]
  }));
  
  const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      min: 0,
      max: 10,
      ticks: {
        stepSize: 2,
        color: '#ccc',
        backdropColor: 'transparent',
      },
      pointLabels: {
        color: '#ccc',
      },
      grid: {
        color: '#555',
      }
    }
  },
  plugins: {
    legend: {
      labels: {
        color: '#ccc',
        font: { size: 14 },
      }
    },
    tooltip: {
      callbacks: {
        label: function (context) {
          const label = context.label;
          const datasetLabel = context.dataset.label || '';
          const normalizedValue = context.raw;

          // Map back to original values
          const originalAverages = context.dataset.label === 'Your Averages'
            ? props.averages
            : recommended;

          let originalValue;
          switch (label) {
            case 'Sleep Hours':
              originalValue = `${(originalAverages.sleep_hours ?? 0).toFixed(1)} hours`;
              break;
            case 'Stress Level':
              originalValue = `${(originalAverages.stress_level ?? 0).toFixed(1)} level`;
              break;
            case 'Nutrition Quality':
              originalValue = `${(originalAverages.nutrition_quality ?? 0).toFixed(1)} score`;
              break;
            case 'Social Minutes':
              originalValue = `${(originalAverages.social_minutes ?? 0).toFixed(1)} mins`;
              break;
            case 'Water Liters':
              originalValue = `${(originalAverages.water_liters ?? 0).toFixed(1)} L`;
              break;
            default:
              originalValue = normalizedValue.toFixed(1);
          }

          return `${datasetLabel}: ${originalValue}`;
        }
      }
    }
  }
};




  </script>
  
  <style scoped>
  .radar-container {
    width: 100%;
    max-width: 600px;
    height: 400px;
    margin: 0 auto;
  }
  </style>
  