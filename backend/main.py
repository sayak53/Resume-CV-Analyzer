from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
import re

app = FastAPI()

# Weighted Skills Database
SKILLS_DB = {
    "python": 10,
    "java": 9,
    "javascript": 9,
    "react": 9,
    "nodejs": 8,
    "nextjs": 8,
    "typescript": 8,
    "html": 4,
    "css": 4,
    "sql": 8,
    "mysql": 7,
    "mongodb": 7,
    "postgresql": 8,
    "fastapi": 8,
    "django": 8,
    "flask": 7,
    "machine learning": 10,
    "artificial intelligence": 10,
    "ai": 10,
    "dbms": 6,
    "git": 3,
    "github": 3,
    "docker": 8,
    "kubernetes": 9,
    "aws": 9,
}

# Skill Categories
SKILL_CATEGORIES = {
    "Frontend": [
        "react",
        "nextjs",
        "html",
        "css",
        "javascript",
        "typescript",
    ],

    "Backend": [
        "python",
        "java",
        "django",
        "flask",
        "fastapi",
        "nodejs",
    ],

    "Database": [
        "sql",
        "mysql",
        "mongodb",
        "postgresql",
        "dbms",
    ],

    "Cloud & DevOps": [
        "aws",
        "docker",
        "kubernetes",
        "git",
        "github",
    ],

    "AI / ML": [
        "machine learning",
        "artificial intelligence",
        "ai",
    ],
}

# Role-Based Skill Mapping
ROLE_KEYWORDS = {

    "frontend developer": [
        "react",
        "html",
        "css",
        "javascript",
        "typescript",
        "nextjs",
    ],

    "backend developer": [
        "python",
        "django",
        "flask",
        "fastapi",
        "nodejs",
        "sql",
    ],

    "full stack developer": [
        "react",
        "javascript",
        "nodejs",
        "python",
        "sql",
    ],

    "devops engineer": [
        "docker",
        "kubernetes",
        "aws",
        "git",
    ],

    "machine learning engineer": [
        "python",
        "machine learning",
        "ai",
    ],

    "data analyst": [
        "python",
        "sql",
        "mysql",
        "postgresql",
    ],
}

# Semantic Skill Aliases
SKILL_ALIASES = {
    "nodejs": ["node js", "node.js"],
    "react": ["react js", "reactjs"],
    "javascript": ["js"],
    "typescript": ["ts"],
    "postgresql": ["postgres", "postgre"],
    "machine learning": ["ml"],
    "artificial intelligence": ["ai"],
    "github": ["git hub"],
    "nextjs": ["next js", "next.js"],
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
            text += extracted + " "

    return text


def extract_skills(text):

    text = text.lower()

    found_skills = set()

    # Direct Skill Matching
    for skill in SKILLS_DB.keys():

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.add(skill)

    # Alias Matching
    for main_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text):
                found_skills.add(main_skill)

    return list(found_skills)


def extract_role_based_skills(text):

    text = text.lower()

    detected_skills = []

    for role, role_skills in ROLE_KEYWORDS.items():

        if role in text:

            detected_skills.extend(role_skills)

    return detected_skills


def extract_experience(text):

    text = text.lower()

    patterns = [
        r"(\d+)\+?\s+years?",
        r"experience\s*:\s*(\d+)",
        r"(\d+)\s+yrs?",
    ]

    years = []

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for match in matches:
            years.append(int(match))

    if years:
        return max(years)

    return 0


def check_resume_sections(text):

    text = text.lower()

    return {
        "skills": "skills" in text,
        "projects": "project" in text or "projects" in text,
        "education": "education" in text,
        "experience": (
            "experience" in text
            and extract_experience(text) > 0
        ),
        "certifications": (
            "certification" in text
            or "certifications" in text
            or "certificate" in text
        ),
    }


def categorize_skills(skills):

    categorized = {}

    for category, category_skills in SKILL_CATEGORIES.items():

        matched = [
            skill for skill in skills
            if skill in category_skills
        ]

        if matched:
            categorized[category] = matched

    return categorized


def generate_summary(score, matched_skills, experience):

    if score >= 80:

        return (
            f"Your resume is highly aligned with the job description. "
            f"Strong matching skills include: {', '.join(matched_skills)}. "
            f"You have {experience} years of experience."
        )

    elif score >= 50:

        return (
            f"Your resume matches many important job requirements. "
            f"You should improve a few missing skills to increase your ATS score."
        )

    else:

        return (
            f"Your resume currently has a low match with the job description. "
            f"Consider improving your technical skills, projects, and experience sections."
        )


def generate_suggestions(
    missing_keywords,
    experience_years,
    resume_sections
):

    suggestions = []

    for keyword in missing_keywords:

        suggestions.append(
            f"Try adding projects or experience related to '{keyword}'."
        )

    if experience_years == 0:

        suggestions.append(
            "Your resume lacks professional experience. Add internships, freelance work, open-source contributions, or personal projects."
        )

    if not resume_sections["projects"]:

        suggestions.append(
            "Add a strong projects section with real-world applications."
        )

    if not resume_sections["education"]:

        suggestions.append(
            "Include your education details for better resume completeness."
        )

    if not resume_sections["certifications"]:

        suggestions.append(
            "Adding certifications can improve resume credibility."
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

    resume_sections = check_resume_sections(resume_text)

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    role_based_skills = extract_role_based_skills(
        job_description
    )

    jd_skills.extend(role_based_skills)

    jd_skills = list(set(jd_skills))

    matched_skills = list(
        set(resume_skills) & set(jd_skills)
    )

    missing_keywords = list(
        set(jd_skills) - set(resume_skills)
    )

    # Categorized Skills
    categorized_matched_skills = categorize_skills(
        matched_skills
    )

    categorized_missing_skills = categorize_skills(
        missing_keywords
    )

    # Weighted Score Calculation
    total_possible_score = sum(
        SKILLS_DB[skill]
        for skill in jd_skills
    )

    matched_score = sum(
        SKILLS_DB[skill]
        for skill in matched_skills
    )

    if total_possible_score > 0:

        score = (
            matched_score / total_possible_score
        ) * 100

    else:
        score = 0

    # Resume Quality Penalties
    if experience_years == 0:
        score -= 10

    if not resume_sections["education"]:
        score -= 5

    if not resume_sections["projects"]:
        score -= 5

    # Prevent Negative Score
    if score < 0:
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
        resume_sections
    )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_keywords": missing_keywords,
        "categorized_matched_skills": categorized_matched_skills,
        "categorized_missing_skills": categorized_missing_skills,
        "experience": experience_years,
        "resume_sections": resume_sections,
        "summary": summary,
        "suggestions": suggestions,
        "resume_preview": resume_text[:500],
        "job_description": job_description
    }