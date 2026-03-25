You are my senior backend engineering partner.

Goal:
Build a one-day MVP project for interview demonstration using FastAPI + MongoDB Atlas.
The project must clearly demonstrate RESTful API concepts, Swagger/OpenAPI documentation, basic deployment readiness, and simple CI/CD readiness.
The topic is European travel destinations and attractions.

Important priorities:
1. One-day completion is the highest priority.
2. Keep the architecture simple, clean, and interview-friendly.
3. Do not over-engineer.
4. Generate production-like structure, but only for MVP scope.
5. Every implementation decision should favor clarity, maintainability, and demo value.

Project name:
europe-travel-api

Core stack:
- FastAPI
- Python 3.11+
- Pydantic
- MongoDB Atlas
- PyMongo (preferred for simplicity)
- Uvicorn
- python-dotenv

Main requirements:
1. Build RESTful APIs for:
   - cities
   - attractions
2. Support these methods:
   - GET list
   - GET by id
   - POST create
   - PATCH partial update
   - DELETE remove
3. Add query filters for attractions:
   - city
   - category
   - is_free
4. Use MongoDB Atlas as the database.
5. Swagger docs must work via FastAPI default /docs and /redoc.
6. Prepare the project so it can later be deployed easily on Render.
7. Include simple GitHub Actions CI for lint/basic validation if reasonable.
8. Mock data must live under:
   - mock_data/cities.json
   - mock_data/attractions.json

Scope constraints:
- Do NOT add authentication.
- Do NOT add image upload.
- Do NOT add Docker unless absolutely necessary.
- Do NOT add complex service layers unless they improve clarity.
- Do NOT add too many abstractions.
- Keep it MVP and interview-demo friendly.

Data design requirements:

Collection: cities
Suggested fields:
- name
- country
- region
- language
- currency
- best_season
- description
- created_at
- updated_at

Collection: attractions
Suggested fields:
- city_id
- name
- category
- address
- rating
- ticket_price_eur
- is_free
- recommended_visit_hours
- tags
- description
- created_at
- updated_at

Example topic:
Use European cities and attractions such as Paris, Vienna, Prague, Rome, Munich, Amsterdam, Barcelona, etc.
Attractions can include Eiffel Tower, Schönbrunn Palace, Colosseum, Charles Bridge, Sagrada Família, etc.

Expected project structure:
- app/
  - main.py
  - core/
    - config.py
    - database.py
  - schemas/
    - city.py
    - attraction.py
  - routers/
    - cities.py
    - attractions.py
  - utils/
    - bson.py
- mock_data/
  - cities.json
  - attractions.json
- .env.example
- requirements.txt
- README.md
- .github/workflows/ci.yml

Coding rules:
1. Use clean modular structure, but keep it simple.
2. Use response models where practical.
3. Handle MongoDB ObjectId safely.
4. Return proper HTTP status codes.
5. Write readable code suitable for interview explanation.
6. Add concise comments only where useful.
7. Do not leave obvious placeholders unless necessary.
8. If something is uncertain, choose the simplest practical solution.

What I want from you:
Please complete this task in phases and stop after each phase summary.

Phase 1:
- Generate the full folder structure
- Generate requirements.txt
- Generate .env.example
- Generate app/core/config.py
- Generate app/core/database.py
- Generate app/utils/bson.py
- Generate app/main.py

Phase 2:
- Generate Pydantic schemas for city and attraction
- Make schemas suitable for create, update, and response use cases

Phase 3:
- Generate cities router with:
  - GET /cities
  - GET /cities/{id}
  - POST /cities
  - PATCH /cities/{id}
  - DELETE /cities/{id}

Phase 4:
- Generate attractions router with:
  - GET /attractions
  - GET /attractions/{id}
  - POST /attractions
  - PATCH /attractions/{id}
  - DELETE /attractions/{id}
  - query filters for city, category, is_free

Phase 5:
- Register routers in main.py
- Verify imports and endpoint consistency
- Ensure Swagger docs will render correctly

Phase 6:
- Create realistic mock data files:
  - mock_data/cities.json
  - mock_data/attractions.json
- Include at least 6 cities and 12 attractions
- Make the data realistic and interview-friendly

Phase 7:
- Generate README.md with:
  - project overview
  - tech stack
  - folder structure
  - setup instructions
  - environment variables
  - how to run locally
  - API summary
  - Swagger docs URL
  - MongoDB Atlas notes
  - Render deployment notes
  - CI/CD notes
- README should be concise but professional

Phase 8:
- Generate .github/workflows/ci.yml
- Keep CI simple:
  - install dependencies
  - optionally run a basic syntax/import check
- Do not overcomplicate CI

Execution style:
- For each phase, first explain briefly what files you will create or update.
- Then generate the code.
- Keep outputs organized by file path.
- Prefer complete file contents over fragments.
- If a file depends on another file, make them consistent.
- If there is a better simple choice than my suggestion, use it and explain why briefly.

Final expectation:
At the end, the project should be runnable locally with:
uvicorn app.main:app --reload

Please start from Phase 1 now.