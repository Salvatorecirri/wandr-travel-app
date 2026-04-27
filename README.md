# WANDR – AI Travel Suggestions

> AI-powered travel destination suggestions based on your mood, budget, and interests.
> Built as a weekend sprint to demonstrate full-stack skills with Vue 3, TypeScript, FastAPI, and Claude AI.

![Vue](https://img.shields.io/badge/Vue-3-42b883?logo=vue.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178c6?logo=typescript)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ed?logo=docker)

## Demo

| Input | Output |
|------|--------|
| ![Home](frontend/assets/demo/demo-1.png) | ![Results](frontend/assets/demo/demo-2.png) |

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3, TypeScript, Vite |
| Backend | Python 3.12, FastAPI |
| AI | Anthropic Claude claude-opus-4-5 |
| Deploy | Docker Compose, Nginx |

## Features

- Pick your travel vibe, budget, duration, interests, and climate preference
- Claude AI generates 3 personalized destination recommendations
- Each result includes highlights, best travel season, and cost estimate
- Fully containerized — runs with a single `docker compose up`, creating 2 containers: backend	(FastAPI + Python) and frontend (Vue build served by Nginx) + Docker Compose to connect them.

## Quick Start

### With Docker (recommended)

```bash
git clone https://github.com/YOUR_USERNAME/wandr-travel-app.git
cd wandr-travel-app
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
docker compose up --build
```

Open http://localhost:3000

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env with your ANTHROPIC_API_KEY
uvicorn main:app --reload
# API running at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# App running at http://localhost:5173
```

## Project Structure

```
wandr-travel-app/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── .vscode/
│   └── extensions.json         # Recommended extensions
├── backend/
│   ├── main.py                 # FastAPI + Claude
│   ├── requirements.txt        # Pinned dependencies
│   ├── Dockerfile              # Python container
│   └── .dockerignore           # Clean Docker build
├── frontend/
│   ├── .vscode/
│   │   └── extensions.json     # Recommended extensions
│   ├── public/
│   │   ├── favicon.svg         # Browser tab icon
│   │   └── icons.svg           # Shared SVG icon sprites
│   ├── src/
│   │   ├── assets/             # Static assets (img, font)
│   │   │   ├── hero.png
│   │   │   └── vite.svg
│   │   ├── components/
│   │   │   ├── TravelForm.vue  # Input component
│   │   │   └── DestinationCard.vue  # Output component
│   │   ├── composables/
│   │   │   └── useTravelSuggestions.ts  # Composable
│   │   ├── types/
│   │   │   └── index.ts        # TypeScript interfaces
│   │   ├── App.vue             # Root + styles
│   │   ├── main.ts             # App entrypoint
│   │   └── style.css
│   ├── .dockerignore           # Clean Docker build
│   ├── .gitignore
│   ├── Dockerfile              # Frontend container
│   ├── index.html              # HTML shell
│   ├── nginx.conf              # Prod server config
│   ├── package.json            # Dependencies
│   ├── package-lock.json
│   ├── README.md
│   ├── tsconfig.app.json
│   ├── tsconfig.json           # TypeScript config
│   ├── tsconfig.node.json
│   └── vite.config.ts          # Dev proxy config
├── .env.example                # Template for env vars
├── .gitignore                  # Excludes .env, venv, dist
├── docker-compose.yml          # Orchestration container
├── LICENSE                     # Project license
└── README.md                   # Full docs with badges

```

## Architecture

```
Vue 3 (TypeScript)  →  FastAPI (Python)  →  Claude API
     Port 3000            Port 8000          Anthropic
         ↑                    ↑
       Nginx             Pydantic models
    (reverse proxy)      (type validation)
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LLM_PROVIDER` | No | `groq` (default, free) or `anthropic` |
| `GROQ_API_KEY` | If using Groq | From console.groq.com |
| `ANTHROPIC_API_KEY` | If using Anthropic | From console.anthropic.com |
| `USE_MOCK` | No | `true` skips all API calls |

## License

MIT
