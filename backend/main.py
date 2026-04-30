from fastapi import FastAPI, File, UploadFile, Form
from PyPDF2 import PdfReader

app = FastAPI()

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}

@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    text = extract_text(resume.file)

    return {
        "message": "File received",
        "resume_preview": text[:300],
        "job_description": job_description[:100]
    }