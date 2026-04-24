<script setup lang="ts">
import { useTravelSuggestions } from './composables/useTravelsSuggestions.ts'
import TravelForm from './components/TravelForm.vue'
import DestinationCard from './components/DestinationCard.vue'
import type { SuggestionRequest } from './types'

const { state, result, error, fetchSuggestions, reset } = useTravelSuggestions()

function handleSubmit(req: SuggestionRequest) {
  fetchSuggestions(req)
}
</script>

<template>
  <div class="app">
    <header class="header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-icon">✦</span>
          <span class="logo-text">WANDR</span>
        </div>
        <p class="tagline-header">AI-powered travel suggestions, tailored to you.</p>
      </div>
      <div class="header-deco" aria-hidden="true">
        <span>PAR</span><span>TYO</span><span>NYC</span><span>BKK</span><span>CPT</span>
      </div>
    </header>

    <main class="main">
      <Transition name="fade" mode="out-in">
        <!-- FORM STATE -->
        <section v-if="state === 'idle'" key="form" class="form-section">
          <h1 class="headline">Where should<br /><em>you</em> go next?</h1>
          <TravelForm @submit="handleSubmit" />
        </section>

        <!-- LOADING STATE -->
        <section v-else-if="state === 'loading'" key="loading" class="loading-section">
          <div class="loader">
            <div class="globe">🌍</div>
            <p>Curating your perfect destinations…</p>
          </div>
        </section>

        <!-- RESULTS STATE -->
        <section v-else-if="state === 'success' && result" key="results" class="results-section">
          <div class="results-header">
            <h2>Your Destinations</h2>
            <button class="back-btn" @click="reset">← Start Over</button>
          </div>
          <div class="cards-grid">
            <DestinationCard
              v-for="(dest, i) in result.destinations"
              :key="dest.city"
              :destination="dest"
              :index="i"
            />
          </div>
          <div class="pro-tip">
            <span class="tip-label">✦ PRO TIP</span>
            <p>{{ result.travel_tip }}</p>
          </div>
        </section>

        <!-- ERROR STATE -->
        <section v-else-if="state === 'error'" key="error" class="error-section">
          <p class="error-msg">⚠ {{ error }}</p>
          <button class="back-btn" @click="reset">Try Again</button>
        </section>
      </Transition>
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --ink: #0e0c0a;
  --paper: #f5f0e8;
  --sand: #e8dfc8;
  --accent: #c8452a;
  --gold: #b8962e;
  --muted: #7a6f5e;
  --card-bg: #fff;
  --radius: 2px;
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'DM Sans', sans-serif;
}

html, body { height: 100%; }

body {
  background: var(--paper);
  color: var(--ink);
  font-family: var(--font-body);
  font-weight: 300;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

/* HEADER */
.header {
  border-bottom: 1px solid var(--sand);
  padding: 0 2rem;
  background: var(--paper);
  position: sticky;
  top: 0;
  z-index: 10;
}
.header-inner {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 0;
}
.logo { display: flex; align-items: center; gap: 0.5rem; }
.logo-icon { color: var(--accent); font-size: 1.2rem; }
.logo-text { font-family: var(--font-display); font-size: 1.4rem; letter-spacing: 0.15em; }
.tagline-header { font-size: 0.8rem; color: var(--muted); letter-spacing: 0.05em; border-left: 1px solid var(--sand); padding-left: 1.5rem; }
.header-deco {
  padding: 0.4rem 0;
  display: flex;
  gap: 1.5rem;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  color: var(--sand);
  overflow: hidden;
  max-width: 900px;
  margin: 0 auto;
  padding-bottom: 0.5rem;
}

/* MAIN */
.main { max-width: 900px; margin: 0 auto; padding: 3rem 2rem; }

/* FORM SECTION */
.headline {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 6vw, 4rem);
  line-height: 1.1;
  margin-bottom: 2.5rem;
}
.headline em { color: var(--accent); font-style: italic; }

.form { display: flex; flex-direction: column; gap: 2rem; }
.section-label {
  display: block;
  font-size: 0.7rem;
  font-weight: 500;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.75rem;
}
.hint { font-weight: 300; text-transform: none; letter-spacing: 0; }

.pill-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.pill {
  background: transparent;
  border: 1px solid var(--sand);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 0.85rem;
  padding: 0.45rem 1rem;
  border-radius: 99px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.pill:hover { border-color: var(--ink); }
.pill.active { background: var(--ink); color: var(--paper); border-color: var(--ink); }

.row-section { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }
select {
  width: 100%;
  background: transparent;
  border: 1px solid var(--sand);
  border-radius: var(--radius);
  font-family: var(--font-body);
  font-size: 0.9rem;
  color: var(--ink);
  padding: 0.6rem 0.75rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%237a6f5e' stroke-width='1.5' fill='none'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
}

.cta {
  align-self: flex-start;
  background: var(--accent);
  color: white;
  border: none;
  font-family: var(--font-body);
  font-size: 0.9rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  padding: 0.85rem 2rem;
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.15s ease;
  margin-top: 0.5rem;
}
.cta:hover:not(:disabled) { background: #a83820; transform: translateY(-1px); }
.cta:disabled { opacity: 0.4; cursor: not-allowed; }

/* LOADING */
.loading-section { display: flex; justify-content: center; padding: 5rem 0; }
.loader { text-align: center; }
.globe {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
  animation: spin 3s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loader p { color: var(--muted); font-size: 0.9rem; letter-spacing: 0.05em; }

/* RESULTS */
.results-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 2rem;
}
.results-header h2 {
  font-family: var(--font-display);
  font-size: 2rem;
}
.back-btn {
  background: none;
  border: none;
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--muted);
  cursor: pointer;
  letter-spacing: 0.02em;
  transition: color 0.15s;
}
.back-btn:hover { color: var(--ink); }

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

/* CARD */
.card {
  background: var(--card-bg);
  border: 1px solid var(--sand);
  padding: 1.5rem;
  border-radius: var(--radius);
  animation: slideUp 0.4s ease both;
  animation-delay: var(--delay, 0ms);
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; }
.city { font-family: var(--font-display); font-size: 1.4rem; line-height: 1.1; }
.country { font-size: 0.75rem; color: var(--muted); letter-spacing: 0.05em; display: block; margin-top: 0.2rem; }
.index-badge {
  font-family: var(--font-display);
  font-size: 2rem;
  color: var(--sand);
  line-height: 1;
  flex-shrink: 0;
}
.tagline {
  font-style: italic;
  font-size: 0.85rem;
  color: var(--accent);
  margin-bottom: 0.75rem;
  line-height: 1.4;
}
.why { font-size: 0.85rem; color: var(--muted); margin-bottom: 1rem; line-height: 1.6; }
.highlights {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  margin-bottom: 1rem;
}
.highlights li { font-size: 0.8rem; padding-left: 1rem; position: relative; }
.highlights li::before { content: '→'; position: absolute; left: 0; color: var(--gold); }
.meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: var(--muted);
  border-top: 1px solid var(--sand);
  padding-top: 0.75rem;
}

/* PRO TIP */
.pro-tip {
  border: 1px solid var(--gold);
  border-left: 3px solid var(--gold);
  padding: 1rem 1.25rem;
  border-radius: var(--radius);
}
.tip-label { font-size: 0.65rem; letter-spacing: 0.2em; color: var(--gold); font-weight: 500; display: block; margin-bottom: 0.4rem; }
.pro-tip p { font-size: 0.875rem; color: var(--muted); }

/* ERROR */
.error-section { text-align: center; padding: 4rem 0; }
.error-msg { color: var(--accent); margin-bottom: 1.5rem; }

/* TRANSITIONS */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 600px) {
  .row-section { grid-template-columns: 1fr; }
  .cards-grid { grid-template-columns: 1fr; }
  .header-deco { display: none; }
}
</style>
