import sqlite3

DATABASE = "smartintern.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT UNIQUE,
        college TEXT,
        degree TEXT,
        skills TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_student(
    full_name,
    email,
    college,
    degree,
    skills
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (full_name, email, college, degree, skills)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(email)
    DO UPDATE SET
        full_name = excluded.full_name,
        college = excluded.college,
        degree = excluded.degree,
        skills = excluded.skills
    """, (
        full_name,
        email,
        college,
        degree,
        skills
    ))

    conn.commit()
    conn.close()


def get_student_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE email = ?",
        (email,)
    )

    student = cursor.fetchone()

    conn.close()

    return student


def get_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return students