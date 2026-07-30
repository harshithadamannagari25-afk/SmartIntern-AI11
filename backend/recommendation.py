def calculate_match(student_skills, required_skills):

    matched = 0

    for skill in required_skills:
        if skill.lower() in [s.lower() for s in student_skills]:
            matched += 1

    score = int((matched / len(required_skills)) * 100)

    return score