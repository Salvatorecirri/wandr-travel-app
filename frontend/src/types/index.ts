export interface SuggestionRequest {
  mood: string
  budget: 'budget' | 'mid-range' | 'luxury'
  duration: 'weekend' | 'week' | 'two-weeks'
  interests: string[]
  climate: 'tropical' | 'cold' | 'temperate' | 'desert'
}

export interface Destination {
  city: string
  country: string
  tagline: string
  why: string
  highlights: string[]
  best_time: string
  estimated_cost: string
}

export interface SuggestionResponse {
  destinations: Destination[]
  travel_tip: string
}

export type LoadingState = 'idle' | 'loading' | 'success' | 'error'