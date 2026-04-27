'''
If you want to use AI mode change in .env file:
USE_MOCK=true -> USE_MOCK=false
In mock mode, the API will return hardcoded suggestions. In AI mode, it will call the Anthropic API to generate suggestions based on the user's input (cost money)
'''

# Imports and app setup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import anthropic
from groq import Groq

import os
import json

from anthropic.types import TextBlock

from dotenv import load_dotenv
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # "groq" or "anthropic", if var in env not defined it falls back to "groq" (free)

# Mock mode for testing without incurring API costs
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"
MOCK_RESPONSE = {
    "destinations": [
        {
            "city": "Florence",
            "country": "Italy",
            "tagline": "Art, wine, and slow sunsets",
            "why": "Perfect match for relaxed culture and history lovers. Florence offers a walkable historic center, world-class museums, and incredible food.",
            "highlights": [
                "Uffizi Gallery",
                "Duomo climb",
                "Tuscan wine tasting"
            ],
            "best_time": "April-June or September-October",
            "estimated_cost": "~€1,200 for a week"
        },
        {
            "city": "Kyoto",
            "country": "Japan",
            "tagline": "Temples, gardens, and quiet mornings",
            "why": "Ideal for slow travel, cultural immersion, and peaceful exploration of temples and nature.",
            "highlights": [
                "Fushimi Inari Shrine",
                "Arashiyama Bamboo Forest",
                "Tea ceremony"
            ],
            "best_time": "March-May or October-November",
            "estimated_cost": "~€1,500 for a week"
        },
        {
            "city": "Porto",
            "country": "Portugal",
            "tagline": "River views and wine cellars",
            "why": "A relaxed European city with great food, wine, and scenic river walks.",
            "highlights": [
                "Douro River cruise",
                "Port wine cellars",
                "Old town Ribeira"
            ],
            "best_time": "May-September",
            "estimated_cost": "~€900 for a week"
        }
    ],
    "travel_tip": "For slow travel, stay in one central neighborhood and explore on foot - it completely changes the experience."
}

app = FastAPI(title="Travel Suggestion API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy-init clients based on provider to avoid unnecessary API calls in mock mode
def get_client():
    if LLM_PROVIDER == "anthropic":
        return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    else:
        return Groq(api_key=os.environ["GROQ_API_KEY"])

prompt_template = """You are a world-class travel curator. Suggest exactly 3 destinations.

Traveler profile:
- Mood/vibe: {mood}
- Budget: {budget}
- Trip duration: {duration}
- Interests: {interests}
- Preferred climate: {climate}

Respond ONLY with valid JSON matching this exact structure (no markdown, no extra text):
{{
  "destinations": [
    {{
      "city": "string",
      "country": "string",
      "tagline": "catchy 6-8 word tagline",
      "why": "2-3 sentence explanation",
      "highlights": ["activity1", "activity2", "activity3"],
      "best_time": "e.g. April-October",
      "estimated_cost": "e.g. ~$1,200 for a week"
    }}
  ],
  "travel_tip": "one pro tip"
}}"""
# Data Models

## Add structured itinerary (day-by-day plan) => Days[], each day activates, timeline-based plan, specify also solo-travel or group travelling or family travelling (might insert questions)

class SuggestionRequest(BaseModel):
    mood: str
    budget: str
    duration: str
    interests: list[str]
    climate: str

## It should give an itinerary, not just destination recommendation and Missing cost aggregation (Rough cost estimate)
class Destination(BaseModel):
    city: str
    country: str
    tagline: str
    why: str
    highlights: list[str]
    best_time: str
    estimated_cost: str

class SuggestionResponse(BaseModel):
    destinations: list[Destination]
    travel_tip: str
    
# Routes
@app.get("/health")
def health():
    return {"status": "ok", "provider": LLM_PROVIDER, "mock": USE_MOCK}

@app.post("/suggest", response_model=SuggestionResponse)
def suggest(req: SuggestionRequest):
    # MOCK MODE
    if USE_MOCK:
        return MOCK_RESPONSE
    # REAL MODE (Claude or Groq)
    prompt = prompt_template.format(
        mood=req.mood,
        budget=req.budget,
        duration=req.duration,
        interests=", ".join(req.interests),
        climate=req.climate,
    )
    # Client only created when actually needed to avoid unnecessary API calls in mock mode (Lazy initialization)
    try:
        client = get_client()
        
        if LLM_PROVIDER == "anthropic":
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            # Defensive extraction (check first, then fails with clear message if structure is unexpected)
            if not message.content or len(message.content) == 0:
                raise HTTPException(status_code=500, detail="Empty response from Claude")

            block = message.content[0]
            raw = getattr(block, "text", "")
        
        else:
            # Groq uses OpenAI-compatible interface
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # best free Groq model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
            )
            raw = chat.choices[0].message.content or ""
        
        # Separating JSON parsing errors from API errors
        
        # -------- NORMALIZATION LAYER --------
        raw = raw.strip()

        # Remove markdown fences if present
        if raw.startswith("```"):
            raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        # -------- PARSING LAYER -------- 
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON from model")

        return SuggestionResponse(**data)    

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))