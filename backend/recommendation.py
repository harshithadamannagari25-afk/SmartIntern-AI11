def calculate_match(student_skills, required_skills):

    if not student_skills or not required_skills:
        return 0

    student_skills_lower = [
        skill.strip().lower()
        for skill in student_skills
    ]

    matched = 0

    for skill in required_skills:

        if skill.strip().lower() in student_skills_lower:
            matched += 1

    score = int(
        (matched / len(required_skills)) * 100
    )

    return score