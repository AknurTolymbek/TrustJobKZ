# TrustJobKZ

Machine-learning web app for checking whether a job vacancy looks real,
suspicious, or fake.

Features:

- English/Russian/Kazakh frontend language switcher
- Single vacancy fake-job prediction
- Vacancy URL prediction with automatic text extraction
- Suspicion score, risk level, explanation, and suspicious phrases
- Similar safer vacancy recommendations from the local Kazakhstan dataset
- Resume-to-job matching with real vacancies
- Skill gap analysis for a resume and selected vacancy
- FastAPI backend and React/Vite frontend

## Run With Docker

Install Docker Desktop first, then run from the project root:

```bash
docker compose up --build
```

Open the frontend:

```text
http://127.0.0.1:5173/
```

The backend API runs here:

```text
http://127.0.0.1:8000/
```

Stop the app:

```bash
docker compose down
```

## Run Without Docker

Backend:

```bash
/opt/anaconda3/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
npm run dev -- --host 127.0.0.1
```
