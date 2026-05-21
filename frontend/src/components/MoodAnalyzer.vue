<script setup>
import Datepicker from 'vue3-datepicker';
import { ref, computed, onMounted, watch } from 'vue';
import { predictMood } from '../api.js';
import MoodLineChart from './MoodLineChart.vue';
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
import RadarChart from './LifeStyleRadarChart.vue';

import MoodBarChart from './MoodBarChart.vue'
import { createRouter, createWebHistory, useRouter } from 'vue-router'
import MenuPage from './MenuPage.vue'

const router = useRouter()

function goBackToMenu() {
  router.push('/')
}



function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // JS months are 0-indexed
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function addMonths(date, months) {
  const result = new Date(date);
  result.setMonth(result.getMonth() + months);
  return result;
}


ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)
// Initial input values
const input = ref({
  sleep_hours: 7,
  stress_level: 3,
  nutrition_quality: 5,
  social_minutes: 60,
  water_liters: 2,
});


// Reactive state
const moodScore = ref(null);
const isPredicting = ref(false);
const backendSeconds = ref(0);
const predictionMessage = ref('');
const moodHistory = ref([]);
const selectedDate = ref(new Date()); // store as Date object
const genStart = ref(new Date())
const genEnd = ref(addMonths(new Date(), 2))
const csvData = ref([]) // Filled later
const currentPage = ref(1)
const itemsPerPage = 7
const paginatedHistory = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return moodHistory.value.slice(start, end)
})

const totalPages = computed(() =>
  Math.ceil(moodHistory.value.length / itemsPerPage)
)

const moodScaleMin = 1;
const moodScaleMax = 5;

const moodScoreNumber = computed(() => {
  if (moodScore.value === null) return null;
  const score = Number(moodScore.value);
  return Number.isFinite(score) ? score : null;
});

const moodScalePosition = computed(() => {
  if (moodScoreNumber.value === null) return '0%';
  const clampedScore = Math.min(Math.max(moodScoreNumber.value, moodScaleMin), moodScaleMax);
  const percent = ((clampedScore - moodScaleMin) / (moodScaleMax - moodScaleMin)) * 100;
  return `${percent}%`;
});

const moodInterpretation = computed(() => {
  const score = moodScoreNumber.value;
  if (score === null) return null;

  if (score >= 4.5) {
    return {
      label: 'Excellent mood',
      description: 'This is close to the top of the scale. A 5.0 means the model thinks your mood is about as positive as it gets.'
    };
  }

  if (score >= 3.5) {
    return {
      label: 'Good mood',
      description: 'The prediction is above average, so your inputs point toward a generally positive day.'
    };
  }

  if (score >= 2.5) {
    return {
      label: 'Okay or mixed mood',
      description: 'This sits around the middle of the scale. Some lifestyle signals may be helping, while others may be pulling the score down.'
    };
  }

  if (score >= 1.5) {
    return {
      label: 'Low mood',
      description: 'The prediction is below average. The model sees a few warning signs in the current inputs.'
    };
  }

  return {
    label: 'Very low mood',
    description: 'This is near the bottom of the scale. A 1.0 means the model thinks the day is likely to feel pretty rough.'
  };
});

const insights = computed(() => {
  const history = moodHistory.value
  if (!history.length) return null

  const sorted = [...history].sort((a, b) => new Date(a.date) - new Date(b.date))
  const scores = sorted.map(entry => entry.moodScore)

  // --- General Trend (based on halves average) ---
  const midpoint = Math.floor(scores.length / 2)
  const firstHalf = scores.slice(0, midpoint)
  const secondHalf = scores.slice(midpoint)

  const avg = arr => arr.reduce((a, b) => a + b, 0) / arr.length
  const generalTrend = avg(secondHalf) - avg(firstHalf || [0]) // avoid div by 0

  // --- Recent Trend (last 3 days) ---
  const recent = scores.slice(-3)
  let recentTrend = null
  if (recent.length === 3) {
    recentTrend = recent[2] - recent[0]
  } else if (recent.length === 2) {
    recentTrend = recent[1] - recent[0]
  }

  // --- Best & Worst Moods ---
  const maxScore = Math.max(...scores)
  const minScore = Math.min(...scores)
  const maxEntry = sorted.find(e => e.moodScore === maxScore)
  const minEntry = sorted.find(e => e.moodScore === minScore)

  // --- Stability (Standard Deviation) ---
  const mean = avg(scores)
  const variance = scores.reduce((acc, val) => acc + (val - mean) ** 2, 0) / scores.length
  const stdDev = Math.sqrt(variance)

  return {
    generalTrend,
    generalTrendText:
      generalTrend > 0.5 ? 'Mood is improving'
      : generalTrend < -0.5 ? 'Mood is declining'
      : 'Mood is steady',

    recentTrend,
    recentTrendText:
      recentTrend == null ? 'Not enough data for recent trend'
      : recentTrend > 0.5 ? 'Recently improved mood'
      : recentTrend < -0.5 ? 'Recent dip in mood'
      : 'Recent mood is steady',

    maxScore,
    maxDate: maxEntry?.date,
    minScore,
    minDate: minEntry?.date,
    stdDev: stdDev.toFixed(2),
    stability: stdDev < 1 ? 'Very Stable' : stdDev < 2 ? 'Moderately Stable' : 'Unstable'
  }
})
const lifestyleAverages = computed(() => {
  if (!moodHistory.value.length) return {};

  const totals = {
    sleep_hours: 0,
    stress_level: 0,
    nutrition_quality: 0,
    social_minutes: 0,
    water_liters: 0,
    water_effect: 0,
  };

  moodHistory.value.forEach(entry => {
    for (const key in totals) {
      totals[key] += entry[key] ?? 0;
    }
  });

  const count = moodHistory.value.length;
  const averages = {};
  for (const key in totals) {
    averages[key] = parseFloat((totals[key] / count).toFixed(2));
  }

  return averages;
});
const barChartInsights = computed(() => {
  const insights = [];

  if (!moodHistory.value.length) return insights;

  const { sleep_hours, stress_level, water_liters } = lifestyleAverages.value;

  if (sleep_hours < 7) insights.push("You might benefit from more sleep (target 8h).");
  if (water_liters < 1.5) insights.push("Hydration is low. Aim for at least 1L of water.");
  if (stress_level > 5) insights.push("Stress levels are high – take breaks and relax.");

  return insights;
});
const radarInsights = computed(() => {
  const rec = {
    sleep_hours: 8,
    stress_level: 3,
    nutrition_quality: 7,
    social_minutes: 60,
    water_liters: 2,
  };

  if (!lifestyleAverages.value || !Object.keys(lifestyleAverages.value).length) return [];

  const msgs = [];

  const diff = (actual, target) => (actual - target).toFixed(1);

  msgs.push(`Average sleep: ${lifestyleAverages.value.sleep_hours}h. ${lifestyleAverages.value.sleep_hours < rec.sleep_hours ? 'Below' : 'Above'} recommended 8h.`);
  msgs.push(`Average stress: ${lifestyleAverages.value.stress_level} / 10. Recommended ≤ 3.`);
  msgs.push(`Average nutrition: ${lifestyleAverages.value.nutrition_quality} / 10. Recommended ≥ 7.`);
  msgs.push(`Average social time: ${lifestyleAverages.value.social_minutes} min. Recommended: 60 min/day.`);
  msgs.push(`Average water intake: ${lifestyleAverages.value.water_liters}L. Recommended: 2L/day.`);

  return msgs;
});
const barChartExplanation = computed(() => {
  const history = moodHistory.value;
  if (!history.length) return [];

  const explanation = [];

  // Data sufficiency warning
  if (history.length < 14) {
    explanation.push("Note: Fewer than 2 weeks of logs may lead to inaccurate lifestyle-mood correlations. Try to log for at least a month.");
  }

  // Example correlation direction (mock logic, adapt to your actual bar data)
  // If you're using a correlation map for the bar chart, adjust the following logic to access real values
  const dummyCorrelations = {
    sleep_hours: 0.5,
    stress_level: -0.4,
    nutrition_quality: 0.1,
    social_minutes: 0.01,
    water_effect: 0.45,
  };

  for (const [key, value] of Object.entries(dummyCorrelations)) {
    if (Math.abs(value) < 0.1) continue; // Skip weak effects

    let factor = key.replace('_', ' ');
    let direction = value > 0 ? 'positively' : 'negatively';
    let msg = `Your data suggests that ${factor.replace('_', ' ')} ${direction} influences your mood.`;

    // Customize message based on factor
    if (key === 'sleep_hours') msg += " Getting more sleep tends to improve your mood.";
    if (key === 'stress_level') msg += " High stress appears to reduce mood.";
    if (key === 'nutrition_quality') msg += " Better nutrition might help slightly.";
    if (key === 'social_minutes') msg += " Social time has a neutral impact based on current data.";
    if (key === 'water_effect') msg += " Staying hydrated seems to improve mood significantly.";

    explanation.push(msg);
  }

  return explanation;
});




watch(lifestyleAverages, (val) => {
  console.log("Lifestyle Averages:", val)
})

watch(barChartInsights, (val) => {
  console.log("Bar chart insights:", val)
})
const getLabel = (key) =>
  key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');







// Helpers
function generateTestLogs() {
  const start = new Date(genStart.value)
  const end = new Date(genEnd.value)
  const days = []

  while (start <= end) {
    days.push(new Date(start))
    start.setDate(start.getDate() + 1)
  }

  const history = JSON.parse(localStorage.getItem('mood_history') || '{}')

  days.forEach(day => {
    const randomRow = csvData.value[Math.floor(Math.random() * csvData.value.length)]
    const dateKey = formatDate(day)

    const waterLiters = Number(randomRow.water_liters);
    const water_effect = !isNaN(waterLiters)
      ? -1 * (waterLiters - 2.0) ** 2 + 2.0 + 1.0
      : 0;  // fallback value if invalid


      history[dateKey] = {
      ...randomRow,
      date: dateKey,
      water_liters: waterLiters,
      water_effect,
    };

  })

  // Update moodHistory immediately
  moodHistory.value = Object.values(history).sort((a, b) =>
    new Date(a.date) - new Date(b.date)
  )

  localStorage.setItem('mood_history', JSON.stringify(
    Object.fromEntries(moodHistory.value.map(e => [e.date, e]))
  ))
}




// Handle prediction + localStorage overwrite by date
async function handleSubmit() {
  isPredicting.value = true;
  backendSeconds.value = 0;
  predictionMessage.value = 'Backend initializing. This can take around 60 seconds on the free Render service. Meanwhile, look around the interface or generate logs if you want to test the insights.';
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), 90000);
  const timerId = window.setInterval(() => {
    backendSeconds.value += 1;
  }, 1000);

  try {
    const result = await predictMood(input.value, { signal: controller.signal });

    if (!result || typeof result.predicted_mood_score !== 'number') {
      throw new Error("Invalid prediction result");
    }

    moodScore.value = result.predicted_mood_score.toFixed(2);

    const entryKey = formatDate(selectedDate.value);
    const water_effect = -1 * (input.value.water_liters - 2.0) ** 2 + 2.0 + 1.0;

    const newEntry = {
      ...input.value,
      water_effect,
      moodScore: parseFloat(moodScore.value),
      date: entryKey,
    };

    // Load and update history
    let history = {};
    const saved = localStorage.getItem('mood_history');
    if (saved) {
      try {
        history = JSON.parse(saved);
      } catch {
        history = {};
      }
    }

    history[entryKey] = newEntry;

    localStorage.setItem('mood_history', JSON.stringify(history));
    moodHistory.value = Object.values(history).sort((a, b) =>
      new Date(a.date) - new Date(b.date)
    );
    predictionMessage.value = '';

  } catch (error) {
    console.error('Error predicting mood:', error);
    predictionMessage.value = 'The backend is still waking up or failed to respond. You can try Predict Mood again in a moment. Meanwhile, generate test logs to explore the charts and insights.';
  } finally {
    window.clearTimeout(timeoutId);
    window.clearInterval(timerId);
    isPredicting.value = false;
  }
}



// Load history from localStorage when app mounts
onMounted(async () => {
  const saved = localStorage.getItem('mood_history');
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      if (parsed && typeof parsed === 'object') {
        const patched = Object.values(parsed).map(entry => ({
          ...entry,
          water_effect:
            entry.water_effect !== undefined
              ? entry.water_effect
              : -1 * (entry.water_liters - 2.0) ** 2 + 2.0 + 1.0
        }));

        moodHistory.value = patched.sort((a, b) =>
          new Date(a.date) - new Date(b.date)
        );
      }
    } catch (err) {
      console.warn('Error parsing mood history:', err);
      localStorage.removeItem('mood_history');
    }
  }

  // Load mood_data.csv from public folder
  try {
    const res = await fetch('/mood_data.csv');
    const text = await res.text();

    const rows = text.trim().split('\n').slice(1);

    csvData.value = rows.map((row, i) => {
      const values = row.split(',').map(Number);

      if (values.length < 6 || values.some(isNaN)) {
        console.warn(`Row ${i} skipped due to invalid data`, row);
        return null;
      }

      const [
        sleep_hours,
        stress_level,
        nutrition_quality,
        social_minutes,
        water_liters,
        moodScore
      ] = values;

      const water_effect = -1 * (water_liters - 2.0) ** 2 + 2.0 + 1.0;

      return {
        sleep_hours,
        stress_level,
        nutrition_quality,
        social_minutes,
        water_liters,
        moodScore,
        water_effect
      };
    }).filter(Boolean);


    console.log("CSV loaded:", csvData.value.length);
  } catch (err) {
    console.error('Error loading mood_data.csv:', err);
  }
});  

watch(lifestyleAverages, (val) => {
  console.log("RadarChart will receive:", val);
})



</script>


<template>
  <div class="go-back-wrapper">
    <button class="go-back-button" @click="goBackToMenu">Back to Menu</button>
  </div>
  

  <div class="page-layout">
    <section class="analyzer-intro">
      <p class="eyebrow">Daily Check-In</p>
      <h1>Log today, then look for patterns.</h1>
      <p>Start with a single prediction or generate sample logs to preview the charts and lifestyle insights.</p>
    </section>
      
      <!-- Top Section: Manual Input + History/Generator -->
  <div class="top-grid">
    <div class="section-box">
    <!-- Manual Input -->
      <div class="manual-input">
        <h3>Manual Mood Logger</h3>
        <label for="log-date">Log Mood For:</label>
        <Datepicker v-model="selectedDate" />

        <form @submit.prevent="handleSubmit">
          <div v-for="(value, key) in input" :key="key" class="slider-row">
            <input
              type="range"
              class="slider"
              :id="key"
              v-model.number="input[key]"
              min="0"
              :max="key === 'social_minutes' ? 180 : (key === 'water_liters' ? 3 : 10)"
              step="0.1"
            />
            <label :for="key">
              {{ getLabel(key) }}: {{ input[key].toFixed(1) }}
            </label>
          </div>
          <div class="generate-button-wrapper">
            <button class="generate-button" type="submit" :disabled="isPredicting">
              {{ isPredicting ? 'Waiting for Backend...' : 'Predict Mood' }}
            </button>
          </div>
          <p v-if="predictionMessage" class="backend-status">
            {{ predictionMessage }}
            <span v-if="isPredicting">Waiting {{ backendSeconds }}s...</span>
          </p>
          <div v-if="moodScore !== null && moodInterpretation" class="prediction-result-card">
            <div class="prediction-summary">
              <span>Predicted Mood Score</span>
              <strong>{{ moodScore }}</strong>
              <p>{{ moodInterpretation.label }}</p>
            </div>

            <div class="mood-scale" aria-label="Mood score scale from 1.0 to 5.0">
              <div class="scale-track">
                <span class="scale-marker" :style="{ left: moodScalePosition }"></span>
              </div>
              <div class="scale-labels">
                <span>1.0<br />Not good</span>
                <span>3.0<br />Okay</span>
                <span>5.0<br />Perfect mood</span>
              </div>
            </div>

            <p class="prediction-explanation">{{ moodInterpretation.description }}</p>
          </div>
        </form>
      </div>
    </div>

    <div class="section-box">
      <!-- Generator + History -->
      <div class="history-logs">
        <h2>Generate Mood Logs</h2> 
        <p class="panel-hint">Want to see some insights? Generate a few days and watch the charts come alive.</p>
        <div class="date-range-container">
          <div class="date-picker-block">
            <label>Generate From:</label>
            <Datepicker v-model="genStart" />
          </div>
          <div class="date-picker-block">
            <label>To:</label>
            <Datepicker v-model="genEnd" />
          </div>
        </div>
        <div class="generate-button-wrapper">
          <button class="generate-button" @click="generateTestLogs">Generate Test Logs</button>
        </div>


        <h2>Mood History</h2>
        <ul class="history-list">
          <li v-for="entry in paginatedHistory" :key="entry.date">
            <strong>{{ entry.date }}:</strong> Mood: {{ entry.moodScore }}
          </li>
        </ul>

        <div class="pagination-controls">
          <button @click="currentPage--" :disabled="currentPage === 1">Previous</button>
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button @click="currentPage++" :disabled="currentPage === totalPages">Next</button>
        </div>
      </div>
    </div>
  </div>
    

    


    <!-- Mood Chart + Insights -->
  <div class="section-box">
    <h3>Your Mood Over Time</h3>

      <MoodLineChart :history="moodHistory" />

    <div v-if="insights" class="panel">
      <h3>Mood Insights</h3>
      <ul class="panel-list">
        <li><strong>General Trend:</strong> {{ insights.generalTrendText }}</li>
        <li><strong>Recent Trend:</strong> {{ insights.recentTrendText }}</li>
        <li><strong>Best Mood:</strong> {{ insights.maxScore }} on {{ insights.maxDate }}</li>
        <li><strong>Lowest Mood:</strong> {{ insights.minScore }} on {{ insights.minDate }}</li>
        <li><strong>Mood Stability:</strong> {{ insights.stability }} (σ = {{ insights.stdDev }})</li>
      </ul>
    </div>
  </div>

  <!-- Lifestyle Radar Chart + Scale -->
  <div class="section-box">
    <h3>Lifestyle Radar</h3>
    <div class="radar-row">

        <RadarChart :averages="lifestyleAverages" />

    </div>
    <div class="panel">
    <h3>Lifestyle Insights</h3>
    <ul class="panel-list">
      <li v-for="(line, i) in radarInsights" :key="i">{{ line }}</li>
    </ul>
    </div>
  </div>

  <!-- Chart 3 -->
  <div class="section-box">
    <h3>Lifestyle Impact on Mood</h3>
    <div class="chart-container">
      <MoodBarChart :moodHistory="moodHistory" />
    </div>
    <!-- Bar Chart Insights -->
    <div class="panel">
      <h3>Lifestyle & Mood Insights</h3>
      <ul class="insights-list">
        <li v-if="barChartInsights.length === 0">No insights generated yet.</li>

        <!-- Simple Warnings -->
        <li v-for="(insight, index) in barChartInsights" :key="'bar-basic-' + index">{{ insight }}</li>
      </ul>

      <!-- Divider -->

      <!-- Correlation Analysis -->
      <div v-if="barChartExplanation.length">
        <h4 class="analysis-heading">Impact Analysis</h4>
        <ul class="panel-list">
          <li v-for="(extra, index) in barChartExplanation" :key="'bar-explain-' + index">
            {{ extra }}
          </li>
        </ul>
      </div>

    </div>


  </div>
     

    
  </div>
</template>
