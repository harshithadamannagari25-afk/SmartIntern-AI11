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


# =========================================================
# DATABASE
# =========================================================

create_tables()


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# TEMPORARY STORAGE
# =========================================================

students = []
applications = []

# Current student's skills
student_skills = []


# =========================================================
# HOME
# =========================================================

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


# =========================================================
# INTERNSHIPS
# =========================================================

def get_internships():

    return [

        {
            "id": 1,
            "company": "Microsoft",
            "role": "Data Analyst Intern",
            "stipend": "₹35,000/month",
            "location": "Hyderabad",
            "skills": [
                "Python",
                "SQL",
                "Power BI",
                "Excel"
            ]
        },

        {
            "id": 2,
            "company": "Google",
            "role": "AI Intern",
            "stipend": "₹50,000/month",
            "location": "Bangalore",
            "skills": [
                "Python",
                "Machine Learning",
                "SQL"
            ]
        },

        {
            "id": 3,
            "company": "Infosys",
            "role": "Python Developer Intern",
            "stipend": "₹20,000/month",
            "location": "Remote",
            "skills": [
                "Python",
                "Git",
                "FastAPI"
            ]
        }

    ]


@app.get("/internships")
def internships():

    return get_internships()


# =========================================================
# RECOMMENDATIONS
# =========================================================

@app.get("/recommendations")
def recommendations():

    print(
        "Current student skills:",
        student_skills
    )

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


# =========================================================
# STUDENT REGISTRATION
# =========================================================

class Student(BaseModel):

    full_name: str
    email: str
    college: str
    degree: str
    skills: str


@app.post("/register")
def register(student: Student):

    global student_skills

    # Save student
    students.append(student)

    # Convert comma-separated skills into list
    student_skills = [
        skill.strip()
        for skill in student.skills.split(",")
        if skill.strip()
    ]

    print(
        "Student registered:",
        student.full_name
    )

    print(
        "Student skills:",
        student_skills
    )

    return {

        "message": "Registration Successful!",

        "student": student,

        "skills": student_skills

    }


@app.get("/students")
def get_students():

    return students


# =========================================================
# APPLICATION
# =========================================================

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


# =========================================================
# RESUME UPLOAD
# =========================================================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    global student_skills

    # Create uploads folder
    os.makedirs(
        "uploads",
        exist_ok=True
    )

    # Save uploaded file
    file_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract skills from resume
    student_skills = extract_skills(
        file_path
    )

    print(
        "Skills extracted from resume:",
        student_skills
    )

    return {

        "message": "Resume uploaded successfully!",

        "filename": file.filename,

        "skills": student_skills

    }