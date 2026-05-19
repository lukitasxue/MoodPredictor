<template>
  <main class="menu-page">
    <section class="hero-shell">
      <div class="hero-copy">
        <p class="eyebrow">Mood Predictor</p>
        <h1>Ever wondered why your mood feels off?</h1>
        <p class="hero-text">
          Log a few daily habits and see how sleep, stress, nutrition, social time, and hydration may be shaping your mood.
        </p>

        <div class="hero-actions">
          <button @click="goToApp" class="primary-action">Test My Mood</button>
          <a href="#how-it-works" class="secondary-action">How it works</a>
        </div>
      </div>

      <div class="hero-panel" aria-label="Mood prediction preview">
        <div class="score-card">
          <span>Predicted Mood</span>
          <strong>7.4</strong>
        </div>
        <div class="signal-list">
          <div>
            <span>Sleep</span>
            <strong>Positive</strong>
          </div>
          <div>
            <span>Stress</span>
            <strong>Negative</strong>
          </div>
          <div>
            <span>Hydration</span>
            <strong>Positive</strong>
          </div>
        </div>
      </div>
    </section>

    <section id="how-it-works" class="content-band">
      <div class="section-heading">
        <p class="eyebrow">Quick Start</p>
        <h2>Three steps, no spreadsheet required</h2>
      </div>
      <div class="steps-grid">
        <article>
          <span>1</span>
          <h3>Enter today's habits</h3>
          <p>Move the sliders for sleep, stress, nutrition, social minutes, and water intake.</p>
        </article>
        <article>
          <span>2</span>
          <h3>Predict your mood</h3>
          <p>The FastAPI backend runs a NumPy regression model and returns a score from 1 to 10.</p>
        </article>
        <article>
          <span>3</span>
          <h3>Read the patterns</h3>
          <p>Charts compare your logs over time and estimate which habits are moving your mood most.</p>
        </article>
      </div>
    </section>

    <section class="content-band split-band">
      <div>
        <p class="eyebrow">What The Model Watches</p>
        <h2>Simple inputs with real signal</h2>
        <p>
          The model was trained on lifestyle rows with mood scores. It learns weights for each variable, so positive weights lift the prediction and negative weights pull it down.
        </p>
      </div>
      <div class="factor-grid">
        <article>
          <h3>Sleep</h3>
          <p>One of the strongest positive drivers in the current model.</p>
        </article>
        <article>
          <h3>Stress</h3>
          <p>The clearest negative driver. Higher stress usually lowers the prediction.</p>
        </article>
        <article>
          <h3>Nutrition</h3>
          <p>Better nutrition quality tends to support a higher mood score.</p>
        </article>
        <article>
          <h3>Hydration</h3>
          <p>Water is modeled with a hydration-effect curve, with around 2L as the sweet spot.</p>
        </article>
        <article>
          <h3>Social Time</h3>
          <p>A smaller signal in this dataset, but still tracked in your personal logs.</p>
        </article>
      </div>
    </section>

    <section class="content-band note-band">
      <div>
        <p class="eyebrow">Tip</p>
        <h2>More logs make better insights</h2>
        <p>
          A single prediction is useful, but the charts get more interesting after several days. Use the test-log generator if you want to preview the insights quickly.
        </p>
      </div>
      <button @click="goToApp" class="primary-action">Open The App</button>
    </section>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goToApp() {
  router.push('/analyzer')
}
</script>
