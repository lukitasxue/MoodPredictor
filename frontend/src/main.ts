import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import MenuPage from './components/MenuPage.vue'
import MoodAnalyzer from './components/MoodAnalyzer.vue'

const routes = [
  { path: '/', component: MenuPage },
  { path: '/analyzer', component: MoodAnalyzer }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')
