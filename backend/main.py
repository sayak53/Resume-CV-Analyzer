from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
import re

app = FastAPI()

# =========================
# WEIGHTED SKILLS DATABASE
# =========================

SKILLS_DB = {
    "python": 10,
    "java": 9,
    "javascript": 9,
    "react": 9,
    "nodejs": 8,
    "nextjs": 8,
    "typescript": 6,
    "html": 4,
    "css": 4,
    "sql": 8,
    "mysql": 7,
    "mongodb": 7,
    "postgresql": 8,
    "sqlite": 6,
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
    "tailwind": 5,
    "bootstrap": 5,
}

# =========================
# SKILL CATEGORIES
# =========================

SKILL_CATEGORIES = {

    "Frontend": [
        "react",
        "nextjs",
        "html",
        "css",
        "javascript",
        "typescript",
        "tailwind",
        "bootstrap",
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
        "sqlite",
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

# =========================
# ROLE-BASED SKILLS
# =========================

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

# =========================
# SKILL ALIASES
# =========================

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

    "html": ["html5"],

    "css": ["css3"],
}

# =========================
# SUBSTITUTE SKILLS
# =========================

SKILL_SUBSTITUTES = {

    "sql": [
        "mysql",
        "postgresql",
        "mongodb",
        "sqlite",
    ],

    "fastapi": [
        "django",
        "flask",
        "nodejs",
    ],

    "flask": [
        "django",
        "fastapi",
        "nodejs",
    ],

    "django": [
        "flask",
        "fastapi",
        "nodejs",
    ],

    "html": [
        "react",
        "nextjs",
    ],

    "css": [
        "tailwind",
        "bootstrap",
    ],

    "typescript": [
        "javascript",
        "react",
        "nextjs",
    ],
}

# =========================
# OPTIONAL SKILLS
# =========================

OPTIONAL_SKILLS = [
    "typescript",
    "tailwind",
    "bootstrap",
    "github",
]

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# PDF TEXT EXTRACTION
# =========================

def extract_text(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + " "

    return text

# =========================
# SKILL EXTRACTION
# =========================

def extract_skills(text):

    text = text.lower()

    found_skills = set()

    # DIRECT MATCHING
    for skill in SKILLS_DB.keys():

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.add(skill)

    # ALIAS MATCHING
    for main_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text):
                found_skills.add(main_skill)

    return list(found_skills)

# =========================
# ROLE-BASED SKILLS
# =========================

def extract_role_based_skills(text):

    text = text.lower()

    detected_skills = []

    for role, role_skills in ROLE_KEYWORDS.items():

        if role in text:
            detected_skills.extend(role_skills)

    return detected_skills

# =========================
# EXPERIENCE EXTRACTION
# =========================

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

# =========================
# PRACTICAL EXPERIENCE CHECK
# =========================

def has_practical_experience(text):

    text = text.lower()

    keywords = [

        "intern",
        "internship",
        "training",
        "hackathon",
        "team leader",
        "freelance",
        "developer",
        "open source",
        "project",
        "worked on",
    ]

    return any(
        keyword in text
        for keyword in keywords
    )

# =========================
# RESUME SECTION CHECK
# =========================

def check_resume_sections(text):

    text = text.lower()

    return {

        "skills": (
            "skills" in text
        ),

        "projects": (
            "project" in text
            or "projects" in text
        ),

        "education": (
            "education" in text
        ),

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

# =========================
# SKILL CATEGORIZATION
# =========================

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

# =========================
# AI SUMMARY
# =========================

def generate_summary(
    score,
    matched_skills,
    experience
):

    if score >= 80:

        return (
            f"Your resume is highly aligned with the "
            f"job description. Strong matching skills "
            f"include: {', '.join(matched_skills)}. "
            f"You have {experience} years of experience."
        )

    elif score >= 50:

        return (
            f"Your resume matches many important "
            f"job requirements. You should improve "
            f"a few missing skills to increase "
            f"your ATS score."
        )

    else:

        return (
            f"Your resume currently has a low "
            f"match with the job description. "
            f"Consider improving your technical "
            f"skills, projects, and experience sections."
        )

# =========================
# SUGGESTIONS
# =========================

def generate_suggestions(

    missing_keywords,
    experience_years,
    resume_sections
):

    suggestions = []

    for keyword in missing_keywords:

        suggestions.append(
            f"Try adding projects or experience "
            f"related to '{keyword}'."
        )

    if experience_years == 0 and not has_practical_experience:

        suggestions.append(
            "Your resume lacks professional "
            "experience. Add internships, "
            "freelance work, open-source "
            "contributions, or personal projects."
        )

    if not resume_sections["projects"]:

        suggestions.append(
            "Add a strong projects section "
            "with real-world applications."
        )

    if not resume_sections["education"]:

        suggestions.append(
            "Include your education details "
            "for better resume completeness."
        )

    if not resume_sections["certifications"]:

        suggestions.append(
            "Adding certifications can improve "
            "resume credibility."
        )

    return suggestions

# =========================
# HOME ROUTE
# =========================

@app.get("/")
def home():

    return {
        "message": "Backend is running 🚀"
    }

# =========================
# MAIN ANALYSIS API
# =========================

@app.post("/analyze/")
async def analyze_resume(

    resume: UploadFile = File(...),

    job_description: str = Form(...)
):

    resume_text = extract_text(resume.file)

    experience_years = extract_experience(
        resume_text
    )
    
    practical_experience = has_practical_experience(
        resume_text
    )

    resume_sections = check_resume_sections(
        resume_text
    )

    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        job_description
    )

    role_based_skills = extract_role_based_skills(
        job_description
    )

    jd_skills.extend(role_based_skills)

    jd_skills = list(set(jd_skills))

    # =========================
    # MATCHED SKILLS
    # =========================

    matched_skills = list(
        set(resume_skills) & set(jd_skills)
    )

    # =========================
    # SMART MISSING SKILLS
    # =========================

    missing_keywords = []

    for skill in jd_skills:

        if skill in resume_skills:
            continue

        substitutes = SKILL_SUBSTITUTES.get(
            skill,
            []
        )

        substitute_found = any(

            substitute in resume_skills

            for substitute in substitutes
        )

        if not substitute_found:

            if skill not in OPTIONAL_SKILLS:
                missing_keywords.append(skill)

    # =========================
    # CATEGORY GROUPING
    # =========================

    categorized_matched_skills = categorize_skills(
        matched_skills
    )

    categorized_missing_skills = categorize_skills(
        missing_keywords
    )

    # =========================
    #   SMART WEIGHTED SCORE
    # =========================

    total_possible_score = sum(
       SKILLS_DB[skill]
       for skill in jd_skills
    )

    matched_score = 0

    for skill in jd_skills:

       # =========================
       # EXACT MATCH
       # =========================

       if skill in resume_skills:

           matched_score += SKILLS_DB[skill]

       else:

           substitutes = SKILL_SUBSTITUTES.get(
               skill,
               []
           )

           substitute_found = any(

               substitute in resume_skills

               for substitute in substitutes
           )

           # =========================
           # SUBSTITUTE MATCH
           # =========================

           if substitute_found:

               matched_score += (
                   SKILLS_DB[skill] * 0.7
               )

           else:

               # =========================
               # CATEGORY MATCH
               # =========================

               for category, category_skills in SKILL_CATEGORIES.items():

                   if skill in category_skills:

                       matched_in_category = [

                           s for s in category_skills

                           if s in resume_skills
                       ]

                       # strong category knowledge
                       if len(matched_in_category) >= 3:

                           matched_score += (
                               SKILLS_DB[skill] * 0.5
                           )

                       break

   # =========================
   # FINAL SCORE
   # =========================

    if total_possible_score > 0:

        score = (
            matched_score / total_possible_score
        )  * 100

    else:

        score = 0

   # =========================
   # QUALITY PENALTIES
   # =========================

    if experience_years == 0 and not practical_experience:
        score -= 10

    if not resume_sections["education"]:
        score -= 5

    if not resume_sections["projects"]:
        score -= 5
 
    # =========================
    # LIMIT SCORE
    # =========================

    score = max(0, min(score, 100))

    score = round(score, 2)

    # =========================
    # QUALITY PENALTIES
    # =========================

    if experience_years == 0 and not practical_experience:
        score -= 10

    if not resume_sections["education"]:
        score -= 5

    if not resume_sections["projects"]:
        score -= 5

    if score < 0:
        score = 0

    score = round(score, 2)

    # =========================
    # SUMMARY & SUGGESTIONS
    # =========================

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

        "categorized_matched_skills":
            categorized_matched_skills,

        "categorized_missing_skills":
            categorized_missing_skills,

        "experience": experience_years,

        "resume_sections": resume_sections,

        "summary": summary,

        "suggestions": suggestions,

        "resume_preview": resume_text[:500],

        "job_description": job_description,
    }