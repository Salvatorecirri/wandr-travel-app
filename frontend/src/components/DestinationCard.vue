<script setup lang="ts">
import type { Destination } from '../types'
defineProps<{ destination: Destination; index: number }>()
</script>

<template>
  <article class="card" :style="{ '--delay': `${index * 120}ms` }">
    <div class="card-header">
      <div class="city-info">
        <h2 class="city">{{ destination.city }}</h2>
        <span class="country">{{ destination.country }}</span>
      </div>
      <span class="index-badge">0{{ index + 1 }}</span>
    </div>
    <p class="tagline">"{{ destination.tagline }}"</p>
    <p class="why">{{ destination.why }}</p>
    <ul class="highlights">
      <li v-for="h in destination.highlights" :key="h">{{ h }}</li>
    </ul>
    <div class="meta">
      <span>🗓 {{ destination.best_time }}</span>
      <span>💰 {{ destination.estimated_cost }}</span>
    </div>
  </article>
</template>