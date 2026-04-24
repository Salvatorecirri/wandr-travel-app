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
import os

from dotenv import load_dotenv
load_dotenv()

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
            "best_time": "April–June or September–October",
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
            "best_time": "March–May or October–November",
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
            "best_time": "May–September",
            "estimated_cost": "~€900 for a week"
        }
    ],
    "travel_tip": "For slow travel, stay in one central neighborhood and explore on foot — it completely changes the experience."
}

app = FastAPI(title="Travel Suggestion API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Data Models

## Add structured itinerary (day-by-day plan) => Days[], each day activites, timeline-based plan, specify also solo-travel or group travelling or family travelling (might insert questions)

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
    return {"status": "ok"}

@app.post("/suggest", response_model=SuggestionResponse)
def suggest(req: SuggestionRequest):

    # ✅ MOCK MODE
    if USE_MOCK:
        return MOCK_RESPONSE

    # 🔥 REAL MODE (Claude)
    prompt = f"""You are a world-class travel curator. Suggest exactly 3 destinations.

Traveler profile:
- Mood/vibe: {req.mood}
- Budget: {req.budget}
- Trip duration: {req.duration}
- Interests: {", ".join(req.interests)}
- Preferred climate: {req.climate}

Respond ONLY with valid JSON."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )

        import json
        data = json.loads(message.content[0].text)
        return SuggestionResponse(**data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))