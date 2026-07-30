import sqlite3

DATABASE = "smartintern.db"


# Create database connection
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create student table
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


# Insert student registration data
def insert_student(full_name, email, college, degree, skills):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (full_name, email, college, degree, skills)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        full_name,
        email,
        college,
        degree,
        skills
    ))

    conn.commit()
    conn.close()


# Fetch all registered students
def get_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return students