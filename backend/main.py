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
            text += extracted + " "

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


def check_resume_sections(text):

    text = text.lower()

    sections = {
        "skills": False,
        "projects": False,
        "education": False,
        "experience": False,
        "certifications": False,
    }

    if re.search(r"\bskills\b", text):
        sections["skills"] = True

    if re.search(r"\bprojects\b", text):
        sections["projects"] = True

    if re.search(r"\beducation\b", text):
        sections["education"] = True

    experience_patterns = [
        r"\bwork experience\b",
        r"\bprofessional experience\b",
        r"\bemployment history\b",
        r"\binternship experience\b",
    ]

    for pattern in experience_patterns:
        if re.search(pattern, text):
            sections["experience"] = True
            break

    if re.search(r"\bcertifications\b|\bcertificates\b", text):
        sections["certifications"] = True

    return sections


def generate_summary(score, matched_skills, experience):

    if score >= 75:
        level = "highly aligned"
    elif score >= 50:
        level = "moderately aligned"
    else:
        level = "needs improvement"

    skills_text = ", ".join(matched_skills[:5])

    if not skills_text:
        skills_text = "no major matching skills"

    summary = (
        f"Your resume is {level} with the job description. "
        f"Strong matching skills include: {skills_text}. "
        f"You have {experience} years of experience."
    )

    return summary


def generate_suggestions(
    missing_keywords,
    experience_years,
    score,
    resume_sections
):

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

    if not resume_sections["projects"]:
        suggestions.append(
            "Add a dedicated Projects section to strengthen your resume."
        )

    if not resume_sections["experience"]:
        suggestions.append(
            "Add an Experience section to improve ATS impact."
        )

    if not resume_sections["certifications"]:
        suggestions.append(
            "Adding certifications can improve your resume credibility."
        )

    return suggestions


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

    resume_sections = check_resume_sections(resume_text)

    if len(jd_skills) > 0:
        score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        score = 0

    score = round(score, 2)

    summary = generate_summary(
        score,
        matched_skills,
        experience_years
    )

    suggestions = generate_suggestions(
        missing_keywords,
        experience_years,
        score,
        resume_sections
    )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_keywords": missing_keywords,
        "experience": experience_years,
        "resume_preview": resume_text[:1000],
        "job_description": job_description,
        "resume_sections": resume_sections,
        "summary": summary,
        "suggestions": suggestions,
    }