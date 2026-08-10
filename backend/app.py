from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from resume_parser import extract_skills
from recommendation import calculate_match

from database import (
    create_tables,
    insert_student,
    get_student_by_email,
    get_students as database_get_students
)

import shutil
import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv


# =========================================================
# EMAIL CONFIGURATION
# =========================================================

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


# =========================================================
# SEND REGISTRATION EMAIL
# =========================================================

def send_registration_email(student_name, student_email):

    try:

        message = EmailMessage()

        message["Subject"] = "SmartIntern AI - Registration Successful"

        message["From"] = EMAIL_ADDRESS

        message["To"] = student_email

        message.set_content(
            f"""
Dear {student_name},

Congratulations!

Your registration for SmartIntern AI has been completed successfully.

You can now use SmartIntern AI to:

• Upload your resume
• Get AI-powered internship recommendations
• View AI match scores
• Apply for internships
• Track your applications

Thank you for registering with SmartIntern AI.

Best Regards,
SmartIntern AI Team
Siva Sivani Degree College
"""
        )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL_ADDRESS,
                EMAIL_APP_PASSWORD
            )

            smtp.send_message(message)

        print(
            "Registration email sent to:",
            student_email
        )

        return True

    except Exception as error:

        print(
            "Email sending failed:",
            error
        )

        return False


# =========================================================
# FASTAPI APPLICATION
# =========================================================

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

    allow_headers=["*"]

)


# =========================================================
# TEMPORARY STORAGE
# =========================================================

students = []

applications = []

student_skills = []


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to SmartIntern AI"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

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
def recommendations(email: str):

    # Get student from database

    student = get_student_by_email(email)


    # Student does not exist

    if student is None:

        return {

            "message": "Student not found",

            "skills": [],

            "recommendations": []

        }


    # Get student's skills

    student_skills = [

        skill.strip()

        for skill in student["skills"].split(",")

        if skill.strip()

    ]


    print(
        "Student email:",
        email
    )

    print(
        "Current student skills:",
        student_skills
    )


    results = []


    # Calculate match

    for job in get_internships():

        score = calculate_match(

            student_skills,

            job["skills"]

        )

        job["match_score"] = score

        results.append(job)


    # Highest match first

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


    # Convert skills into list

    student_skills = [

        skill.strip()

        for skill in student.skills.split(",")

        if skill.strip()

    ]


    # Save temporarily

    students.append(student)


    # Save permanently in SQLite

    insert_student(

        student.full_name,

        student.email,

        student.college,

        student.degree,

        student.skills

    )


    # =====================================================
    # SEND REGISTRATION EMAIL
    # =====================================================

    email_sent = send_registration_email(

        student.full_name,

        student.email

    )


    print(
        "Student registered:",
        student.full_name
    )

    print(
        "Student skills:",
        student_skills
    )


    return {

        "message":
            "Registration Successful!",

        "student":
            student,

        "skills":
            student_skills,

        "email_sent":
            email_sent

    }


# =========================================================
# GET STUDENTS
# =========================================================

@app.get("/students")
def get_students():

    return database_get_students()


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

        "message":
            "Application Submitted Successfully!",

        "application":
            application

    }


@app.get("/applications")
def get_applications():

    return applications


# =========================================================
# RESUME UPLOAD
# =========================================================

@app.post("/upload-resume")
async def upload_resume(

    email: str,

    file: UploadFile = File(...)

):

    global student_skills


    # -----------------------------------------------------
    # Check student
    # -----------------------------------------------------

    student = get_student_by_email(email)


    if student is None:

        return {

            "message":
                "Student not found",

            "skills": []

        }


    # -----------------------------------------------------
    # Create uploads folder
    # -----------------------------------------------------

    os.makedirs(

        "uploads",

        exist_ok=True

    )


    # -----------------------------------------------------
    # Save PDF
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Extract skills
    # -----------------------------------------------------

    student_skills = extract_skills(

        file_path

    )


    print(

        "Skills extracted from resume:",

        student_skills

    )


    # -----------------------------------------------------
    # Update database
    # -----------------------------------------------------

    insert_student(

        student["full_name"],

        student["email"],

        student["college"],

        student["degree"],

        ", ".join(student_skills)

    )


    print(

        "Database updated with resume skills:",

        student_skills

    )


    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {

        "message":
            "Resume uploaded successfully!",

        "filename":
            file.filename,

        "skills":
            student_skills

    }