from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from resume_parser import extract_skills
from recommendation import calculate_match
from database import create_tables

import shutil
import os

app = FastAPI(
    title="SmartIntern AI",
    version="1.0"
)

# Create database tables
create_tables()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage
students = []
applications = []
student_skills = []

# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "message": "Welcome to SmartIntern AI"
    }

@app.get("/health")
def health():
    return {
        "status": "Running"
    }

# ---------------- INTERNSHIPS ----------------

def get_internships():

    return [

        {
            "id": 1,
            "company": "Microsoft",
            "role": "Data Analyst Intern",
            "stipend": "₹35,000/month",
            "location": "Hyderabad",
            "skills": ["Python", "SQL", "Power BI", "Excel"]
        },

        {
            "id": 2,
            "company": "Google",
            "role": "AI Intern",
            "stipend": "₹50,000/month",
            "location": "Bangalore",
            "skills": ["Python", "Machine Learning", "SQL"]
        },

        {
            "id": 3,
            "company": "Infosys",
            "role": "Python Developer Intern",
            "stipend": "₹20,000/month",
            "location": "Remote",
            "skills": ["Python", "Git", "FastAPI"]
        }

    ]


@app.get("/internships")
def internships():
    return get_internships()


# ---------------- RECOMMENDATIONS ----------------

@app.get("/recommendations")
def recommendations():

    print("Recommendations are using:", student_skills)

    results = []

    for job in get_internships():

        score = calculate_match(
            student_skills,
            job["skills"]
        )

        job["match_score"] = score

        results.append(job)

    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results


# ---------------- STUDENT ----------------

class Student(BaseModel):

    full_name: str
    email: str
    college: str
    degree: str
    skills: str


@app.post("/register")
def register(student: Student):

    global student_skills

    students.append(student)

    student_skills = [
        skill.strip()
        for skill in student.skills.split(",")
    ]

    print("Student Skills from Registration:", student_skills)

    return {

        "message": "Registration Successful!",
        "student": student

    }


@app.get("/students")
def get_students():

    return students


# ---------------- APPLICATION ----------------

class Application(BaseModel):

    company: str
    role: str


@app.post("/apply")
def apply(application: Application):

    applications.append(application)

    return {

        "message": "Application Submitted Successfully!",
        "application": application

    }


@app.get("/applications")
def get_applications():

    return applications


# ---------------- RESUME UPLOAD ----------------

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    global student_skills

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    student_skills = extract_skills(file_path)

    print("Student Skills from Resume:", student_skills)

    return {

        "message": "Resume uploaded successfully!",
        "filename": file.filename,
        "skills": student_skills

    }
