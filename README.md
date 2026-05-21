# Resume-CV-Analyzer

An AI-powered Resume Analyzer web application built with **React**, **FastAPI**, and **NLP-based resume parsing** techniques.

This project helps users analyze resumes against job descriptions and provides a match score, experience estimation, and AI-style feedback.

---

## Live Demo

[https://my-resume-cv-analyzer.netlify.app/](https://my-resume-cv-analyzer.netlify.app/)

Try uploading a PDF resume and compare it with any job description.

---

## Features

* Upload PDF resumes
* Paste job descriptions
* Resume analysis against job roles
* Match score generation
* Experience estimation
* AI-powered resume feedback and improvement suggestions
* Responsive modern UI
* Loading spinner animation
* Full frontend-backend deployment

---

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS

### Backend

* FastAPI
* Python
* Uvicorn

### Deployment

* Netlify (Frontend)
* Render (Backend)

---

## Project Structure

```bash
Resume-CV-Analyzer/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── runtime.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
```

---

## Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/sayak53/Resume-CV-Analyzer.git
cd Resume-CV-Analyzer
```

---

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at:

```bash
http://127.0.0.1:8000
```

---

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```bash
http://localhost:5173
```

---

## API Endpoint

### Analyze Resume

```http
POST /analyze/
```

### Form Data

| Key             | Type     |
| --------------- | -------- |
| resume          | PDF File |
| job_description | Text     |

---

## Future Improvements

* Advanced NLP-based resume scoring
* ATS compatibility checker
* Skill gap analysis
* Resume improvement recommendations
* Authentication system
* Resume history dashboard
* Charts and analytics
* Multi-role resume matching

---

## Author

### Sayak Chakraborty

Full-stack project built with React, FastAPI, and Tailwind CSS.

---

