<script setup lang="ts">
import { reactive } from 'vue'
import type { SuggestionRequest } from '../types'

const emit = defineEmits<{ submit: [req: SuggestionRequest] }>()

const INTERESTS = ['Food & Wine', 'History', 'Adventure', 'Beaches', 'Art & Culture', 'Nightlife', 'Nature', 'Architecture']
const MOODS = ['Relaxed & Slow', 'Active & Packed', 'Romantic', 'Solo Explorer', 'Family Fun']

const form = reactive<SuggestionRequest>({
  mood: '',
  budget: 'mid-range',
  duration: 'week',
  interests: [],
  climate: 'temperate',
})

function toggleInterest(i: string) {
  const idx = form.interests.indexOf(i)
  if (idx === -1) form.interests.push(i)
  else form.interests.splice(idx, 1)
}

function submit() {
  if (!form.mood || form.interests.length === 0) return
  emit('submit', { ...form })
}
</script>

<template>
  <form class="form" @submit.prevent="submit">
    <section>
      <label class="section-label">Vibe</label>
      <div class="pill-grid">
        <button v-for="m in MOODS" :key="m" type="button" class="pill"
          :class="{ active: form.mood === m }" @click="form.mood = m">{{ m }}</button>
      </div>
    </section>

    <section class="row-section">
      <div>
        <label class="section-label">Budget</label>
        <select v-model="form.budget">
          <option value="budget">Budget</option>
          <option value="mid-range">Mid-range</option>
          <option value="luxury">Luxury</option>
        </select>
      </div>
      <div>
        <label class="section-label">Duration</label>
        <select v-model="form.duration">
          <option value="weekend">Weekend</option>
          <option value="week">1 Week</option>
          <option value="two-weeks">2 Weeks</option>
        </select>
      </div>
      <div>
        <label class="section-label">Climate</label>
        <select v-model="form.climate">
          <option value="tropical">Tropical</option>
          <option value="cold">Cold</option>
          <option value="temperate">Temperate</option>
          <option value="desert">Desert</option>
        </select>
      </div>
    </section>

    <section>
      <label class="section-label">Interests <span class="hint">(pick at least one)</span></label>
      <div class="pill-grid">
        <button v-for="i in INTERESTS" :key="i" type="button" class="pill"
          :class="{ active: form.interests.includes(i) }" @click="toggleInterest(i)">{{ i }}</button>
      </div>
    </section>

    <button type="submit" class="cta" :disabled="!form.mood || form.interests.length === 0">
      Find My Destinations →
    </button>
  </form>
</template>