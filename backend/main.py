import sys
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT_DIR = Path(__file__).resolve().parents[1]
ML_SRC_DIR = ROOT_DIR / "ml" / "src"
SAFE_JOBS_PATH = ROOT_DIR / "data" / "clean" / "dataset_clean.csv"
sys.path.insert(0, str(ML_SRC_DIR))

from predictor import predict_single_job

app = FastAPI()

_SAFE_JOBS = None
_REC_VECTORIZER = None
_REC_MATRIX = None

SKILL_KEYWORDS = {
    "Python": ["python", "питон"],
    "SQL": ["sql", "postgresql", "mysql", "database", "база данных"],
    "Excel": ["excel", "эксель", "сводные таблицы"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "JavaScript": ["javascript", "js", "джаваскрипт"],
    "TypeScript": ["typescript", "ts"],
    "React": ["react", "реакт"],
    "Vue": ["vue", "nuxt"],
    "HTML": ["html"],
    "CSS": ["css", "tailwind", "scss"],
    "Docker": ["docker", "докер"],
    "Git": ["git", "github", "gitlab"],
    "REST API": ["rest api", "api", "axios"],
    "Figma": ["figma"],
    "1C": ["1c", "1с"],
    "Analytics": ["analytics", "аналитика", "анализ данных", "data analysis"],
    "Marketing": ["marketing", "маркетинг"],
    "Sales": ["sales", "продажи", "b2b"],
    "Negotiation": ["negotiation", "переговоры"],
    "Communication": ["communication", "коммуникация", "коммуникативные"],
    "Management": ["management", "управление", "project manager"],
    "HR": ["hr", "recruitment", "рекрутинг", "подбор персонала"],
    "Procurement": ["procurement", "закупки", "снабжение"],
    "Logistics": ["logistics", "логистика"],
    "Accounting": ["accounting", "бухгалтерия"],
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobInput(BaseModel):
    title: str
    description: str
    requirements: str = ""
    company_profile: str = ""
    benefits: str = ""
    salary_range: str = ""
    location: str = ""
    employment_type: str = ""
    industry: str = ""
    telecommuting: int = 0
    has_company_logo: int = 0
    has_questions: int = 0


class ResumeInput(BaseModel):
    resume_text: str
    limit: int = 5


class SkillGapInput(BaseModel):
    resume_text: str
    job_title: str = ""
    job_description: str = ""
    job_url: str = ""


class JobUrlInput(BaseModel):
    url: str


def _combined_text(job: JobInput):
    return " ".join(
        [
            job.title,
            job.company_profile,
            job.description,
            job.requirements,
            job.benefits,
            job.salary_range,
            job.location,
            job.employment_type,
        ]
    ).strip()


def _job_from_url(url: str):
    local_job = _find_local_job_by_url(url)
    if local_job:
        return local_job

    scraped = _scrape_job_url(url)
    return JobInput(
        title=scraped["title"],
        description=scraped["description"],
        company_profile=scraped["company_name"],
        salary_range=scraped["salary"],
        location=scraped["location"],
    )


def _find_local_job_by_url(url: str):
    if not SAFE_JOBS_PATH.exists():
        return None

    jobs = pd.read_csv(SAFE_JOBS_PATH)
    matches = jobs[jobs.get("url", "").fillna("") == url]
    if matches.empty:
        return None

    row = matches.iloc[0]
    return JobInput(
        title=_safe_value(row.get("title"), ""),
        description=_safe_value(row.get("description"), _safe_value(row.get("text"), "")),
        company_profile=_safe_value(row.get("company_name"), ""),
        salary_range=_safe_value(row.get("salary"), ""),
        location="",
    )


def _scrape_job_url(url: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=12)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = _extract_first_text(
        soup,
        [
            "[data-qa='vacancy-title']",
            "h1",
            "meta[property='og:title']",
            "title",
        ],
    )
    description = _extract_first_text(
        soup,
        [
            "[data-qa='vacancy-description']",
            "[data-cy='ad_description']",
            "article",
            "main",
            "body",
        ],
    )
    company_name = _extract_first_text(
        soup,
        [
            "[data-qa='vacancy-company-name']",
            "[data-qa='vacancy-serp__vacancy-employer']",
            "[data-testid='ad-price-container']",
        ],
    )
    salary = _extract_first_text(
        soup,
        [
            "[data-qa='vacancy-salary']",
            "[data-testid='ad-price-container']",
            "[data-testid='ad-price']",
        ],
    )
    location = _extract_first_text(
        soup,
        [
            "[data-qa='vacancy-view-location']",
            "[data-testid='location-date']",
        ],
    )

    if not title and not description:
        raise ValueError("Could not extract vacancy text from URL")

    return {
        "title": title,
        "description": description,
        "company_name": company_name,
        "salary": salary,
        "location": location,
    }


def _extract_first_text(soup: BeautifulSoup, selectors):
    for selector in selectors:
        node = soup.select_one(selector)
        if not node:
            continue
        if node.name == "meta":
            text = node.get("content", "")
        else:
            text = node.get_text(" ", strip=True)
        if text:
            return " ".join(text.split())
    return ""


def _load_safe_jobs():
    global _SAFE_JOBS, _REC_VECTORIZER, _REC_MATRIX

    if _SAFE_JOBS is not None:
        return

    if not SAFE_JOBS_PATH.exists():
        _SAFE_JOBS = pd.DataFrame()
        return

    jobs = pd.read_csv(SAFE_JOBS_PATH)
    jobs = jobs[jobs.get("label", 1).fillna(1).astype(int) == 0].copy()
    jobs["text"] = jobs.get("text", "").fillna("").astype(str)
    jobs = jobs[jobs["text"].str.len() > 20].reset_index(drop=True)
    risky_pattern = (
        "whatsapp|ватсап|telegram|телеграм|предоплата|оплата за обучение|"
        "без опыта|легкий заработок|быстрый доход"
    )
    jobs = jobs[~jobs["text"].str.contains(risky_pattern, case=False, na=False)]
    jobs = jobs.reset_index(drop=True)

    _SAFE_JOBS = jobs
    if jobs.empty:
        return

    _REC_VECTORIZER = TfidfVectorizer(max_features=8000, ngram_range=(1, 2))
    _REC_MATRIX = _REC_VECTORIZER.fit_transform(jobs["text"])


def recommend_safe_jobs(job: JobInput, limit=3):
    _load_safe_jobs()

    if _SAFE_JOBS is None or _SAFE_JOBS.empty:
        return []

    query = _combined_text(job)
    if not query:
        return []

    query_vector = _REC_VECTORIZER.transform([query])
    scores = cosine_similarity(query_vector, _REC_MATRIX).ravel()
    top_indexes = scores.argsort()[::-1][:limit]

    recommendations = []
    for index in top_indexes:
        row = _SAFE_JOBS.iloc[index]
        recommendations.append(
            {
                "title": _safe_value(row.get("title"), "Untitled vacancy"),
                "company_name": _safe_value(row.get("company_name"), "Unknown company"),
                "salary": _safe_value(row.get("salary"), "Not specified"),
                "source": _safe_value(row.get("source"), ""),
                "url": _safe_value(row.get("url"), ""),
                "similarity": round(float(scores[index]), 3),
            }
        )

    return recommendations


def match_resume_to_jobs(resume_text: str, limit=5):
    _load_safe_jobs()

    if _SAFE_JOBS is None or _SAFE_JOBS.empty or not resume_text.strip():
        return []

    limit = max(1, min(int(limit or 5), 10))
    resume_vector = _REC_VECTORIZER.transform([resume_text])
    scores = cosine_similarity(resume_vector, _REC_MATRIX).ravel()
    top_indexes = scores.argsort()[::-1][:limit]
    resume_skills = extract_skills(resume_text)

    matches = []
    for index in top_indexes:
        row = _SAFE_JOBS.iloc[index]
        job_text = _safe_value(row.get("text"), "")
        required_skills = extract_skills(job_text)
        matched_skills = sorted(set(resume_skills) & set(required_skills))
        missing_skills = sorted(set(required_skills) - set(resume_skills))

        matches.append(
            {
                "title": _safe_value(row.get("title"), "Untitled vacancy"),
                "company_name": _safe_value(row.get("company_name"), "Unknown company"),
                "salary": _safe_value(row.get("salary"), "Not specified"),
                "source": _safe_value(row.get("source"), ""),
                "url": _safe_value(row.get("url"), ""),
                "match_percent": round(float(scores[index]) * 100),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills[:8],
            }
        )

    return matches


def calculate_skill_gap(payload: SkillGapInput):
    job_text = payload.job_description.strip()
    job_title = payload.job_title.strip()

    if not job_text and payload.job_url:
        _load_safe_jobs()
        if _SAFE_JOBS is not None and not _SAFE_JOBS.empty:
            rows = _SAFE_JOBS[_SAFE_JOBS["url"].fillna("") == payload.job_url]
            if not rows.empty:
                row = rows.iloc[0]
                job_title = _safe_value(row.get("title"), job_title)
                job_text = _safe_value(row.get("text"), "")

    if not job_text and job_title:
        matches = match_resume_to_jobs(job_title, limit=1)
        if matches:
            job_title = matches[0]["title"]
            job_text = job_title

    resume_skills = extract_skills(payload.resume_text)
    required_skills = extract_skills(f"{job_title} {job_text}")
    matched_skills = sorted(set(resume_skills) & set(required_skills))
    missing_skills = sorted(set(required_skills) - set(resume_skills))

    coverage = 0
    if required_skills:
        coverage = round(len(matched_skills) / len(required_skills) * 100)

    return {
        "job_title": job_title or "Selected vacancy",
        "coverage_percent": coverage,
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


def extract_skills(text: str):
    text_lower = f" {text.lower()} "
    found = []
    for skill, aliases in SKILL_KEYWORDS.items():
        if any(alias.lower() in text_lower for alias in aliases):
            found.append(skill)
    return sorted(found)


def _safe_value(value, fallback):
    if pd.isna(value) or value == "":
        return fallback
    return str(value)

@app.post("/predict")
def predict(job: JobInput):
    result = predict_single_job(job.model_dump(), use_hybrid=True)
    risk_score = result["final_risk_score"]

    if result["prediction"] == "Fake":
        prediction = "Fake"
    elif risk_score >= 0.40:
        prediction = "Suspicious"
    else:
        prediction = "Real"

    return {
        "prediction": prediction,
        "fraud_probability": result["ml_fraud_probability"],
        "suspicion_score": round(risk_score * 100),
        "risk_level": result["risk_level"],
        "detected_phrases": result["detected_suspicious_phrases"],
        "explanation": result["explanation"],
        "ml_fraud_probability": result["ml_fraud_probability"],
        "local_rule_score": result["local_rule_score"],
        "final_risk_score": risk_score,
        "recommendations": recommend_safe_jobs(job) if prediction != "Real" else [],
    }


@app.post("/predict-url")
def predict_url(payload: JobUrlInput):
    job = _job_from_url(payload.url)
    result = predict(job)
    result["extracted_job"] = job.model_dump()
    result["source_url"] = payload.url
    return result


@app.post("/recommend")
def recommend(job: JobInput):
    return {"recommendations": recommend_safe_jobs(job)}


@app.post("/resume-match")
def resume_match(resume: ResumeInput):
    return {"matches": match_resume_to_jobs(resume.resume_text, resume.limit)}


@app.post("/skill-gap")
def skill_gap(payload: SkillGapInput):
    return calculate_skill_gap(payload)
