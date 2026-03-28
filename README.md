# Europe Travel API

This repository contains a FastAPI project for managing European cities and attractions. The codebase is organized by application responsibilities so the API entrypoint, configuration, routers, schemas, and utility helpers stay separated.

## Project Structure

```text
.
|-- .github/
|   `-- workflows/
|       `-- ci.yml              # GitHub Actions workflow for linting and tests
|-- app/
|   |-- core/
|   |   |-- config.py           # Application settings loaded from environment variables
|   |   `-- database.py         # MongoDB client and collection access
|   |-- routers/
|   |   |-- attractions.py      # Attraction API routes
|   |   `-- cities.py           # City API routes
|   |-- schemas/
|   |   |-- attraction.py       # Attraction request and response models
|   |   `-- city.py             # City request and response models
|   |-- utils/
|   |   `-- bson.py             # MongoDB ObjectId parsing and serialization helpers
|   |-- main.py                 # FastAPI application entrypoint
|   `-- __init__.py
|-- mock_data/
|   |-- attractions.json        # Sample attraction data
|   `-- cities.json             # Sample city data
|-- tests/
|   |-- test_app.py             # Basic API endpoint tests
|   `-- test_bson.py            # BSON helper tests
|-- .gitignore                  # Local files and generated artifacts excluded from Git
|-- GENERAL.md                  # Additional project notes
|-- README.md                   # Repository overview
|-- requirements-dev.txt        # Development and CI dependencies
`-- requirements.txt            # Runtime dependencies
```

## Deploy To Vercel

This project is ready for Vercel using the included [`vercel.json`](./vercel.json) config and the ASGI entrypoint at [`api/index.py`](./api/index.py).

Set these environment variables in your Vercel project before deploying:

- `MONGODB_URL`
- `DB_NAME` (optional, defaults to `europe_travel_api`)

You can use [`.env.example`](./.env.example) as the reference for required values.

Deployment steps:

1. Import this GitHub repository into Vercel.
2. Leave the framework settings on auto-detect. Vercel will follow `vercel.json`.
3. Add the required environment variables in `Settings -> Environment Variables`.
4. Start the first deployment.

After deployment, verify these paths:

- `/`
- `/health`
- `/docs`
