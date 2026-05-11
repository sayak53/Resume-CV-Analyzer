from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader

import re

app = FastAPI()

SKILLS_DB = {
    "python": 10,
    "java": 9,
    "javascript": 9,
    "react": 9,
    "nodejs": 8,
    "html": 4,
    "css": 4,
    "sql": 8,
    "mysql": 7,
    "mongodb": 7,
    "fastapi": 8,
    "django": 8,
    "flask": 7,
    "machine learning": 10,
    "ai": 10,
    "dbms": 6,
    "git": 3,
    "github": 3,
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text(file):
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB.keys():

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def extract_experience(text):

    pattern = r"(\d+)\+?\s+years?"

    matches = re.findall(pattern, text.lower())

    if matches:
        years = [int(year) for year in matches]
        return max(years)

    return 0


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    resume_text = extract_text(resume.file)

    experience_years = extract_experience(resume_text)

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    matched_skills = list(set(resume_skills) & set(jd_skills))

    missing_keywords = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) > 0:
        score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        score = 0

    return {
        "score": round(score, 2),
        "matched_skills": matched_skills,
        "missing_keywords": missing_keywords,
        "experience": experience_years,
        "resume_preview": resume_text[:500],
        "job_description": job_description
    }