import { ref } from 'vue'
import type { SuggestionRequest, SuggestionResponse, LoadingState } from '../types'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export function useTravelSuggestions() {
  const state = ref<LoadingState>('idle')
  const result = ref<SuggestionResponse | null>(null)
  const error = ref<string | null>(null)

  async function fetchSuggestions(req: SuggestionRequest): Promise<void> {
    state.value = 'loading'
    error.value = null
    result.value = null

    try {
      const res = await fetch(`${API_BASE}/suggest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req),
      })

      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail ?? `HTTP ${res.status}`)
      }

      result.value = await res.json()
      state.value = 'success'
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Unknown error'
      state.value = 'error'
    }
  }

  function reset() {
    state.value = 'idle'
    result.value = null
    error.value = null
  }

  return { state, result, error, fetchSuggestions, reset }
}