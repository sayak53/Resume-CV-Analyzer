from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader

import re

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
    "docker",
    "kubernetes",
    "aws",
    "postgresql",
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

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

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


def detect_resume_sections(text):

    text = text.lower()

    sections = {
        "skills": False,
        "projects": False,
        "education": False,
        "experience": False,
        "certifications": False,
    }

    if "skills" in text:
        sections["skills"] = True

    if "project" in text or "projects" in text:
        sections["projects"] = True

    if "education" in text:
        sections["education"] = True

    if "experience" in text:
        sections["experience"] = True

    if "certification" in text or "certifications" in text:
        sections["certifications"] = True

    return sections


def generate_summary(score, matched_skills, missing_keywords, experience):

    summary = ""

    if score >= 75:
        summary += "Your resume is highly aligned with the job description. "

    elif score >= 50:
        summary += "Your resume matches the job description moderately well. "

    else:
        summary += "Your resume has a low match with the job description. "

    if len(matched_skills) > 0:

        summary += (
            "Strong matching skills include: "
            + ", ".join(matched_skills)
            + ". "
        )

    if len(missing_keywords) > 0:

        summary += (
            "You may improve your resume by adding skills or projects related to: "
            + ", ".join(missing_keywords)
            + ". "
        )

    if experience == 0:

        summary += (
            "Adding internships, freelance work, or personal projects may improve your profile."
        )

    else:

        summary += f"You have {experience} years of experience."

    return summary


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

    resume_sections = detect_resume_sections(resume_text)

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    matched_skills = list(set(resume_skills) & set(jd_skills))

    missing_keywords = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) > 0:
        score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        score = 0

    score = round(score, 2)

    summary = generate_summary(
        score,
        matched_skills,
        missing_keywords,
        experience_years
    )

    suggestions = []

    for keyword in missing_keywords:

        suggestions.append(
            f"Try adding projects or experience related to '{keyword}'."
        )

    if experience_years == 0:

        suggestions.append(
            "Add internships, freelance work, or personal projects to showcase experience."
        )

    if score < 50:

        suggestions.append(
            "Your resume matches less than 50% of the job description. Consider improving your skills section."
        )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_keywords": missing_keywords,
        "experience": experience_years,
        "resume_sections": resume_sections,
        "suggestions": suggestions,
        "summary": summary,
        "resume_preview": resume_text[:800],
        "job_description": job_description
    }