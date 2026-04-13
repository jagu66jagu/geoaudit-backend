# GeoAudit Backend

FastAPI backend for GeoAudit — AI Visibility & GEO Audit platform.

## Stack
- Python 3.11+
- FastAPI
- Anthropic Claude API

## Local development

```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health` — service health check
- `POST /api/actions/generate` — generate AI action output

## Deploy
Deployed on Railway. Push to main branch triggers auto-deploy.
