from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

SKILLS_DB = [
    "python",
    "java",
    "javascript",
    "react",
    "nodejs",
    "html",
    "css",
    "sql",
    "mysql",
    "mongodb",
    "fastapi",
    "django",
    "flask",
    "machine learning",
    "ai",
    "dbms",
    "git",
    "github",
]

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
        text += page.extract_text()

    return text


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

        if skill in text:
            found_skills.append(skill)

    return found_skills


def get_similarity(resume, job_description):

    documents = [resume, job_description]

    cv = TfidfVectorizer(stop_words="english")

    matrix = cv.fit_transform(documents)

    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100, 2)


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    text = extract_text(resume.file)

    resume_skills = extract_skills(text)

    jd_skills = extract_skills(job_description)

    matched_skills = list(set(resume_skills) & set(jd_skills))

    missing_keywords = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) > 0:
        score = round((len(matched_skills) / len(jd_skills)) * 100, 2)
    else:
        score = 0

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_keywords": missing_keywords,
        "resume_preview": text[:300],
        "job_description": job_description
    }