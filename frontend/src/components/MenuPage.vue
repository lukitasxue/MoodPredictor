<template>
  <div class="menu-container">
    <h1>Welcome to the Mood Analyzer App</h1>

    <p class="delay-warning">
      Note: The app may take up to 40 seconds to start due to free hosting startup time.
    </p>

    <section>
      <h2>About This App</h2>
      <p>
        This web app lets you log your daily lifestyle habits and predicts your mood using a custom multivariable linear regression model (built from scratch using NumPy). 
        You can manually enter data, generate mock logs, view your full prediction history, and analyze insights through graphs.
      </p>
    </section>

    <section class="tutorial-section">
      <h2>Quick Tutorial</h2>
      <ol>
        <li><strong>Back to Menu (Top-Left):</strong> Allows you to return to this main info page from anywhere in the app.</li>
        <li>
          <strong>Manual Mood Logger:</strong> Use the sliders to enter your daily data including sleep, stress, water, nutrition, and social interaction. 
          When you click <em>Predict Mood</em>, the app will estimate your mood score based on your inputs.
        </li>
        <li>
          <strong>Auto Log Generator + History:</strong> 
          Use the <em>Generate Test Logs</em> button to create multiple entries between two dates for testing. The <em>Mood History</em> below it shows all your mood logs.
        </li>
        <li>
          <strong>Graphs & Insights:</strong> 
          Explore how your mood changes over time, compare your habits to recommended values, and see which factors impact your mood most.
        </li>
      </ol>
      <img src="/guide.jpg" alt="Tutorial Layout" class="tutorial-image" />
    </section>

    <section>
      <h2>Input Variable Guide</h2>
      <ul>
        <li><strong>Sleep Hours:</strong> Number of hours slept last night. (~8 hours recommended)</li>
        <li><strong>Stress Level:</strong> Ranges from 0 (no stress) to 10 (extreme stress). Lower is better.</li>
        <li><strong>Nutrition Quality:</strong> Scored from 0 to 10 based on diet quality. Higher is better.</li>
        <li><strong>Social Minutes:</strong> Minutes spent socializing (0–180). Balanced interaction improves mood.</li>
        <li><strong>Water Liters:</strong> Water intake from 0 to 3L. Aim for at least 2L/day.</li>
      </ul>
      <p><strong>Predicted Mood Score:</strong> Ranges from 1 (very poor mood) to 10 (very good mood).</p>
    </section>

    <section>
      <h2>Graph Insights</h2>
      <ul>
        <li><strong>Mood Trend:</strong> Line chart of mood changes over time.</li>
        <li><strong>Lifestyle Radar:</strong> Compares your habits to recommended levels.</li>
        <li><strong>Impact Chart:</strong> Shows how each input variable affects mood prediction.</li>
      </ul>
    </section>

    <button @click="goToApp" class="start-button">Enter the App</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

function goToApp() {
  router.push('/analyzer')
}
</script>

<style scoped>
.menu-container {
  max-width: 850px;
  margin: auto;
  padding: 2rem;
  text-align: left;
  color: white;
  font-family: 'Segoe UI', sans-serif;
}

h1 {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 1.2rem;
}

h2 {
  color: #a18aff;
  margin-top: 2rem;
  margin-bottom: 0.5rem;
}

ul, ol {
  margin-left: 1.5rem;
  line-height: 1.6;
}

.delay-warning {
  font-style: italic;
  margin-top: -1rem;
  margin-bottom: 1.5rem;
  color: #ccc;
  text-align: center;
}

.start-button {
  display: block;
  margin: 3rem auto 0 auto;
  background-color: #8265f2;
  color: white;
  font-size: 1.2rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}
.start-button:hover {
  background-color: #a18aff;
}

.tutorial-section {
  margin-bottom: 2rem;
}


.tutorial-image {
  margin-top: 1.5rem;
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}


</style>

