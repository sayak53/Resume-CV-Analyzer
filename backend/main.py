from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

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


def get_similarity(resume, job_description):
    documents = [resume, job_description]

    cv = CountVectorizer()

    matrix = cv.fit_transform(documents)

    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100, 2)


def get_missing_keywords(resume, job_description):

    resume_words = set(resume.lower().split())

    jd_words = set(job_description.lower().split())

    missing = jd_words - resume_words

    return list(missing)[:10]


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    text = extract_text(resume.file)

    score = get_similarity(text, job_description)

    missing_keywords = get_missing_keywords(text, job_description)

    return {
        "score": score,
        "missing_keywords": missing_keywords,
        "resume_preview": text[:300],
        "job_description": job_description
    }