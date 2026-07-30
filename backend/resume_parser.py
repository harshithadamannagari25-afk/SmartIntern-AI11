import pdfplumber

# List of skills to detect
SKILLS = [
    "Python",
    "SQL",
    "Power BI",
    "Excel",
    "Machine Learning",
    "Data Analysis",
    "Java",
    "C++",
    "Git",
    "Docker",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "FastAPI"
]

def extract_skills(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills