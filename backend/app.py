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
import requests
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


# =========================================================
# CREATE FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="SmartIntern AI",
    description="AI-Powered Internship Recommendation Engine",
    version="1.0.0"
)


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

create_tables()


# =========================================================
# TEMPORARY UPLOAD FOLDER
# =========================================================

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# INTERNSHIP DATA
# =========================================================

internships = [
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


# =========================================================
# APPLICATION STORAGE
# =========================================================

applications = []


# =========================================================
# PYDANTIC MODEL FOR REGISTRATION
# =========================================================

class Student(BaseModel):
    full_name: str
    email: str
    college: str
    degree: str
    skills: str


# =========================================================
# PYDANTIC MODEL FOR APPLICATION
# =========================================================

class Application(BaseModel):
    student_email: str
    company: str
    role: str


# =========================================================
# SEND REGISTRATION EMAIL USING RESEND
# =========================================================

def send_registration_email(student_name, student_email):

    try:

        # Check API key
        if not RESEND_API_KEY:
            print("RESEND_API_KEY not found in .env file")
            return False

        url = "https://api.resend.com/emails"

        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {

            "from": "SmartIntern AI <onboarding@resend.dev>",

            "to": [student_email],

            "subject": "🎉 Welcome to SmartIntern AI - Registration Successful",

            "html": f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>SmartIntern AI</title>

</head>

<body style="
margin:0;
padding:0;
background:#f4f7fb;
font-family:Arial,Helvetica,sans-serif;
">

<table width="100%"
       cellpadding="0"
       cellspacing="0"
       style="background:#f4f7fb;padding:30px 10px;">

<tr>

<td align="center">

<table width="600"
       cellpadding="0"
       cellspacing="0"
       style="
       max-width:600px;
       width:100%;
       background:white;
       border-radius:16px;
       overflow:hidden;
       box-shadow:0 4px 20px rgba(0,0,0,0.08);
       ">

<!-- HEADER -->

<tr>

<td style="
background:#111827;
padding:30px;
text-align:center;
">

<div style="
font-size:32px;
font-weight:bold;
color:white;
">

🤖 SmartIntern AI

</div>

<div style="
color:#d1d5db;
font-size:14px;
margin-top:8px;
">

AI-Powered Internship Recommendation Engine

</div>

</td>

</tr>


<!-- CONTENT -->

<tr>

<td style="padding:35px 30px;">

<h1 style="
margin:0 0 15px;
color:#111827;
font-size:26px;
">

🎉 Registration Successful!

</h1>


<p style="
color:#374151;
font-size:16px;
line-height:1.6;
">

Dear <strong>{student_name}</strong>,

</p>


<p style="
color:#374151;
font-size:16px;
line-height:1.6;
">

Welcome to <strong>SmartIntern AI</strong>!

Your registration has been completed successfully.

</p>


<!-- FEATURES -->

<table width="100%"
       cellpadding="0"
       cellspacing="0"
       style="
       background:#f9fafb;
       border-radius:12px;
       margin:25px 0;
       ">

<tr>

<td style="padding:20px;">

<p style="
margin:0 0 15px;
font-size:17px;
font-weight:bold;
color:#111827;
">

🚀 What you can do with SmartIntern AI

</p>

<p style="margin:8px 0;color:#374151;">
✅ Upload your resume
</p>

<p style="margin:8px 0;color:#374151;">
✅ Get AI-powered internship recommendations
</p>

<p style="margin:8px 0;color:#374151;">
✅ View AI match scores
</p>

<p style="margin:8px 0;color:#374151;">
✅ Apply for internships
</p>

<p style="margin:8px 0;color:#374151;">
✅ Track your applications
</p>

</td>

</tr>

</table>


<!-- BUTTON -->

<table width="100%"
       cellpadding="0"
       cellspacing="0">

<tr>

<td align="center">

<a href="https://smartintern-ai11-1.onrender.com"
   style="
   display:inline-block;
   background:#111827;
   color:white;
   text-decoration:none;
   padding:14px 28px;
   border-radius:8px;
   font-weight:bold;
   font-size:16px;
   ">

🚀 Open SmartIntern AI

</a>

</td>

</tr>

</table>


<p style="
color:#6b7280;
font-size:14px;
line-height:1.6;
margin-top:30px;
">

Thank you for registering with SmartIntern AI.

We wish you the best in finding your perfect internship!

</p>

</td>

</tr>


<!-- FOOTER -->

<tr>

<td style="
background:#f9fafb;
padding:25px;
text-align:center;
">

<p style="
margin:0;
color:#374151;
font-weight:bold;
">

SmartIntern AI Team

</p>

<p style="
margin:6px 0;
color:#6b7280;
font-size:13px;
">

Siva Sivani Degree College

</p>

<p style="
margin:10px 0 0;
color:#9ca3af;
font-size:12px;
">

AI-Powered Internship Recommendation Engine

</p>

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>
"""
        }


        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=20
        )


        if response.status_code in [200, 201]:

            print(
                "Registration email sent to:",
                student_email
            )

            return True


        print(
            "Email sending failed:",
            response.status_code,
            response.text
        )

        return False


    except Exception as error:

        print(
            "Email sending failed:",
            error
        )

        return False


# =========================================================
# HOME API
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
# GET ALL INTERNSHIPS
# =========================================================

@app.get("/internships")
def get_internships():

    return internships


# =========================================================
# REGISTER STUDENT
# =========================================================

@app.post("/register")
def register_student(student: Student):

    try:

        # Check whether student already exists

        existing_student = get_student_by_email(
            student.email
        )

        if existing_student:

            email_sent = send_registration_email(
                student.full_name,
                student.email
            )

            return {
                "message": "Student already registered - welcome email sent again",
                "email": student.email,
                "email_sent": email_sent
            }


        # Insert student into database

        insert_student(
            student.full_name,
            student.email,
            student.college,
            student.degree,
            student.skills
        )


        # Send welcome email

        email_sent = send_registration_email(
            student.full_name,
            student.email
        )


        return {

            "message": "Registration successful",

            "student": {
                "full_name": student.full_name,
                "email": student.email,
                "college": student.college,
                "degree": student.degree,
                "skills": student.skills
            },

            "email_sent": email_sent
        }


    except Exception as error:

        return {
            "message": "Registration failed",
            "error": str(error)
        }


# =========================================================
# GET ALL STUDENTS
# =========================================================

@app.get("/students")
def get_students():

    try:

        students = database_get_students()

        return students

    except Exception as error:

        return {
            "message": "Unable to get students",
            "error": str(error)
        }


# =========================================================
# UPLOAD RESUME
# =========================================================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    try:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )


        # Save uploaded file

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # Extract skills from resume

        skills = extract_skills(file_path)


        return {

            "message": "Resume uploaded successfully",

            "filename": file.filename,

            "skills": skills
        }


    except Exception as error:

        return {

            "message": "Resume upload failed",

            "error": str(error)
        }


# =========================================================
# GET RECOMMENDATIONS
# =========================================================

@app.get("/recommendations")
def get_recommendations():

    try:

        # Get latest student

        students = database_get_students()


        if not students:

            return []


        # Get last registered student

        student = students[-1]


        # Get student skills

        student_skills = student[4]


        # Convert skills string to list

        if isinstance(student_skills, str):

            student_skills_list = [
                skill.strip()
                for skill in student_skills.split(",")
                if skill.strip()
            ]

        else:

            student_skills_list = student_skills


        recommendations = []


        for internship in internships:

            score = calculate_match(
                student_skills_list,
                internship["skills"]
            )


            internship_copy = internship.copy()

            internship_copy["match_score"] = score


            recommendations.append(
                internship_copy
            )


        # Sort highest match first

        recommendations.sort(
            key=lambda x: x["match_score"],
            reverse=True
        )


        return recommendations


    except Exception as error:

        return {

            "message": "Recommendation failed",

            "error": str(error)
        }


# =========================================================
# APPLY FOR INTERNSHIP
# =========================================================

@app.post("/apply")
def apply_for_internship(
    application: Application
):

    try:

        new_application = {

            "student_email":
                application.student_email,

            "company":
                application.company,

            "role":
                application.role
        }


        applications.append(
            new_application
        )


        return {

            "message":
                "Application submitted successfully",

            "application":
                new_application
        }


    except Exception as error:

        return {

            "message":
                "Application failed",

            "error":
                str(error)
        }


# =========================================================
# GET APPLICATIONS
# =========================================================

@app.get("/applications")
def get_applications():

    return applications


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )